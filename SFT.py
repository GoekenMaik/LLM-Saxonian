from transformers import (
    AutoModelForCausalLM,
    AutoTokenizer,
    DataCollatorForLanguageModeling,
    Trainer,
    TrainingArguments
)
from datasets import load_from_disk, load_dataset
import torch
import os
from pathlib import Path

# Configure cache directory
CACHE_DIR = "./model_cache"
os.makedirs(CACHE_DIR, exist_ok=True)
os.environ["PYTORCH_CUDA_ALLOC_CONF"] = "max_split_size_mb:256"

# Define the Llama 3.2 Instruct prompt template
LLAMA_3_2_TEMPLATE = "<|begin_of_text|><|start_header_id|>system<|end_header_id|>\n\nDu büst en höchst fähigen Hülper. Du schüllst in plattdüütsch antwoorten.<|eot_id|><|start_header_id|>user<|end_header_id|>\n{instruction}<|eot_id|><|start_header_id|>assistant<|end_header_id|>\n{response}<|eot_id|><|file_separator|>"

def prepare_data_for_sft(instruction_column, response_column, tokenizer, template, max_length=2048):
    """Tokenize and prepare text data for Supervised Fine-Tuning (SFT) using a template."""

    def tokenize_function(examples):
        instructions = examples[instruction_column]
        responses = examples[response_column]
        prompts = []
        for instruction, response in zip(instructions, responses):
            # Format the prompt using the Llama 3.2 template
            prompt_text = template.format(instruction=instruction, response=response)
            prompts.append(prompt_text)

        tokenized_inputs = tokenizer(
            prompts,
            truncation=True,
            max_length=max_length,
            padding='max_length',
            return_tensors="pt"
        )
        tokenized_inputs["labels"] = tokenized_inputs["input_ids"].clone() # Labels are the same as input_ids for Causal LM

        return tokenized_inputs

    return tokenize_function


def main():
    print("started")

    # Configure parameters
    #model_name = "meta-llama/Llama-3.2-8B-Instruct" # Using 8B Instruct as 3B Instruct might not be available, adjust if needed.
    output_dir = "./llama3.2-3B-Instruct-multi-dataset-sft/" # Adjusted output directory
    dataset_path = "combinedDatasets.json" # Path to your SFT dataset on disk.  Assume it's saved as "sft_dataset" using datasets.save_to_disk()

    # Download and cache the model locally (optional, if you want to use a local copy)
    # local_model_path = "./llama3.2-8B-Instruct/" ## model path # You can download and save the model manually and use this path
    local_model_path = "./llama3.2-3B-Instruct-multi-dataset/" # Use model_name directly if you want to download from Hugging Face Hub

    # Initialize tokenizer and model with specific Llama settings
    print("tokenizer load begin")
    tokenizer = AutoTokenizer.from_pretrained(
        local_model_path,
        padding_side="right",
        use_fast=False,  # Llama tokenizer doesn't support fast tokenization
    )
    # Add pad token if it doesn't exist (generally not needed for Llama tokenizers, but good practice)
    if not tokenizer.pad_token:
        tokenizer.pad_token = tokenizer.eos_token


    # Load dataset (modify this according to your data source)
    dataset = load_from_disk("./combinedDatasetHuggingfaceFormatOnlyTranslations")

    # Define instruction and response columns - ADJUST THESE TO YOUR DATASET COLUMN NAMES
    instruction_column = "question"
    response_column = "answer"

    print("tokenize dataset begin")
    # Tokenize dataset for SFT using the template
    print("tokenize dataset for SFT")
    tokenize_function = prepare_data_for_sft(instruction_column, response_column, tokenizer, LLAMA_3_2_TEMPLATE)
    tokenized_dataset = dataset.map(
        tokenize_function,
        batched=True,
        num_proc=4  # Adjust based on your CPU cores
    )

    # Create data collator for causal language modeling
    data_collator = DataCollatorForLanguageModeling(
        tokenizer=tokenizer,
        mlm=False  # Set to False for causal language modeling
    )


    print("model load begin")
    # Load model with specific Llama configurations
    model = AutoModelForCausalLM.from_pretrained(
        local_model_path,
        torch_dtype=torch.bfloat16,
        device_map="auto",  # Automatically handle model parallel loading
        use_cache=False  # Disable KV cache during training
    )

    # Define training arguments with Llama-specific optimizations
    training_args = TrainingArguments(
        output_dir=output_dir,
        overwrite_output_dir=True,
        num_train_epochs=5,
        per_device_train_batch_size=4,  # Adjust based on your GPU memory and model size
        gradient_accumulation_steps=32,  # Increase this for larger effective batch size
        save_steps=5000,
        save_total_limit=2,
        learning_rate=3e-4,
        warmup_steps=1000,
        logging_dir='./logs',
        logging_steps=100,
        gradient_checkpointing=True,  # Enable gradient checkpointing to save memory
        optim="adamw_torch_fused",  # Use fused AdamW for better performance
        dataloader_num_workers=4 # Adjust based on your CPU cores and data loading needs.
    )

    # Initialize trainer
    trainer = Trainer(
        model=model,
        args=training_args,
        data_collator=data_collator,
        train_dataset=tokenized_dataset,
    )

    # Start training
    print("start train")
    trainer.train()
    print("end train")

    # Save the model and tokenizer
    trainer.save_model()
    tokenizer.save_pretrained(output_dir)

if __name__ == "__main__":
    main()
