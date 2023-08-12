import pandas as pd


def add_excel_sheets(list_of_genres, list_of_sheets):

    # Delete old data
    with pd.ExcelWriter(f'all_texts.xlsx') as writer:
        df = pd.DataFrame()
        df.to_excel(writer, index=False)

    # Write new data sheet for sheet
    for sheet in list_of_sheets:

        word_dict = {}
        for name in list_of_genres:

            # Open the Excel file
            excel_file = pd.ExcelFile(f"{name}-.xlsx")

            # Get the sheet you want to read
            df = excel_file.parse(sheet)
            dicty = df.to_dict(orient="split")
            for row in dicty["data"]:
                if row[0] in word_dict.keys():
                    word_dict[row[0]] += row[1]
                else:
                    word_dict[row[0]] = row[1]

        # Sort dictionary
        word_dict = {
            k: v for k, v in sorted(
                word_dict.items(), key=lambda item: item[1], reverse=True
            )
        }

        print(word_dict)
        print("\n")

        write_df = pd.DataFrame(word_dict.items())

        with pd.ExcelWriter(f'all_texts.xlsx', mode="a", engine="openpyxl") as writer:
            write_df.to_excel(writer, sheet_name=sheet, index=False, header=False)

    return True


all_genres = ["Gerichtsurteile", "Leserbriefe", "Interviews", "Kommentare"]
all_sheets = ["all", "best", "nouns", "names", "pronouns", "indefinitivpronomen"]

add_excel_sheets(all_genres, all_sheets)
