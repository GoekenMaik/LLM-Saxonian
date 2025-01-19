# example with OSCAR 2201
from datasets import load_dataset

dataset = load_dataset("oscar-corpus/OSCAR-2301",
                        language="nds", 
                        split="train")

dataset.save_to_disk("lowergermandataset")
