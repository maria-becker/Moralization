import sys
import xml.etree.ElementTree as ET
import regex as re
import pandas as pd

sys.path.append("../_utils_")
import corpus_extraction as ce
import xmi_analysis_util as xau


def list_nonmorals_strings_from_xmi(
    filepath,
    metadata_regex,
    rm_duplicates=True
):
    """
    Creates a list of strings from an xmi file that
        1) Are tagged as non-moralizing
        2) Do not match a regex (to avoid corpus metadata in the list)

    Parameters:
        filepath: filepath to xmi file
        metadata_regex: regular expression matching the metadata of the corpus
    Returns:
        List of strings as specified above
    """

    tree = ET.parse(filepath)
    root = tree.getroot()

    span_list = root.findall("{http:///custom.ecore}Span")

    nonmoral_spans_list = []
    for span in span_list:
        test = span.get('KAT1MoralisierendesSegment')

        if test == "Keine Moralisierung":
            coordinates = (int(span.get("begin")), int(span.get("end")))
            if coordinates not in nonmoral_spans_list:
                nonmoral_spans_list.append(coordinates)
            else:
                pass

    corpus_list = []
    corpus_string = ce.text_from_xmi(filepath)
    for span in nonmoral_spans_list:
        text = xau.get_span(corpus_string, span)
        text = re.sub(metadata_regex, '', text)
        corpus_list.append(text)

    if rm_duplicates:
        corpus_list = list(set(corpus_list))

    return corpus_list


def list_moralization_strings_from_xmi(filepath, rm_duplicates=True):
    """
    Takes an xmi file and returns a list with 2-tuples.
    The tuples mark the beginning and ending of spans that were
    categorized as "moralizing speechacts".

    Parameters:
        filepath: The xmi file you want to open.
    Returns:
        List of 2-tuples.
    """

    moral_spans_list = ce.list_moralizations_from_xmi(filepath)

    text = ce.text_from_xmi(filepath)

    corpus_list = []
    for span in moral_spans_list:
        corpus_list.append(ce.get_span(text, span))

    if rm_duplicates:
        corpus_list = list(set(corpus_list))

    return corpus_list


def list_nonmoral_strings_from_xlsx(
    filepath,
    sheet_name,
    categories,
    rm_duplicates=True
):
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
    Mostly depricated. Uses output of old SSC code as input.
    Reads an excel file which lists all spans annotated as 'moralization'.
    Returns the sentences annotated that way as a list of strings.

    Parameters:
        sheet_name: genre string, e.g. "Gerichtsurteile"
    Returns:
        list of strings which were annotated as moralizations.
    """

    print("".join(("Warning: Use list_moralization__strings_from_xmi() ",
                   "instead of list_moral_from_xlsx() if possible.")))

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

    moral_texts = []
    for column in textsorten_dict[sheet_name]:
        for row in range(2, 7):
            try:
                data = df.at[row, column]
                new_data_list = data.split(" ### ")
                moral_texts = moral_texts + new_data_list
            except AttributeError:
                print("No spans at (Row" + str(row) + " / " + column + ").")

    if rm_duplicates:
        moral_texts = list(set(moral_texts))

    return moral_texts
