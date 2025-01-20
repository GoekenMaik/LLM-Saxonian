from transformers import (
    AutoModelForCausalLM,
    AutoTokenizer,
    DataCollatorForLanguageModeling,
    Trainer,
    TrainingArguments
)
from datasets import load_from_disk
import torch
import os
from pathlib import Path


# Configure cache directory
CACHE_DIR = "./model_cache"
os.makedirs(CACHE_DIR, exist_ok=True)
os.environ["PYTORCH_CUDA_ALLOC_CONF"] = "max_split_size_mb:512"

def download_model(model_name, cache_dir):
    """Download and cache the model locally"""
    local_model_path = Path(cache_dir) / model_name.split('/')[-1]
    
    if not local_model_path.exists():
        print(f"Downloading model to {local_model_path}...")
        
        # Download tokenizer
        tokenizer = AutoTokenizer.from_pretrained(
            model_name,
            padding_side="right",
            use_fast=False,
            cache_dir=cache_dir
        )
        tokenizer.save_pretrained(local_model_path)
        
        # Download model
        model = AutoModelForCausalLM.from_pretrained(
            model_name,
            torch_dtype=torch.bfloat16,
            cache_dir=cache_dir
        )
        model.save_pretrained(local_model_path)
        
        print(f"Model downloaded and cached at {local_model_path}")
    else:
        print(f"Using cached model from {local_model_path}")
    
    return str(local_model_path)

def prepare_data(text_column, tokenizer, max_length=512):
    """Tokenize and prepare text data for causal language modeling."""
    def tokenize_function(examples):
        outputs = tokenizer(
            examples[text_column],
            truncation=True,
            max_length=max_length,
            padding='max_length',
            return_tensors="pt"
        )
        # For causal LM, labels are the same as inputs
        outputs["labels"] = outputs["input_ids"].clone()
        return outputs
    return tokenize_function

def main():
    print("started")

    # Configure parameters
    model_name = "meta-llama/Llama-3.2-3B" 
    text_column = "text"  # column containing text in your dataset
    output_dir = "./llama3.2-3BlowGerman"

    # Download and cache the model locally
    print("start model download")
    local_model_path = download_model(model_name, CACHE_DIR)
    print("end model download")

    # Initialize tokenizer and model with specific Llama settings
    tokenizer = AutoTokenizer.from_pretrained(
        local_model_path,
        padding_side="right",
        use_fast=False,  # Llama tokenizer doesn't support fast tokenization
    )
    # Add pad token if it doesn't exist
    if not tokenizer.pad_token:
        tokenizer.pad_token = tokenizer.eos_token
    
    print("start model loading")
    # Load model with specific Llama configurations
    model = AutoModelForCausalLM.from_pretrained(
        local_model_path,
        torch_dtype=torch.bfloat16,
        device_map="auto",  # Automatically handle model parallel loading
        use_cache=False  # Disable KV cache during training
    )
    print("end model loading")
    
    # Load dataset (modify this according to your data source)
    print("start dataset loading")
    dataset = load_from_disk("lowergermandataset")
    print("end dataset loading")

    # Tokenize dataset
    tokenize_function = prepare_data(text_column, tokenizer)
    tokenized_dataset = dataset.map(
        tokenize_function,
        batched=True,
        remove_columns=dataset.column_names,
        num_proc=4  # Adjust based on your CPU cores
    )
    
    # Create data collator for causal language modeling
    data_collator = DataCollatorForLanguageModeling(
        tokenizer=tokenizer,
        mlm=False  # Set to False for causal language modeling
    )
    
    # Define training arguments with Llama-specific optimizations
    training_args = TrainingArguments(
        output_dir=output_dir,
        overwrite_output_dir=True,
        num_train_epochs=3,
        per_device_train_batch_size=4,  # Reduced batch size due to model size
        gradient_accumulation_steps=32,  # Increase this for larger effective batch size
        save_steps=5000,
        save_total_limit=2,
        learning_rate=5e-5,  # Lower learning rate for fine-tuning
        warmup_steps=1000,
        logging_dir='./logs',
        logging_steps=100,
        gradient_checkpointing=True,  # Enable gradient checkpointing to save memory
        optim="adamw_torch_fused",  # Use fused AdamW for better performance
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
