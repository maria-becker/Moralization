import pandas as pd
from HanTa import HanoverTagger as ht
import re
import nltk
import scipy.stats as stats
import xlsxwriter
import numpy as np


spans_path = (
    r"C:\Users\Arbeit\Desktop\Bachelorarbeit\Data"
    r"\Data_Jypiter\Spans_and_instances.xlsx"
)
positive_path = (
    r"C:\Users\Arbeit\Desktop\Bachelorarbeit\Data"
    r"\Kategorisierungen\Alle_bearbeiteten_Annotationen_positiv_final.xlsx"
)
negative_path = (
    r"C:\Users\Arbeit\Desktop\Bachelorarbeit\Data"
    r"\Kategorisierungen\Alle_bearbeiteten_Annotationen_negativ_final.xlsx"
)
relev_textsorten_dict = {
    "Leserbriefe": ["Column4", "Column13"],
    "Interviews": ["Column12", "Column5"],
    "Gerichtsurteile": ["Column8", "Column10"],
    "Kommentare": ["Column14", "Column11"],
    "Plenarprotokolle": ["Column6", "Column7"],
    "Sachbücher": ["Column3"]
}


def nonmoral_df(sheet_name, categories):
    """
    Creates a dataframe which includes spans of the categories specified.

    Parameters:
        sheet_name: genre string, e.g. "Gerichtsurteile"
        categories: 0, 1, 2, 3 like in the sheets
    Returns:
        Dataframe that has all the spans from the genre and category specified.
    """

    # Load the Excel file into a pandas dataframe
    df_neg = pd.read_excel(
        negative_path,
        sheet_name=sheet_name,
        header=None)
    df_pos = pd.read_excel(
        positive_path,
        sheet_name=sheet_name,
        header=None)

    dataframe_list = [df_neg, df_pos]

    # Create two empty dataframes
    nonmoral_df = pd.DataFrame()

    # Loop through the rows in the dataframe
    for df in dataframe_list:
        for index, row in df.iterrows():
            # Check the value in the second column
            if row[1] in categories:
                # Add the row to the second dataframe
                if index % 2 == 1:
                    nonmoral_df = nonmoral_df.append(row)

    return nonmoral_df


def moral_list(sheet_name):
    """
    Reads an excel file which lists all spans annotated as 'moralization'.
    Returns the sentences annotated that way as a list of strings.

    Parameters:
        sheet_name: genre string, e.g. "Gerichtsurteile"
    Returns:
        list of strings which were annotated as moralizations.
    """

    excel_file = pd.ExcelFile(spans_path)
    df = excel_file.parse('spans_out')

    # Read data
    moralisierung_list = []
    for column in relev_textsorten_dict[sheet_name]:
        for row in range(2, 7):
            try:
                data = df.at[row, column]
                data_list = data.split(" ### ")
                # Remove duplicates
                moralisierung_list = moralisierung_list + list(
                    set(data_list) - set(moralisierung_list))
            except AttributeError:
                print("No spans at (Row" + str(row) + " / " + column + ").")

    return moralisierung_list


def get_comparison_list(
    filename,
    header,
    comparison_sheet,
    dont_count_list=[],
    top_hits=0
):

    comparison_list = []
    df_protag = pd.read_excel(
        filename, sheet_name=comparison_sheet, header=header)

    # Use all entries in the list if no maximum was set
    if top_hits == 0:
        top_hits = len(df_protag)

    # Add all relevant Lemmas to the list that will get compared
    for index, row in df_protag.iterrows():
        if index < top_hits:
            if not row[1] == -1:
                comparison_list.append(row[0])

    # Remove unwanted entries from list
    for entry in dont_count_list:
        if entry in comparison_list:
            comparison_list.remove(entry)

    return comparison_list


