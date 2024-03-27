import sys
import xml.etree.ElementTree as ET
import regex as re
import pandas as pd

sys.path.append("../_utils_")
import corpus_extraction as ce
import xmi_analysis_util as xau


def list_moral_strings_from_subcorpus(
    subcorpus
):
    """
    Takes an xmi file and returns a list with 2-tuples.
    The tuples mark the beginning and ending of spans that were
    categorized as "moralizing speechacts".

    Parameters:
        filepath: The xmi file you want to open.
    Returns:
        List of 2-tuples.
    """

    moralizations = []
    for span in subcorpus.moralizations:
        moralizations.append(xau.get_span(subcorpus.text, span))

    corpus_list = list(set(moralizations))

    return corpus_list


def list_nonmoral_strings_from_xlsx(
    filepath,
    sheet_name,
    categories=None,
):
    """
    Creates a list which includes spans of the categories specified.

    Parameters:
        sheet_name: genre string, e.g. "Gerichtsurteile"
        categories: 0, 1, 2, 3 like in the sheets
    Returns:
        List that has all the spans from the genre and category specified.
    """

    if categories is None:
        categories = [0, 1, 2]

    # Load the Excel file into a pandas dataframe
    source_df = pd.read_excel(
        filepath,
        sheet_name=sheet_name,
        header=None
    )

    nonmoral_texts = []

    # Loop through the rows in the dataframe
    for index, row in source_df.iterrows():
        # Check the value in the second column
        if row[1] in categories and index % 2 == 1:
            nonmoral_texts.append(row[0])

    nonmoral_texts = list(set(nonmoral_texts))

    return nonmoral_texts
