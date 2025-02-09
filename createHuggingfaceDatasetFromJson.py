import json
from datasets import Dataset
import pandas as pd

def create_dataset_from_json(json_path, output_dir):
    """
    Create a HuggingFace dataset from a JSON file containing question-answer pairs
    and save it to disk.
    
    Args:
        json_path (str): Path to the JSON file
        output_dir (str): Directory to save the dataset
    """
    # Read the JSON file
    with open(json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # If the JSON file is a list of dictionaries, use it directly
    # If it's not a list (single object), wrap it in a list
    if not isinstance(data, list):
        data = [data]
    
    # Convert to DataFrame first (makes it easier to handle)
    df = pd.DataFrame(data)
    
    # Create HuggingFace Dataset
    dataset = Dataset.from_pandas(df)
    
    # Save to disk
    dataset.save_to_disk(output_dir)
    
    print(f"Dataset created with {len(dataset)} examples")
    print(f"Dataset features: {dataset.features}")
    return dataset

# Example usage
if __name__ == "__main__":
    # Replace these paths with your actual paths
    json_path = "combinedDatasets.json"
    output_dir = "./combinedDatasetHuggingfaceFormat"
    
    dataset = create_dataset_from_json(json_path, output_dir)
    
    # Verify the data
    print("\nFirst example:")
    print(dataset[0])
    print(dataset[55])