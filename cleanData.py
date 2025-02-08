import json
import os
from typing import List, Dict, Set

def clean_translations(
    input_file: str, 
    output_file: str, 
    excluded_strings: Set[str] = set(),
    length_ratio_threshold: float = 0.5
) -> None:
    """
    Clean translation dataset by removing entries where:
    1. Source and translation lengths differ significantly
    2. Translation is missing or empty
    3. Translation contains any of the specified excluded strings
    
    Args:
        input_file (str): Path to input JSON file
        output_file (str): Path to output JSON file
        excluded_strings (Set[str]): Set of strings that should not appear in translations
        length_ratio_threshold (float): Maximum allowed difference ratio between text lengths
    """
    cleaned_data = []
    skipped_entries = {
        "missing_translation": 0,
        "length_mismatch": 0,
        "invalid_entry": 0,
        "excluded_string": 0
    }
    
    try:
        # Read the input file
        with open(input_file, 'r', encoding='utf-8') as f:
            try:
                data = json.load(f)
            except json.JSONDecodeError:
                # Handle case where the file contains one JSON object per line
                f.seek(0)
                data = []
                for line in f:
                    if line.strip():
                        try:
                            data.append(json.loads(line))
                        except json.JSONDecodeError:
                            print(f"Warning: Skipping invalid JSON line: {line[:100]}...")
                            continue
    except FileNotFoundError:
        print(f"Error: Input file '{input_file}' not found.")
        return
    except Exception as e:
        print(f"Error reading input file: {str(e)}")
        return
    
    # Ensure data is a list
    if isinstance(data, dict):
        data = [data]
    
    # Process each entry
    for entry in data:
        try:
            # Check if translation exists and is not empty
            if not entry.get('translation') or not entry.get('text'):
                skipped_entries["missing_translation"] += 1
                continue
            
            # Check for excluded strings
            translation = entry['translation']
            if any(excl_str in translation for excl_str in excluded_strings):
                skipped_entries["excluded_string"] += 1
                continue
            
            text_length = len(entry['text'].split())
            translation_length = len(entry['translation'].split())
            
            # Calculate length ratio
            max_length = max(text_length, translation_length)
            min_length = min(text_length, translation_length)
            length_ratio = min_length / max_length if max_length > 0 else 0
            
            # Keep entry if length ratio is above threshold
            if length_ratio >= (1 - length_ratio_threshold):
                cleaned_data.append(entry)
            else:
                skipped_entries["length_mismatch"] += 1
        except (KeyError, AttributeError) as e:
            skipped_entries["invalid_entry"] += 1
            print(f"Warning: Skipping invalid entry: {str(e)}")
            continue
    
    # Save cleaned data
    try:
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(cleaned_data, f, ensure_ascii=False, indent=4)
    except Exception as e:
        print(f"Error writing output file: {str(e)}")
        return
    
    # Print statistics
    print("\nCleaning Statistics:")
    print(f"Original entries: {len(data)}")
    print(f"Cleaned entries: {len(cleaned_data)}")
    print("\nSkipped entries breakdown:")
    print(f"- Missing or empty translations: {skipped_entries['missing_translation']}")
    print(f"- Length mismatches: {skipped_entries['length_mismatch']}")
    print(f"- Contained excluded strings: {skipped_entries['excluded_string']}")
    print(f"- Invalid entries: {skipped_entries['invalid_entry']}")
    print(f"\nOutput saved to: {output_file}")


# Example usage
if __name__ == "__main__":
    input_file = "translate_nds_de.json"
    output_file = "translate_nds_de_clean1.json"

    # Define strings to exclude
    excluded_strings = {
        "translation of the text",
        "a translation of the",
        "the translation into",
        "a translation aiming",
        "a translation into",
        "a translation that aims",
        "the translation of",
        "Translation Choices:",
        "nglish translation of",
        "Natural English",
        "Natural english",
        "natural English",
        "natural english",
        "natural-sounding",
        "a natural feel",
        "English translation",
        "a translation focusing",
        "Übersetzung",
        "the translation, aiming"
    }
    
    clean_translations(input_file, output_file,excluded_strings, length_ratio_threshold=0.3)