def compare_lemma_likelihood(
    sheet_name,
    comparison_list,
    nonmoral_categories=[0]
):
    """
    This function compares moralizing and non-moralizing segments.
    In particular, it calculates the frequency of 'protagonist' terms
    """

    # Get nonmoral spans from excel sheets
    df_thema = nonmoral_df(sheet_name, nonmoral_categories)
    # Get moralizing spans SSC excel sheets
    moralisierung_list = moral_list(sheet_name)

    tagger = ht.HanoverTagger('morphmodel_ger.pgz')

    print("COMPARISON LIST (MANUAL): ", str(comparison_list))

    counter_moral_prot = 0
    counter_moral_n = 0
    counter_them_prot = 0
    counter_them_n = 0

    # Loop through the rows in the dataframe of moralizing segments
    for morali in moralisierung_list:
        tokenized_sents = nltk.tokenize.word_tokenize(
            morali, language='german')
        tags = tagger.tag_sent(tokenized_sents)
        for tag in tags:
            if tag[1] in comparison_list:
                counter_moral_prot += 1
            counter_moral_n += 1

    # Loop through the rows in the dataframe of non-moralizing segments
    for index, row in df_thema.iterrows():
        tokenized_sents = nltk.tokenize.word_tokenize(
            row[0], language='german')
        tags = tagger.tag_sent(tokenized_sents)
        for tag in tags:
            if tag[1] in comparison_list:
                counter_them_prot += 1
            counter_them_n += 1

    # Calculate the likelihood that a token in a given text type
    # (moralizing vs non-moralizing) is on the list of protagonists
    try:
        likelihood_moral = counter_moral_prot / counter_moral_n
        likelihood_them = counter_them_prot / counter_them_n

        not_prot_moral = counter_moral_n - counter_moral_prot
        not_prot_them = counter_them_n - counter_them_prot

        contingency_table = [
            [counter_moral_prot, not_prot_moral],
            [counter_them_prot, not_prot_them]
        ]

        res = stats.fisher_exact(contingency_table)

        print("\nLIKELIHOOD MORAL (Percent): ", str(likelihood_moral * 100))
        print("LIKELIHOOD THEM  (Percent): ", str(likelihood_them * 100))

        ratio = (
            likelihood_moral
            / likelihood_them
        )
        diff_coeficient = (
            (likelihood_moral - likelihood_them)
            / (likelihood_moral + likelihood_them)
        )

        # Compare the likelihoods
        print("\nRATIO: ", str(ratio))
        print("DIFF COEFF: ", str(diff_coeficient))
        print("PROBABILITY FISHER: ", str(res.pvalue))
    except ZeroDivisionError:
        print("Error: Division by zero.")

    return None


def compare_pos_likelihood(
    sheet_name,
    pos_list,
    categories=[0]
):
    """
    This function compares moralizing and non-moralizing segments.
    In particular, it calculates the frequency of 'protagonist' terms
    """

    # Get nonmoral spans from excel sheets
    df_thema = nonmoral_df(sheet_name, categories)
    # Get moralizing spans SSC excel sheets
    moralisierung_list = moral_list(sheet_name)

    counter_moral_prot = 0
    counter_moral_n = 0
    counter_them_prot = 0
    counter_them_n = 0

    tagger = ht.HanoverTagger('morphmodel_ger.pgz')

    # Loop through the rows in the dataframe of moralizing segments
    for morali in moralisierung_list:
        tokenized_sents = nltk.tokenize.word_tokenize(
            morali, language='german')
        tags = tagger.tag_sent(tokenized_sents)
        for tag in tags:
            if tag[2] in pos_list:
                counter_moral_prot += 1
            counter_moral_n += 1

    # Loop through the rows in the dataframe of non-moralizing segments
    for index, row in df_thema.iterrows():
        tokenized_sents = nltk.tokenize.word_tokenize(
            row[0], language='german')
        tags = tagger.tag_sent(tokenized_sents)
        for tag in tags:
            if tag[2] in pos_list:
                counter_them_prot += 1
            counter_them_n += 1

    # Calculate the likelihood that a token in a given text type
    # (moralizing vs non-moralizing) is on the list of protagonists
    likelihood_moral = counter_moral_prot / counter_moral_n
    likelihood_them = counter_them_prot / counter_them_n

    contingency_table = [
        [counter_moral_prot, counter_moral_n - counter_moral_prot],
        [counter_them_prot, counter_them_n - counter_them_prot]
    ]
    print(contingency_table)

    res = stats.fisher_exact(contingency_table)

    print("\nLIKELIHOOD MORAL (Prozent): ", str(likelihood_moral * 100))
    print("LIKELIHOOD THEM  (Prozent): ", str(likelihood_them * 100))

    ratio = (
            likelihood_moral
            / likelihood_them
    )
    diff_coeficient = (
        (likelihood_moral - likelihood_them)
        / (likelihood_moral + likelihood_them)
    )

    try:
        # Compare the likelihoods
        print("\nRATIO: ", str(ratio))
        print("DIFF COEFF OLD: ", str(diff_coeficient))
        print("PROBABILITY FISHER: ", str(res.pvalue))
    except ZeroDivisionError:
        print("Error: Division by zero.")

    return 0


