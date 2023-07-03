import pandas
import regex as re
import xlsxwriter
import os
import glob


def fix_duplication(filename):

    df = pandas.read_excel(f"{filename}.xlsx", header=None)

    regex = re.compile(r"###(.*)\1###")

    # Define a function to apply the regular expression to each element in the 'Text' column
    def replace_with_regex(text):
        if regex.findall(str(text)):
            improved = re.sub(r"###(.*)\1###", r"###\1###", text)
            print(improved)
            return improved
        return text

    df[0] = df[0].apply(replace_with_regex)

    df[0] = df[0].apply(replace_with_regex)  # Just to be sure

    # WRITE TO EXCEL

    workbook = xlsxwriter.Workbook(f'#{filename}_fixed.xlsx')
    worksheet = workbook.add_worksheet()
    bold = workbook.add_format({'bold': True})

    row = 0
    for integer in range(0, df.size // 2):
        worksheet.write(row, 0, df[0][row], bold)
        # worksheet.write(row, 1, df[1][row])
        row += 1
        worksheet.write(row, 0, df[0][row])
        # worksheet.write(row, 1, df[1][row])
        row += 1

    workbook.close()

    return None


os.chdir(r"C:\Users\Arbeit\Desktop\Arbeit\Moralisierungen\Teil 14 Korrigieren\Fremdsprachen\IT-20230326T153543Z-001\IT")
for file in glob.glob("*.xlsx"):
    file = file[:-5]
    print(file)
    fix_duplication(file)
