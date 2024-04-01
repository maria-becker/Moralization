"""
This module allows one to retrieve sentences that were tagged a certain way
(moralizing or not) for a given subcorpus.

Author:
Bruno Brocai (bruno.brocai@gs.uni-heidelberg.de)
University of Heidelberg
Research Projekt "Moralisierungen in verschiedenen Wissensdomänen"
"""


import pandas as pd
from . import _util_ as util


def list_moral_strings_from_subcorpus(
    subcorpus
):
    """
    Creates a list of all passages marked as moralizing in a subcorpus.

    Args:
        subcorpus (Subcorpus): subcorpus object, representing an xmi file

    Returns:
        list: A list of strings that were marked as moralizing.
    """

    moralizations = []
    for span in subcorpus.moralizations:
        moralizations.append(util.get_span(subcorpus.text, span))

    corpus_list = list(set(moralizations))

    return corpus_list


def list_nonmoral_strings_from_xlsx(
    filepath,
    sheet_name,
    categories=None,
):
    """
    Creates a list which includes spans of the categories specified.

    Args:
        filepath (str): path to the xlsx file
        sheet_name (str): genre string, e.g. "Gerichtsurteile"
        categories (list of ints): 0, 1, 2, 3 like in the sheets

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