def compare_lemma_likelihood_dict(
    sheet_name=0,
    comparison_list=0,
    categories=[0]
):
    """
    This function compares moralizing and non-moralizing segments.
    In particular, it calculates the frequency of 'protagonist' terms
    """

    # Get nonmoral spans from excel sheets
    df_thema = nonmoral_df(sheet_name, categories)
    # Get moralizing spans SSC excel sheets
    moralisierung_list = moral_list(sheet_name)

    comparison_dict = {k: None for k in comparison_list}
    for key in comparison_dict:
        comparison_dict[key] = [0, 0]   # [counter_moral, counter_them]

    # Print just to be sure
    print("COMPARISON DICT: ", str(comparison_dict))

    counter_moral_n = 0
    counter_them_n = 0

    tagger = ht.HanoverTagger('morphmodel_ger.pgz')

    # Loop through the rows in the dataframe of moralizing segments
    for morali in moralisierung_list:
        tokenized_sents = nltk.tokenize.word_tokenize(
            morali, language='german')
        tags = tagger.tag_sent(tokenized_sents)
        for tag in tags:
            if tag[1] in comparison_dict.keys():
                comparison_dict[tag[1]][0] += 1
            counter_moral_n += 1

    # Loop through the rows in the dataframe of non-moralizing segments
    for index, row in df_thema.iterrows():
        tokenized_sents = nltk.tokenize.word_tokenize(
            row[0], language='german')
        tags = tagger.tag_sent(tokenized_sents)
        for tag in tags:
            if tag[1] in comparison_dict.keys():
                comparison_dict[tag[1]][1] += 1
            counter_them_n += 1

    results_dict = {k: None for k in comparison_dict.keys()}
    for lemma in results_dict:
        counter_moral_prot = comparison_dict[lemma][0]
        counter_them_prot = comparison_dict[lemma][1]
        likelihood_moral = counter_moral_prot / counter_moral_n
        likelihood_them = counter_them_prot / counter_them_n

        contingency_table = [
            [counter_moral_prot, counter_moral_n - counter_moral_prot],
            [counter_them_prot, counter_them_n - counter_them_prot]
        ]

        res = stats.fisher_exact(contingency_table)

        ratio = None
        diff_coeficient = (
            (likelihood_moral - likelihood_them)
            / (likelihood_moral + likelihood_them)
        )
        try:
            # Compare the likelihoods
            ratio = likelihood_moral / likelihood_them
        except ZeroDivisionError:
            ratio = False

        results_dict[lemma] = {
            "ratio": ratio,
            "diff_co": diff_coeficient,
            "pvalue": res.pvalue
        }

    return results_dict


