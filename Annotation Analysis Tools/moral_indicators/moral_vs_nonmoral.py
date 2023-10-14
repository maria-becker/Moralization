import pandas as pd
from HanTa import HanoverTagger as ht
import nltk
import scipy.stats as stats
import xlsxwriter
import xml.etree.ElementTree as ET


def list_nonmoral(filepath, sheet_name, categories, rm_duplicates=True):
    """
    Creates a list which includes spans of the categories specified.

    Parameters:
        sheet_name: genre string, e.g. "Gerichtsurteile"
        categories: 0, 1, 2, 3 like in the sheets
    Returns:
        List that has all the spans from the genre and category specified.
    """

    # Load the Excel file into a pandas dataframe
    source_df = pd.read_excel(
        filepath,
        sheet_name=sheet_name,
        header=None)

    nonmoral_texts = []

    # Loop through the rows in the dataframe
    for index, row in source_df.iterrows():
        # Check the value in the second column
        if row[1] in categories and index % 2 == 1:
            nonmoral_texts.append(row[0])

    if rm_duplicates:
        nonmoral_texts = list(set(nonmoral_texts))

    return nonmoral_texts


def list_moral_from_xlsx(filepath, sheet_name, rm_duplicates=True):
    """
    Reads an excel file which lists all spans annotated as 'moralization'.
    Returns the sentences annotated that way as a list of strings.

    Parameters:
        sheet_name: genre string, e.g. "Gerichtsurteile"
    Returns:
        list of strings which were annotated as moralizations.
    """

    excel_file = pd.ExcelFile(filepath)
    df = excel_file.parse('spans_out')

    textsorten_dict = {
        "Leserbriefe": ["Column4", "Column13"],
        "Interviews": ["Column12", "Column5"],
        "Gerichtsurteile": ["Column8", "Column10"],
        "Kommentare": ["Column14", "Column11"],
        "Plenarprotokolle": ["Column6", "Column7"],
        "Sachbücher": ["Column3"]
    }

    # Read data
    moral_texts = []
    for column in textsorten_dict[sheet_name]:
        for row in range(2, 7):
            try:
                data = df.at[row, column]
                new_data_list = data.split(" ### ")
                # Remove duplicates
                moral_texts = moral_texts + new_data_list
            except AttributeError:
                print("No spans at (Row" + str(row) + " / " + column + ").")

    if rm_duplicates:
        moral_texts = list(set(moral_texts))    

    return moral_texts


def get_span(text, coordinates):
    try:
        span = text[coordinates[0]:(coordinates[1])]
        return span
    except TypeError:
        print("Error getting span.")
        return None


def text_from_xmi(filepath):
    """
    Extracts from the xmi the corpus that the annotations are based on.
    It is necessary to call this function if you want to output
    annotated text at some point.

    Parameters:
        filepath: The xmi file you want to open.
    Returns:
        The corpus as a string
    """

    # Open the XMI file
    tree = ET.parse(filepath)
    root = tree.getroot()

    text = root.find("{http:///uima/cas.ecore}Sofa").get('sofaString')

    return text


def list_moralizations_from_xmi(filepath, rm_duplicates):
    """
    Takes an xmi file and returns a list with 2-tuples.
    The tuples mark the beginning and ending of spans that were
    categorized as "moralizing speechacts".

    Parameters:
        filepath: The xmi file you want to open.
    Returns:
        List of 2-tuples.
    """

    # Open the XMI file
    tree = ET.parse(filepath)
    root = tree.getroot()

    span_list = root.findall("{http:///custom.ecore}Span")

    # Get all moralizing instances
    moral_spans_list = []
    for span in span_list:
        test = span.get('KAT1MoralisierendesSegment')

        if test:
            if test != "Keine Moralisierung":
                coordinates = (int(span.get("begin")), int(span.get("end")))
                moral_spans_list.append(coordinates)

    text = text_from_xmi(filepath)

    moral_texts = []
    for span in moral_spans_list:
        moral_texts.append(get_span(text, span))

    if rm_duplicates:
        moral_texts = list(set(moral_texts))

    return moral_texts


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


