import xlsxwriter
import pandas as pd


def list_to_excel(source_list, filepath):
    """
    Takes a list and writes it into the first column
    of an excel file.
    """

    workbook = xlsxwriter.Workbook(filepath)
    worksheet = workbook.add_worksheet("list")

    row = 0
    col = 0
    for item in source_list:
        worksheet.write(row, col, item)
        row += 1

    workbook.close()
    return None


def append_df_to_excel(df, filename, sheetname):
    """Appends a sheet of pandas dataframa data to an excel file."""
    with pd.ExcelWriter(filename, mode="a", engine="openpyxl") as writer:
        df.to_excel(writer, sheet_name=sheetname, index=False)

    return None