def compare_lemma_likelihood_fulltexts(
    comparison_list,
    ignore_sheet=[],
    categories=[0],
):
    """
    This function compares moralizing and non-moralizing segments.
    In particular, it calculates the frequency of 'protagonist' terms
    """

    sheet_list = ["Gerichtsurteile", "Interviews", "Kommentare", "Leserbriefe"]
    sheet_list = [sheet for sheet in sheet_list if sheet not in ignore_sheet]

    df_thema = pd.DataFrame()
    moralisierung_list = []

    for sheet in sheet_list:
        # Load the Excel file into a pandas dataframe
        df_neg = pd.read_excel(
            negative_path,
            sheet_name=sheet,
            header=None)
        df_pos = pd.read_excel(
            positive_path,
            sheet_name=sheet,
            header=None)

        dataframe_list = [df_neg, df_pos]

        # Loop through the rows in the dataframe
        for df in dataframe_list:
            for index, row in df.iterrows():
                # Check the value in the second column
                if row[1] in categories:
                    # Add the row to the second dataframe
                    if index % 2 == 1:
                        df_thema = df_thema.append(row)

        # Open the Excel file
        excel_file = pd.ExcelFile(spans_path)

        # Get the sheet you want to read
        df = excel_file.parse('spans_out')

        # Read data
        for column in relev_textsorten_dict[sheet]:
            for row in range(2, 7):
                try:
                    data = df.at[row, column]
                    data_list = data.split(" ### ")

                    # Zuerst Duplikate entfernen
                    moralisierung_list = moralisierung_list + list(
                        set(data_list) - set(moralisierung_list))
                except AttributeError:
                    print("No values @ (Row" + str(row) + " / " + column + ")")

    counter_moral_prot = 0
    counter_moral_n = 0
    counter_them_prot = 0
    counter_them_n = 0

    tagger = ht.HanoverTagger('morphmodel_ger.pgz')

    # Loop through the rows in the dataframe of moralizing segments
    for morali in moralisierung_list:
        tokenized_sents = nltk.tokenize.word_tokenize(
            morali, language='german')
        tags = tagger.tag_sent(tokenized_sents)
        for tag in tags:
            if tag[1] in comparison_list:
                counter_moral_prot += 1
            counter_moral_n += 1

    # Loop through the rows in the dataframe of non-moralizing segments
    for index, row in df_thema.iterrows():
        tokenized_sents = nltk.tokenize.word_tokenize(
            row[0], language='german')
        tags = tagger.tag_sent(tokenized_sents)
        for tag in tags:
            if tag[1] in comparison_list:
                counter_them_prot += 1
            counter_them_n += 1

    # Calculate the likelihood that a token in a given text type
    # (moralizing vs non-moralizing) is on the list of protagonists
    likelihood_moral = counter_moral_prot / counter_moral_n
    likelihood_them = counter_them_prot / counter_them_n

    contingency_table = [
        [counter_moral_prot, counter_moral_n - counter_moral_prot],
        [counter_them_prot, counter_them_n - counter_them_prot]
    ]
    print(contingency_table)

    res = stats.fisher_exact(contingency_table)

    print("\nLIKELIHOOD MORAL (Prozent): ", str(likelihood_moral * 100))
    print("LIKELIHOOD THEM  (Prozent): ", str(likelihood_them * 100))

    ratio = (
        likelihood_moral
        / likelihood_them
    )
    diff_coeficient = (
        (likelihood_moral - likelihood_them)
        / (likelihood_moral + likelihood_them)
    )

    try:
        # Compare the likelihoods
        print("\nRATIO: ", str(ratio))
        print("DIFF COEFF OLD: ", str(diff_coeficient))
        print("PROBABILITY FISHER: ", str(res.pvalue))
    except ZeroDivisionError:
        print("Error: Division by zero.")

    return 0


