import os
import json

# Set your parent directory here
PARENT_DIR = r"/Users/diegopartida/Desktop/TEC/Semestre8/Compu/Code-Fixer-LLM-Agent/fine-tuning-LLM/dataset/tssb_data_3M"
OUTPUT_FILE = "merged_tssb_dataset.jsonl"

with open(OUTPUT_FILE, "w", encoding="utf-8") as output:
    for root, dirs, files in os.walk(PARENT_DIR):
        for file in files:
            if file.endswith(".jsonl"):
                file_path = os.path.join(root, file)
                print(f"Processing: {file_path}")
                with open(file_path, "r", encoding="utf-8") as f:
                    for line in f:
                        try:
                            data = json.loads(line)
                            sstub_pattern = data.get("sstub_pattern", "UNKNOWN")
                            before = data.get("before", "").strip()
                            after = data.get("after", "").strip()

                            formatted = {
                                "Task": "Fix the issues",
                                "Bug Type": sstub_pattern,
                                "Buggy Code": before,
                                "completion": after
                            }

                            output.write(json.dumps(formatted) + "\n")
                        except Exception as e:
                            print(f"Error in file {file_path}: {e}")
