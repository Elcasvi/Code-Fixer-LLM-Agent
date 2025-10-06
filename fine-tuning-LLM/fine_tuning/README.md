# Fine-Tuning LLM with Jupyter Notebooks

The `fine-tuning-LLM/fine_tuning` directory contains three Jupyter notebooks designed to help fine-tune a language model (LLM). Below are the steps and details for using each notebook.

## Notebook Workflow

### 1. unsloth-fine-hyper-parameters-tuning.ipynb

This notebook is used to find the optimal hyperparameters for fine-tuning the LLM. It should be run first as it will determine the best parameters, specifically `learning_rate` and `num_train_epochs`.

- **Output**: The notebook provides the best hyperparameter values (`best_params`) for further fine-tuning.

### 2. unsloth-fine-tuning.ipynb

After determining the optimal hyperparameters from the previous step, run this notebook to actually fine-tune the LLM using those parameters.

#### Prerequisites:
- Prepare the dataset in the following directory: `dataset/dataset_curation_agent/curated_dataset.jsonl`.

#### Outputs:
- **Results**: The fine-tuned model will be saved in the directory: `fine_tuning/results`.
- **Logs**: Training logs will be stored in this directory: `fine_tuning/logs`.

### 3. unsloth-inference.ipynb

This notebook performs inference using the fine-tuned model obtained from the second step.

#### Prerequisites:
- The fine-tuned model must exist inside the directory: `fine_tuning/results`.

## Prerequisite Installation

Before running any notebooks, you need to ensure that all necessary Python libraries are installed. Execute the following command:

```bash
pip install -r fine-tuning-LLM/requirements.txt