def compare_lemma_likelihood_fulltext_dict(
    comparison_list=0,
    ignore_genre=[],
    categories=[0],
):
    """
    This function compares moralizing and non-moralizing segments.
    In particular, it calculates the frequency of 'protagonist' terms
    """

    sheet_list = ["Gerichtsurteile", "Interviews", "Kommentare", "Leserbriefe"]
    sheet_list = [sheet for sheet in sheet_list if sheet not in ignore_genre]

    df_thema = pd.DataFrame()
    moralisierung_list = []

    # Load the Excel file into a pandas dataframe
    for sheet in sheet_list:
        df_neg = pd.read_excel(
            negative_path,
            sheet_name=sheet,
            header=None)
        df_pos = pd.read_excel(
            positive_path,
            sheet_name=sheet,
            header=None)

        dataframe_list = [df_neg, df_pos]

        # Loop through the rows in the dataframe
        for df in dataframe_list:
            for index, row in df.iterrows():
                # Check the value in the second column
                if row[1] in categories:
                    # Add the row to the second dataframe
                    if index % 2 == 1:
                        df_thema = df_thema.append(row)

        print(df_thema)

        # Open the Excel file
        excel_file = pd.ExcelFile(spans_path)
        # Get the sheet you want to read
        df = excel_file.parse('spans_out')

        # Read data
        for column in relev_textsorten_dict[sheet]:
            for row in range(2, 7):
                try:
                    data = df.at[row, column]
                    data_list = data.split(" ### ")

                    # Zuerst Duplikate entfernen
                    moralisierung_list = moralisierung_list + list(
                        set(data_list) - set(moralisierung_list))
                except AttributeError:
                    print(
                        "No values at (Row" + str(row) + " / " + column + ")."
                    )

    comparison_dict = {k: None for k in comparison_list}
    for key in comparison_dict:
        comparison_dict[key] = [0, 0]  # [counter_moral, counter_them]

    counter_moral_n = 0
    counter_them_n = 0

    tagger = ht.HanoverTagger('morphmodel_ger.pgz')

    # Loop through the rows in the dataframe of moralizing segments
    for morali in moralisierung_list:
        tokenized_sents = nltk.tokenize.word_tokenize(
            morali, language='german')
        tags = tagger.tag_sent(tokenized_sents)
        for tag in tags:
            if tag[1] in comparison_dict.keys():
                comparison_dict[tag[1]][0] += 1
            counter_moral_n += 1

    # Loop through the rows in the dataframe of non-moralizing segments
    for index, row in df_thema.iterrows():
        tokenized_sents = nltk.tokenize.word_tokenize(
            row[0], language='german')
        tags = tagger.tag_sent(tokenized_sents)
        for tag in tags:
            if tag[1] in comparison_dict.keys():
                comparison_dict[tag[1]][1] += 1
            counter_them_n += 1

    results_dict = {k: None for k in comparison_dict.keys()}
    for lemma in results_dict:
        counter_moral_prot = comparison_dict[lemma][0]
        counter_them_prot = comparison_dict[lemma][1]
        likelihood_moral = counter_moral_prot / counter_moral_n
        likelihood_them = counter_them_prot / counter_them_n

        contingency_table = [
            [counter_moral_prot, counter_moral_n - counter_moral_prot],
            [counter_them_prot, counter_them_n - counter_them_prot]
        ]

        res = stats.fisher_exact(contingency_table)

        ratio = None

        try:
            # Compare the likelihoods
            ratio = likelihood_moral / likelihood_them
            diff_coeficient = (
                (likelihood_moral - likelihood_them)
                / (likelihood_moral + likelihood_them)
            )
        except ZeroDivisionError:
            ratio = False

        results_dict[lemma] = {
            "ratio": ratio,
            "diff_co": diff_coeficient,
            "pvalue": res.pvalue
        }

    return results_dict


def compare_pos_likelihood_fulltexts(
    pos_list,
    categories=[0],
    ignore_sheet=[]
):
    """
    This function compares moralizing and non-moralizing segments.
    In particular, it calculates the frequency of 'protagonist' terms
    """

    print("POS LIST: ", str(pos_list))

    # Load the Excel file into a pandas dataframe
    sheet_list = ["Gerichtsurteile", "Interviews", "Kommentare", "Leserbriefe"]
    sheet_list = [sheet for sheet in sheet_list if sheet not in ignore_sheet]

    df_thema = pd.DataFrame()
    moralisierung_list = []

    for sheet in sheet_list:
        # Load the Excel file into a pandas dataframe
        df_neg = pd.read_excel(
            negative_path,
            sheet_name=sheet,
            header=None)
        df_pos = pd.read_excel(
            positive_path,
            sheet_name=sheet,
            header=None)

        dataframe_list = [df_neg, df_pos]

        # Loop through the rows in the dataframe
        for df in dataframe_list:
            for index, row in df.iterrows():
                # Check the value in the second column
                if row[1] in categories:
                    # Add the row to the second dataframe
                    if index % 2 == 1:
                        df_thema = df_thema.append(row)

        # Open the Excel file
        excel_file = pd.ExcelFile(spans_path)

        # Get the sheet you want to read
        df = excel_file.parse('spans_out')

        # Read data
        for column in relev_textsorten_dict[sheet]:
            for row in range(2, 7):
                try:
                    data = df.at[row, column]
                    data_list = data.split(" ### ")

                    # Zuerst Duplikate entfernen
                    moralisierung_list = moralisierung_list + list(
                        set(data_list) - set(moralisierung_list))
                except AttributeError:
                    print("No values @ (Row" + str(row) + " / " + column + ")")

    counter_moral_prot = 0
    counter_moral_n = 0
    counter_them_prot = 0
    counter_them_n = 0

    tagger = ht.HanoverTagger('morphmodel_ger.pgz')

    # Loop through the rows in the dataframe of moralizing segments
    for morali in moralisierung_list:
        tokenized_sents = nltk.tokenize.word_tokenize(
            morali, language='german')
        tags = tagger.tag_sent(tokenized_sents)
        for tag in tags:
            if tag[2] in pos_list:
                counter_moral_prot += 1
            counter_moral_n += 1

    # Loop through the rows in the dataframe of non-moralizing segments
    for index, row in df_thema.iterrows():
        tokenized_sents = nltk.tokenize.word_tokenize(
            row[0], language='german')
        tags = tagger.tag_sent(tokenized_sents)
        for tag in tags:
            if tag[2] in pos_list:
                counter_them_prot += 1
            counter_them_n += 1

    # Calculate the likelihood that a token in a given text type
    # (moralizing vs non-moralizing) is on the list of protagonists
    likelihood_moral = counter_moral_prot / counter_moral_n
    likelihood_them = counter_them_prot / counter_them_n

    contingency_table = [
        [counter_moral_prot, counter_moral_n - counter_moral_prot],
        [counter_them_prot, counter_them_n - counter_them_prot]
    ]

    res = stats.fisher_exact(contingency_table)

    print("\nLIKELIHOOD MORAL (Prozent): ", str(likelihood_moral * 100))
    print("LIKELIHOOD THEM  (Prozent): ", str(likelihood_them * 100))

    ratio = likelihood_moral / likelihood_them
    diff_coeficient = (
        (likelihood_moral - likelihood_them)
        / (likelihood_moral + likelihood_them)
    )

    try:
        # Compare the likelihoods
        print("\nRATIO: ", str(ratio))
        print("DIFF COEFF: ", str(diff_coeficient))
        print("PROBABILITY FISHER: ", str(res.pvalue))
    except ZeroDivisionError:
        print("Error: Division by zero.")

    return 0


