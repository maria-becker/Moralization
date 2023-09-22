import pandas as pd
import xlsxwriter


def randomize_and_sort_corpus(corpus_file,
                              goal_name,
                              main_corpus_size,
                              backup_corpus_size,
                              seed):
    """
    Creates a main and backup random corpus from corpus_file,
    and then sorts them alphabetically.
    """
    # Read the entire corpus into a DataFrame
    dataframe = pd.read_excel(corpus_file, header=None)
    dataframe = dataframe.drop_duplicates()

    # Shuffle the rows in the DataFrame
    dataframe = dataframe.sample(frac=1, random_state=seed)

    # Split the DataFrame into main and backup
    main_corpus = dataframe.iloc[:main_corpus_size].reset_index(drop=True)
    backup_corpus = dataframe.iloc[main_corpus_size:main_corpus_size + backup_corpus_size].reset_index(drop=True)

    # Sort main and backup corpuses alphabetically
    main_corpus = main_corpus.sort_values(by=0, ignore_index=True)
    backup_corpus = backup_corpus.sort_values(by=0, ignore_index=True)

    # Create main corpus Excel file
    main_filename = f'Main_{goal_name}_{main_corpus_size}.xlsx'
    main_workbook = xlsxwriter.Workbook(main_filename)
    main_worksheet = main_workbook.add_worksheet()

    for index, row in main_corpus.iterrows():
        if not pd.isna(row[0]):  # Check if the cell is not empty
            main_worksheet.write(index, 0, row[0])

    main_workbook.close()

    # Create backup corpus Excel file
    backup_filename = f'Backup_{goal_name}_{backup_corpus_size}.xlsx'
    backup_workbook = xlsxwriter.Workbook(backup_filename)
    backup_worksheet = backup_workbook.add_worksheet()

    for index, row in backup_corpus.iterrows():
        if not pd.isna(row[0]):  # Check if the cell is not empty
            backup_worksheet.write(index, 0, row[0])

    backup_workbook.close()

    print("Done!")


if __name__ == "__main__":
    corpus_file = r"dwds-Kern\Sach-neg-dwds_20_21.xlsx"
    goal_name = "dwds"
    seed = 1998  # Use 1998 for consistent results.
    main_corpus_size = 600
    backup_corpus_size = 300

    randomize_and_sort_corpus(corpus_file,
                              goal_name,
                              main_corpus_size,
                              backup_corpus_size,
                              seed)
