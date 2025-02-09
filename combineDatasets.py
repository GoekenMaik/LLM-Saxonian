import json
import random

dataset1 = "DeToNDS_clean.json"
dataset2 = "EnToNDS_clean.json"
dataset3 = "datasetInJson.json"
datasets = [dataset1, dataset2, dataset3]

merged_data = []

for dataset in datasets:
    with open(dataset, "r", encoding='utf8') as file:
        data = json.load(file)
        for datapoint in data:
            merged_data.append(datapoint)

random.shuffle(merged_data)
with open("combinedDatasets.json", "w") as writeFile:
    json.dump(merged_data, writeFile, ensure_ascii=False, indent=4)