def compare_token_likelihood(
    sheet_name,
    comparison_list,
    categories=[0],
):
    """
    This function compares moralizing and non-moralizing segments.
    In particular, it calculates the frequency of 'protagonist' terms
    """

    # Get nonmoral spans from excel sheets
    df_thema = nonmoral_df(sheet_name, categories)
    # Get moralizing spans SSC excel sheets
    moralisierung_list = moral_list(sheet_name)

    counter_moral_prot = 0
    counter_moral_n = 0
    counter_them_prot = 0
    counter_them_n = 0

    # Loop through the rows in the dataframe of moralizing segments
    for morali in moralisierung_list:
        tokenized_sents = nltk.tokenize.word_tokenize(
            morali, language='german')
        tokenized_sents = [x.lower() for x in tokenized_sents]
        for token in tokenized_sents:
            if token in comparison_list:
                counter_moral_prot += 1
            counter_moral_n += 1

    # Loop through the rows in the dataframe of non-moralizing segments
    for index, row in df_thema.iterrows():
        tokenized_sents = nltk.tokenize.word_tokenize(
            row[0], language='german')
        tokenized_sents = [x.lower() for x in tokenized_sents]
        for token in tokenized_sents:
            if token in comparison_list:
                counter_them_prot += 1
            counter_them_n += 1

    # Calculate the likelihood that a token in a given text type
    # (moralizing vs non-moralizing) is on the list of protagonists
    likelihood_moral = counter_moral_prot / counter_moral_n
    likelihood_them = counter_them_prot / counter_them_n

    contingency_table = [
        [counter_moral_prot, counter_moral_n - counter_moral_prot],
        [counter_them_prot, counter_them_n - counter_them_prot]
    ]

    res = stats.fisher_exact(contingency_table)

    print("\nLIKELIHOOD MORAL (Prozent): ", str(likelihood_moral * 100))
    print("LIKELIHOOD THEM  (Prozent): ", str(likelihood_them * 100))

    ratio = likelihood_moral / likelihood_them
    diff_coeficient = (
        (likelihood_moral - likelihood_them)
        / (likelihood_moral + likelihood_them)
    )

    try:
        # Compare the likelihoods
        print("\nRATIO: ", str(ratio))
        print("DIFF COEFF OLD: ", str(diff_coeficient))
        print("PROBABILITY FISHER: ", str(res.pvalue))
    except ZeroDivisionError:
        print("Error: Division by zero.")

    return 0


