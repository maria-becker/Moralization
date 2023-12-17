import read_moralizations as rm
import _util_ as util
import json
import os

# Specify the directory you want to walk through
directory_path = "/home/bruno/Desktop/Databases/Moralization/Deutsche_XMIs"


for filename in os.listdir(directory_path):
    file_path = os.path.join(directory_path, filename)

    # Check if it is a file (and not a directory)
    if (
        os.path.isfile(file_path)
        and "Wikipedia" not in filename
        and filename.endswith(".xmi")
    ):

        print(filename)

        mappings = rm.map_from_file(file_path, util.genre_labels(filename))
        with open(f"prepared_{filename}.json", 'w', encoding="utf-8") as f:
            json.dump(mappings, f, indent=4)
