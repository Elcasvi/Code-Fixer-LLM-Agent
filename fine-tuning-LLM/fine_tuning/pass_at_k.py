import torch
from tqdm import tqdm
import evaluate

def load_evaluation_framework():
    return evaluate.load("code_eval")


def generate_completions(model, tokenizer, prompts, num_completions, max_new_tokens):
    all_predictions = []
    model.eval()

    for prompt in tqdm(prompts, desc="Generating Completions"):
        input_ids = tokenizer(prompt, return_tensors="pt").input_ids.cuda()
        outputs = model.generate(
            do_sample=True,
            top_k=50,
            top_p=0.95,
            temperature=0.7,
            num_return_sequences=num_completions,
            max_new_tokens=max_new_tokens,
            pad_token_id=tokenizer.eos_token_id
        )

        torch.cuda.empty_cache()
        decoded = tokenizer.batch_decode(outputs, skip_special_tokens=True)
        cleaned = clean_decoded_outputs(decoded)
        all_predictions.append(cleaned)

    return all_predictions


def clean_decoded_outputs(decoded):
    cleaned = []
    for d in decoded:
        parts = d.split("### Fixed Code:")
        cleaned.append(parts[-1].strip() if len(parts) > 1 else d.strip())
    return cleaned


def compute_pass_at_k(code_eval, references, predictions, k_values):
    print("\n All completions generated. Computing pass@k...\n")
    result, _ = code_eval.compute(
        references=references,
        predictions=predictions,
        k=k_values,
    )

    print("🎯 Final pass@k scores:")
    for k in k_values:
        score = result.get(f'pass@{k}', 'N/A')
        if isinstance(score, (float, int)):
            print(f"pass@{k}: {score:.4f}")
        else:
            print(f"pass@{k}: {score}")

    return result


def create_prompts(test_dataset):
    prompts = []
    for ex in test_dataset:
        prompt = f"""Below is an instruction that describes a task, paired with an input that provides further context. Write a response that appropriately completes the request.

### Instruction:
{ex["task"]}

### Input:
{ex["buggy_code"]}

### Response:"""
        prompts.append(prompt)
    return prompts
