import json
import random

def modify_dataset(input_file, output_file):
    """
    Read JSON data, modify entries by adding random prefixes, and save to a new file.
    
    Args:
        input_file (str): Path to input JSON file
        output_file (str): Path to output JSON file
    """
    
    # Example lists of prefix strings - modify these according to your needs
    
    translation_prefixes = [
        ["Please translate this into Low German: \"", "Here is the translation into Low German: \""],
        ["Can you translate into low german?: \"", "Here is a translation in Low German: \""],
        ["Translate into low german: \"", "Here is the text translated into Low German:\""],
        ["translate to low german \"", "The Low German version is as follows:\""],
        ["Can you please translate into Lower German?: \"", "Below is the Low German translation:\""],
        ["Bitte übersetze dies ins plattdeutsche: \"", "Hier ist die Übersetzung ins plattdeutsche: \""],
        ["Könntest du das ins Plattdeutsche übersetzen? \"","Hier ist die plattdeutsche Übersetzung: \""],
        ["Übersetze den folgenden Text ins Plattdeutsche: \"", "So lautet die Übersetzung auf Plattdeutsch: \""],
        ["Wie würde das auf Plattdeutsch heißen? \"", "Die plattdeutsche Version lautet: \""],
        ["Übersetze das bitte ins Plattdeutsche:\"", "Hier ist die plattdeutsche Übersetzung: \""],
        ["übersetz auf plattdeutsch \"", "So lautet die Übersetzung auf Plattdeutsch: \""],
        ["Översett dat op platt: \"", "In’t Plattdüütsche översett hett dat: \""],
        ["Kannst du dat up plattdüütsch översetten?: \"", "Översett is dat: \""],
        ["Kannst du dat up platt översetten? \"", "Op Plattdüütsch översett: \""],
        ["Kannst du dat up plattdüütsch översetten \"", "Översett heet dat: \""]

    ]
    
    # Read the JSON file
    with open(input_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # Handle both single entry and list of entries
    if isinstance(data, dict):
        data = [data]
    
    newDataList = []
    # Process each entry
    for entry in data:
        text_prefix = random.choice(translation_prefixes)
        newData = dict()

        # Add random prefixes
        if 'translation' in entry:
            newData['question'] = text_prefix[0] + entry['translation'] + "\""
        
        if 'text' in entry:
            newData['answer'] = text_prefix[1] + entry['text'] + "\""

        newDataList.append(newData)
    
    # Save the modified data
    with open(output_file, 'w', encoding='utf-8') as f:
        if len(data) == 1:
            json.dump(newDataList[0], f, ensure_ascii=False, indent=4)
        else:
            json.dump(newDataList, f, ensure_ascii=False, indent=4)

# Example usage
if __name__ == "__main__":
    input_file = "new_translate_nds_en_clean1.json"
    output_file = "ENToNDS_clean_new.json"
    modify_dataset(input_file, output_file)