def compare_token_likelihood_fulltexts(
    comparison_list,
    ignore_sheet=[],
    categories=[0],
):
    """
    This function compares moralizing and non-moralizing segments.
    In particular, it calculates the frequency of 'protagonist' terms
    """

    sheet_list = ["Gerichtsurteile", "Interviews", "Kommentare", "Leserbriefe"]
    sheet_list = [sheet for sheet in sheet_list if sheet not in ignore_sheet]

    df_thema = pd.DataFrame()
    moralisierung_list = []

    for sheet in sheet_list:
        # Load the Excel file into a pandas dataframe
        df_neg = pd.read_excel(
            negative_path,
            sheet_name=sheet,
            header=None)
        df_pos = pd.read_excel(
            positive_path,
            sheet_name=sheet,
            header=None)

        dataframe_list = [df_neg, df_pos]

        # Loop through the rows in the dataframe
        for df in dataframe_list:
            for index, row in df.iterrows():
                # Check the value in the second column
                if row[1] in categories:
                    # Add the row to the second dataframe
                    if index % 2 == 1:
                        df_thema = df_thema.append(row)

        # Open the Excel file
        excel_file = pd.ExcelFile(spans_path)

        # Get the sheet you want to read
        df = excel_file.parse('spans_out')

        # Read data
        for column in relev_textsorten_dict[sheet]:
            for row in range(2, 7):
                try:
                    data = df.at[row, column]
                    data_list = data.split(" ### ")

                    # Zuerst Duplikate entfernen
                    moralisierung_list = moralisierung_list + list(
                        set(data_list) - set(moralisierung_list))
                except AttributeError:
                    print("No values @ (Row" + str(row) + " / " + column + ")")

    counter_moral_prot = 0
    counter_moral_n = 0
    counter_them_prot = 0
    counter_them_n = 0

    # Loop through the rows in the dataframe of moralizing segments
    for morali in moralisierung_list:
        tokenized_sents = nltk.tokenize.word_tokenize(
            morali, language='german')
        tokenized_sents = [x.lower() for x in tokenized_sents]
        for token in tokenized_sents:
            if token in comparison_list:
                counter_moral_prot += 1
            counter_moral_n += 1

    # Loop through the rows in the dataframe of non-moralizing segments
    for index, row in df_thema.iterrows():
        tokenized_sents = nltk.tokenize.word_tokenize(
            row[0], language='german')
        tokenized_sents = [x.lower() for x in tokenized_sents]
        for token in tokenized_sents:
            if token in comparison_list:
                counter_them_prot += 1
            counter_them_n += 1

    # Calculate the likelihood that a token in a given text type
    # (moralizing vs non-moralizing) is on the list of protagonists
    likelihood_moral = counter_moral_prot / counter_moral_n
    likelihood_them = counter_them_prot / counter_them_n

    contingency_table = [
        [counter_moral_prot, counter_moral_n - counter_moral_prot],
        [counter_them_prot, counter_them_n - counter_them_prot]
    ]
    print(contingency_table)

    res = stats.fisher_exact(contingency_table)

    print("\nLIKELIHOOD MORAL (Prozent): ", str(likelihood_moral * 100))
    print("LIKELIHOOD THEM  (Prozent): ", str(likelihood_them * 100))

    ratio = likelihood_moral / likelihood_them
    diff_coeficient = (
        (likelihood_moral - likelihood_them)
        / (likelihood_moral + likelihood_them)
    )

    try:
        # Compare the likelihoods
        print("\nRATIO: ", str(ratio))
        print("DIFF COEFF OLD: ", str(diff_coeficient))
        print("PROBABILITY FISHER: ", str(res.pvalue))
    except ZeroDivisionError:
        print("Error: Division by zero.")

    return 0


def dictdict_to_xlsx(dictionary, filename):

    if filename[-5:] != ".xlsx":
        print("Filename is not an excel file!")
        print(f"The file ending is {filename[-5:]} when it should be .xlsx!")

    # Create a workbook and add a worksheet.
    workbook = xlsxwriter.Workbook(filename)
    worksheet = workbook.add_worksheet()

    # Start from the first cell. Rows and columns are zero indexed.
    row = 0

    # Iterate over the data and write it out row by row.
    for key in dictionary:
        col = 0
        worksheet.write(row, col, key)
        for inner_key in dictionary[key]:
            col += 1
            worksheet.write(row, col, dictionary[key][inner_key])
        row += 1

    workbook.close()


compare_pos_likelihood("Interviews", ["NN"])