def get_stats(
        counter_moral_prot,
        counter_moral_n,
        counter_them_prot,
        counter_them_n
):

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

        ratio = (
            likelihood_moral
            / likelihood_them
        )
        diff_coeficient = (
            (likelihood_moral - likelihood_them)
            / (likelihood_moral + likelihood_them)
        )

        statistics = {
            "likelihood_moral": likelihood_moral,
            "likelihood_nonmoral": likelihood_them,
            "ratio": ratio,
            "diff_coeficient": diff_coeficient,
            "pvalue_fisher": res.pvalue,
            "contingency_table": contingency_table
        }

        return statistics

    except ZeroDivisionError:
        print("Error: Division by zero.")
        return None


def count_instances_lemma(
    text_list,
    lemmata_list,
    combined_mode,
    language='german',
):

    comparison_dict = {lemma: 0 for lemma in lemmata_list}
    comparison_dict["_total_"] = 0

    tagger = ht.HanoverTagger('morphmodel_ger.pgz')

    # Loop through the rows in the dataframe of moralizing segments
    for doc in text_list:
        tokenized_sents = nltk.tokenize.word_tokenize(
            doc, language=language)
        tags = tagger.tag_sent(tokenized_sents)
        for tag in tags:
            comparison_dict["_total_"] += 1
            if tag[1] in comparison_dict.keys():
                comparison_dict[tag[1]] += 1

    if combined_mode:
        combined_dict = {
            "_total_": comparison_dict.pop("_total_")
        }
        combined_dict[tuple(lemmata_list)] = sum(comparison_dict.values())
        return combined_dict

    return comparison_dict


def count_instances_pos(
    text_list,
    pos_list,
    combined_mode,
    language='german',
):

    comparison_dict = {pos: 0 for pos in pos_list}
    comparison_dict["_total_"] = 0

    tagger = ht.HanoverTagger('morphmodel_ger.pgz')

    # Loop through the rows in the dataframe of moralizing segments
    for doc in text_list:
        tokenized_sents = nltk.tokenize.word_tokenize(
            doc, language=language)
        tags = tagger.tag_sent(tokenized_sents)
        for tag in tags:
            comparison_dict["_total_"] += 1
            if tag[2] in comparison_dict.keys():
                comparison_dict[tag[2]] += 1

    if combined_mode:
        combined_dict = {
            "_total_": comparison_dict.pop("_total_")
        }
        combined_dict[tuple(pos_list)] = sum(comparison_dict.values())
        return combined_dict

    return comparison_dict


def count_instances_token(
    text_list,
    token_list,
    combined_mode,
    language='german',
):

    comparison_dict = {token: 0 for token in token_list}
    comparison_dict["_total_"] = 0

    tagger = ht.HanoverTagger('morphmodel_ger.pgz')

    # Loop through the rows in the dataframe of moralizing segments
    for doc in text_list:
        tokenized_sents = nltk.tokenize.word_tokenize(
            doc, language=language)
        lower_sents = [word.lower() for word in tokenized_sents]
        for word in lower_sents:
            comparison_dict["_total_"] += 1
            if word in comparison_dict.keys():
                comparison_dict[word] += 1

    if combined_mode:
        combined_dict = {
            "_total_": comparison_dict.pop("_total_")
        }
        combined_dict[tuple(token_list)] = sum(comparison_dict.values())
        return combined_dict

    return comparison_dict


def compare_lemma_likelihood(
    moral_list,
    nonmoral_list,
    lemmata,
    language="german"
):
    """
    This function compares moralizing and non-moralizing segments.
    In particular, it calculates the frequency of 'protagonist' terms
    """

    moral_counts = count_instances_lemma(
        moral_list,
        lemmata,
        combined_mode=True,
        language=language,
    )
    nonmoral_counts = count_instances_lemma(
        nonmoral_list,
        lemmata,
        combined_mode=True,
        language=language
    )

    results = get_stats(
        moral_counts[tuple(lemmata)],
        moral_counts["_total_"],
        nonmoral_counts[tuple(lemmata)],
        nonmoral_counts["_total_"]
    )

    for stat, value in results.items():
        print(stat, value)

    return results


