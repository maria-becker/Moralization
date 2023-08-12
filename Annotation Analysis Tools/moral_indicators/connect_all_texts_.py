import pandas as pd


def join_all_texts(sheet_list):

    # Delete old data
    with pd.ExcelWriter(f'all_texts-expanded.xlsx') as writer:
        df = pd.DataFrame()
        df.to_excel(writer)

    excel_file = pd.ExcelFile("all_texts.xlsx")

    role_list = ["Adressaten", "Benefizienten", "Forderer"]

    for sheet in sheet_list:
        df = excel_file.parse(sheet, header=None)
        df.columns = ["Lemma", "Insg"]
        df.set_index("Lemma", inplace=True)

        for role in role_list:
            role_excel_file = pd.ExcelFile(f'all_texts-{role}.xlsx')
            df_role = role_excel_file.parse(sheet, header=None)
            df_role.columns = ["Lemma", "Insg"]
            df_role.set_index("Lemma", inplace=True)

            df[role] = ([0] * len(df))
            for index, row in df.iterrows():
                print(index)
                try:
                    row[role] = df_role.loc[index, "Insg"]
                    print(row[role])
                except KeyError:
                    print("lel")

            print(df)

        with pd.ExcelWriter(f'all_texts-expanded.xlsx', mode="a", engine="openpyxl") as writer:
            df.to_excel(writer, sheet_name=sheet)








all_sheets = ["all", "best", "nouns", "names", "pronouns", "indefinitivpronomen"]

join_all_texts(all_sheets)
