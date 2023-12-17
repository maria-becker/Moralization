import read_excel as re
import json


filepaths = {
    "/home/bruno/Desktop/Databases/Moralization/Thematisierungen/BRUNO_Sachbücher_negativ.xlsx": ("Sheet1", "before_text", 7),
    "/home/bruno/Desktop/Databases/Moralization/Thematisierungen/Dengler_Annotation Plenarprotokolle-DE-neg.xlsx": ("Tabelle4", "col_0", 5)
}

for filepath, sheetinfo in filepaths.items():
    print("\n", filepath)
    mappings = re.get_mappings_new(filepath,
                                   sheetinfo[0],
                                   [0, 1, 2],
                                   sheetinfo[1],
                                   sheetinfo[2])

    with open(
        f"prepared_nonm_{filepath[61:-5]}.json",
        'w',
        encoding="utf-8"
    ) as json_file:
        json.dump(mappings, json_file, indent=4)


for filepath, sheetinfo in filepaths.items():
    print("\n", filepath)
    mappings = re.get_mappings_new(filepath,
                                   sheetinfo[0],
                                   [3],
                                   sheetinfo[1],
                                   sheetinfo[2])

    with open(
        f"prepared_mora_{filepath[61:-5]}.json",
        'w',
        encoding="utf-8"
    ) as json_file:
        json.dump(mappings, json_file, indent=4)