def compare_pos_likelihood(
    moral_list,
    nonmoral_list,
    pos_list,
    language='german'
):
    """
    This function compares moralizing and non-moralizing segments.
    In particular, it calculates the frequency of 'protagonist' terms
    """

    moral_counts = count_instances_pos(
        moral_list,
        pos_list,
        combined_mode=True,
        language=language,
    )
    nonmoral_counts = count_instances_pos(
        nonmoral_list,
        pos_list,
        combined_mode=True,
        language=language
    )

    results = get_stats(
        moral_counts[tuple(pos_list)],
        moral_counts["_total_"],
        nonmoral_counts[tuple(pos_list)],
        nonmoral_counts["_total_"],
    )

    for stat, value in results.items():
        print(stat, value)

    return results


def compare_token_likelihood(
    moral_list,
    nonmoral_list,
    token_list,
    language='german'
):
    """
    This function compares moralizing and non-moralizing segments.
    In particular, it calculates the frequency of 'protagonist' terms
    """

    moral_counts = count_instances_token(
        moral_list,
        token_list,
        combined_mode=True,
        language=language,
    )
    nonmoral_counts = count_instances_token(
        nonmoral_list,
        token_list,
        combined_mode=True,
        language=language
    )

    results = get_stats(
        moral_counts[tuple(token_list)],
        moral_counts["_total_"],
        nonmoral_counts[tuple(token_list)],
        nonmoral_counts["_total_"],
    )

    for stat, value in results.items():
        print(stat, value)

    return results


def compare_lemma_likelihood_dict(
    moral_list,
    nonmoral_list,
    lemmata,
    language="german"
):
    """
    This function compares moralizing and non-moralizing segments.
    In particular, it calculates the frequency of 'protagonist' terms
    """

    moral_counts = count_instances_lemma(
        moral_list,
        lemmata,
        combined_mode=False,
        language=language,
    )
    nonmoral_counts = count_instances_lemma(
        nonmoral_list,
        lemmata,
        combined_mode=False,
        language=language
    )

    results_dict = {}
    for lemma in lemmata:
        results_dict[lemma] = get_stats(
            moral_counts[lemma],
            moral_counts["_total_"],
            nonmoral_counts[lemma],
            nonmoral_counts["_total_"]
        )

    return results_dict


def compare_pos_likelihood_dict(
    moral_list,
    nonmoral_list,
    pos_list,
    language="german"
):
    """
    This function compares moralizing and non-moralizing segments.
    In particular, it calculates the frequency of 'protagonist' terms
    """

    moral_counts = count_instances_pos(
        moral_list,
        pos_list,
        combined_mode=False,
        language=language,
    )
    nonmoral_counts = count_instances_pos(
        nonmoral_list,
        pos_list,
        combined_mode=False,
        language=language
    )

    results_dict = {}
    for pos in pos_list:
        results_dict[pos] = get_stats(
            moral_counts[pos],
            moral_counts["_total_"],
            nonmoral_counts[pos],
            nonmoral_counts["_total_"]
        )

    return results_dict


def compare_token_likelihood_dict(
    moral_list,
    nonmoral_list,
    token_list,
    language='german'
):
    """
    This function compares moralizing and non-moralizing segments.
    In particular, it calculates the frequency of 'protagonist' terms
    """

    moral_counts = count_instances_token(
        moral_list,
        token_list,
        combined_mode=False,
        language=language,
    )
    nonmoral_counts = count_instances_token(
        nonmoral_list,
        token_list,
        combined_mode=False,
        language=language
    )

    results_dict = {}
    for token in token_list:
        results_dict[token] = get_stats(
            moral_counts[token],
            moral_counts["_total_"],
            nonmoral_counts[token],
            nonmoral_counts["_total_"]
        )

    return results_dict


def dict_to_xlsx(dictionary, filename):

    if filename[-5:] != ".xlsx":
        print("Filename is not an excel file!")
        print(f"The file ending is {filename[-5:]} when it should be .xlsx!")

    # Create a workbook and add a worksheet.
    workbook = xlsxwriter.Workbook(filename)
    worksheet = workbook.add_worksheet()

    # Write header row
    bold = workbook.add_format({'bold': True})
    row = 0
    col = 1
    for key in next(iter(dictionary.values())):
        worksheet.write(row, col, key, bold)
        col += 1

    # Iterate over the data and write it out row by row.
    row = 1
    for key, statistics in dictionary.items():
        col = 0
        worksheet.write(row, col, key)
        for stat, value in statistics.items():
            col += 1
            try:
                worksheet.write(row, col, value)
            except TypeError:
                worksheet.write(row, col, str(value))
        row += 1

    workbook.close()

