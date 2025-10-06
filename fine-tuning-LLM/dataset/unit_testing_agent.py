from langgraph.graph import StateGraph, END
from typing import TypedDict, List, Dict
from langchain_ollama import ChatOllama
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
import time
import ast

model = ChatOllama(
    model="phi4:14b",
    temperature=0,
    callbacks=[StreamingStdOutCallbackHandler()],
)


# ---- Estado del agente ----
class CodeTestPair(TypedDict):
    task:str
    buggy_code:str
    correct_code: str
    unit_test: str

class AgentState(TypedDict):
    code_tests: List[Dict[str, str]]


def read_jsonl_node(state: AgentState) -> AgentState:
    print("[Reading] Reading file python_bugs.jsonl ...")
    with open("simple_python_bugs.jsonl", "r") as f:
        lines = f.readlines()

    code_tests = []
    for line in lines:
        data = json.loads(line)
        buggy_code = data["buggy_code"]
        correct_code = data["correct_code"]
        # Inject default/fake fields if not present
        code_tests.append({
            "task": "Fix the issue in the following Python code.",
            "buggy_code":buggy_code ,  # or extract if available
            "correct_code": correct_code,
            "unit_test": ""
        })

    print(f"[Reading] {len(code_tests)} codes has been read. Example:")
    if code_tests:
        print(f"[Reading] Example code:\n{code_tests[0]['correct_code'][:200]}\n---")
    return {"code_tests": code_tests}
# ---- Función 2: generar pruebas con LLM ----
import json
import re
from typing import Dict

def lm_call_node(state: Dict) -> Dict:
    print("[Generation] Generation unit test for each code example...")
    output_path = "unitest_dataset.jsonl"
    code_tests = []

    # Abrir el archivo en modo append al inicio
    with open(output_path, "a") as f:
        for idx, item in enumerate(state["code_tests"]):
            task=item["task"]
            buggy_code = item["buggy_code"]
            correct_code = item["correct_code"]
            print(f"[Generation] Generating test for code #{idx + 1} (first 100 chars):\n{correct_code[:100]}\n...")

            prompt = f"""You are a code evaluation assistant.

            Your task is to generate a Python function named `check(candidate)` that tests the correctness of the given implementation.
            The function named `candidate` will be passed into `check()`.
            
            Instructions:
            - Use only `assert` statements to validate that `candidate(...)` produces the correct results.
            - Derive inputs and expected outputs from the function’s docstring if available.
            - If there is no docstring, make reasonable assumptions based on the function logic.
            - Do not include the implementation of the function in the output — only the check() function.
            
            Example format:
            def check(candidate):
                assert candidate(2, 3) == 5
                assert candidate(-1, 1) == 0
            
            Code to test:
            {correct_code}
            """

            response = model.invoke(prompt)
            unit_test_raw = response.content.strip()

            # Extract the code block from Markdown-style formatting
            unit_test = unit_test_raw
            if '```' in unit_test_raw:
                matches = re.findall(r'```(?:python)?\n([\s\S]*?)```', unit_test_raw)
                if matches:
                    unit_test = matches[0].strip()
            unit_test = unit_test.strip()

            print(f"[Generation] Test generated (first 100 chars):\n{unit_test[:100]}\n---")


            try:
                ast.parse(unit_test)
                record = {
                    "task": task,
                    "buggy_code": buggy_code,
                    "correct_code": correct_code,
                    "unit_test": unit_test
                }

                f.write(json.dumps(record) + "\n")
                f.flush()

                code_tests.append(record)
                print(f"[Saved] Unit test #{idx + 1} saved successfully.")

            except SyntaxError as e:
                print(f"[SyntaxError] Skipping invalid unit test #{idx + 1}: {e}")

    print(f"[Generation] {len(code_tests)} unit tests has been generated.")
    return {"code_tests": code_tests}


# ---- Construcción del grafo ----
builder = StateGraph(AgentState)
builder.set_entry_point("read_jsonl")
builder.add_node("read_jsonl", read_jsonl_node)
builder.add_node("lm_call", lm_call_node)

builder.add_edge("read_jsonl", "lm_call")
builder.add_edge("lm_call", END)


graph = builder.compile()

# ---- Ejecución ----
print("[Execution] Starting unit tests generation pipeline...")
start=time.time()
for event in graph.stream({}):
    print(f"[Evento] {event}")

end = time.time()
length = end - start

hours = int(length // 3600)
minutes = int((length % 3600) // 60)
seconds = int(length % 60)
print(f"It took {hours} hours, {minutes} minutes, and {seconds} seconds to generate the unit tests!")
