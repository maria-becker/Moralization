import pandas as pd

def combine_excel_files(file1, file2, output_file):
    """
    Combines two Excel files by appending the second file to the first
    and saves the result to a new Excel file.

    Parameters:
    - file1 (str): Filepath of the first Excel file.
    - file2 (str): Filepath of the second Excel file to be appended.
    - output_file (str): Filepath of the output Excel file where the combined data will be saved.
    """
    # Read the first Excel file into a DataFrame
    df1 = pd.read_excel(file1, header=None)

    # Read the second Excel file into another DataFrame
    df2 = pd.read_excel(file2, header=None)

    # Append the second DataFrame to the first one
    combined_df = df1.append(df2, ignore_index=True)

    # Save the combined DataFrame to a new Excel file
    combined_df.to_excel(output_file, index=False, header=None)
    print(f"Combined data saved to {output_file}")


file1_path_main = "Main_dwds_600.xlsx"
file2_path_main = "Main_wikibooks_400.xlsx"
output_file_path_main = "DE_Sachbücher_negativ-selection.xlsx"
file1_path_bkup = "Backup_dwds_300.xlsx"
file2_path_bkup = "Backup_wikibooks_200.xlsx"
output_file_path_bkup = "BACKUP_DE_Sachbücher_negativ-selection.xlsx"

combine_excel_files(file1_path_bkup, file2_path_bkup, output_file_path_bkup)
