import read_excel as re
import json


def genre_labels(filename):
    if filename.startswith("Gerichtsurteile"):
        return 1
    elif filename.startswith("Interviews"):
        return 2
    elif filename.startswith("Kommentare"):
        return 3
    elif filename.startswith("Leserbriefe"):
        return 4
    elif filename.startswith("Plenarprotokolle"):
        return 5
    elif filename.startswith("Wikipedia"):
        return 6
    elif filename.startswith("Prototypen"):
        return 99
    return 0


genres = [
    "Leserbriefe",
    "Interviews",
    "Plenarprotokolle",
    "Kommentare",
    "Gerichtsurteile",
    "Wikipedia Diskussionen"
]

filepaths = {
    "/home/bruno/Desktop/Databases/Moralization/Thematisierungen/Alle_bearbeiteten_Annotationen_negativ_final.xlsx": genres,
    "/home/bruno/Desktop/Databases/Moralization/Thematisierungen/Alle_bearbeiteten_Annotationen_positiv_final.xlsx": genres + ['Sachbücher']
}

for filepath, sheetnames in filepaths.items():
    for sheetname in sheetnames:
        print("\n", filepath, "--", sheetname)
        mappings = re.get_mappings_old(filepath, sheetname, [0, 1, 2])
        with open(
            f"prepared_{sheetname}_{filepath[61:-5]}.json",
            'w',
            encoding="utf-8"
        ) as json_file:
            json.dump(mappings, json_file, indent=4)
