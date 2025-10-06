# Python Bugs Dataset Preparation Guide

This guide provides steps to prepare a curated dataset from the original `diff_benchmark.json` file available on Hugging Face.

## Original Dataset

The starting point is the `diff_benchmark.json` file, which can be found in the [public dataset](https://huggingface.co/datasets/Muennighoff/python-bugs) hosted by Hugging Face.

## Steps to Generate Curated Dataset

Follow these steps to transform and prepare your dataset:
1. **Download the Dataset**
   - Obtain the `diff_benchmark.json` file from Hugging Face.
   
2. **Convert Data**
   - Run the `convert_data.py` script inside the dataset:
     ```bash
     python convert_data.py
     ```
   - This will generate the `python_bugs.jsonl` file.

3. **Generate Unit Tests**
   - Execute the `unit_testing_agent.py` program:
     ```bash
     python unit_testing_agent.py
     ```
   - Ensure you have an Ollama local model available, as it is required to generate unit tests.
   - This step will create the `unitest_dataset.jsonl` file.
   
4. **Run the compiler**
    - Pass the `unitest_dataset.jsonl` to the C++ compiler.
    - This step will run the compiler and generate the `curated_dataset.jsonl` file.
## Requirements

- An Ollama local model for generating unit tests in Step 3.
- Python environment with necessary libraries installed (ensure you check any dependencies listed within the scripts).
