import json
import os
import read_moralizations as rm


directory_path = "/home/bruno/Desktop/GitProjects/moralization-detection"
dataset = []


for filename in os.listdir(directory_path):
    file_path = os.path.join(directory_path, filename)

    if (
        os.path.isfile(file_path)
        and filename.endswith(".json")
        and not filename.startswith("full")
    ):
        print(filename)
        with open(file_path, "r", encoding="utf-8") as json_file:
            new_data = json.load(json_file)

    dataset.extend(new_data)

dataset = rm.remove_doubles(dataset)
dataset = rm.remove_doubles(dataset)

with open("full_dataset.json", 'w', encoding="utf-8") as json_file:
    json.dump(dataset, json_file, indent=4)

print("Wrote .json dataset with ", len(dataset), " entries.")
