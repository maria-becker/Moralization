"""Excel Data Preparation for Binary Classifier

This module contains functions that allow one to retrieve annotated spans
from an Excel file, map annotations onto corresponding sentences,
remove duplicates and standarize the data.

The data is assumed to be in the format used by the Moralization Project
@ University of Heidelberg; see here:
https://github.com/maria-becker/Moralization

Author: Bruno Brocai
"""


import pandas as pd
from nltk.tokenize import sent_tokenize
import _util_ as util


def list_strings_from_xlsx_old(
    filepath,
    sheet_name,
    categories,
):
    """
    Creates a list which includes spans of the categories specified.
    This works for Excel files in the old format - in other words,
    where all even rows contain metadata and all odd rows contain
    text spans.


    Args:
        filepath (str): path to excel file
        sheet_name (str): name of the excel sheet
        categories (list): list of integers representing annotation categories
            that you want to retrieve; e.g. [0] to retrieve thematizations

    Returns:
        list: list of strings that were annotated in the specified categories
    """

    # Load the Excel file into a pandas dataframe
    source_df = pd.read_excel(
        filepath,
        sheet_name=sheet_name,
        header=None
    )

    retrieved_spans = []

    # Loop through the rows in the dataframe
    for index, row in source_df.iterrows():

        # Check the value in the second column
        if row[1] in categories and index % 2 == 1:
            retrieved_spans.append(row[0])

    return retrieved_spans


def list_strings_from_xlsx_new(
    filepath,
    sheet_name,
    categories,
    metadata_loc,
):
    """
    Creates a list which includes spans of the categories specified.
    This works for Excel files in the new format - in other words,
    where all rows contain both metadata and the text span.

    Args:
        filepath (str): path to excel file
        sheet_name (str): name of the excel sheet
        categories (list): list of integers representing annotation categories
            that you want to retrieve; e.g. [0] to retrieve thematizations
        metadata_loc (str): For now, either "col_0" or "before_text".
            Specifies where the metadata is to be found. This is different
            depending on the excel format used as input.

    Returns:
        list: list of strings that were annotated in the specified categories
    """

    # Load the Excel file into a pandas dataframe
    source_df = pd.read_excel(
        filepath,
        sheet_name=sheet_name,
        header=None
    )

    retrieved_spans = []

    if metadata_loc == "col_0":
        annotation_col = 2
        rm_metadata = False
    elif metadata_loc == "before_text":
        annotation_col = 1
        rm_metadata = True
    else:
        raise ValueError(
            "Metadata_loc must be one of 'col_0' or 'before_text'."
        )

    # Loop through the rows in the dataframe
    for index, row in source_df.iterrows():

        # Check the value in the relevant column
        if row[annotation_col] in categories:
            span = row[annotation_col-1]

            # Cut metadata if included in the span
            if rm_metadata:
                span = span.split('###')
                try:
                    span = span[1]
                except IndexError:
                    print(f"No (properly formatted) metadata in row {index}.")

            retrieved_spans.append(span)

    return retrieved_spans


def annotate_nonmoral_strings(string_list, genre_nbr):
    """
    Given a list of spans classified as nonmoralizing (meaning all sentences
    are nonmoralizing), transforms them into the desired output format.

    Args:
        string_list (str): list of spans
        genre_nbr (int): number associated with the genre of the spans
            (cf. _util_)

    Returns:
        list: 3d array with info data from the xmi of shape [
            [
                genre_nbr(int),
                [
                    'sentence1'(str),
                    'sentence2'(str)
                ],
                moralization_in_span?(bool - always False),
                [
                    moralization_in_sent1?(bool - always False),
                    moralization_in_sent2?(bool - always false)
                ]
            ]
        ]
    """

    mappings = []
    for span in string_list:
        sentences = sent_tokenize(span)
        sentences = util.clean_sentences(sentences)
        annotations = [
            genre_nbr,
            sentences,
            0,
            [0] * len(sentences)
        ]
        mappings.append(annotations)

    return mappings


def annotate_moral_strings(string_list, genre_nbr):
    """
    Given a list of spans classified as moralizing (given that
    we are working with excel, were indiviual sentences are not annotated,
    we will assume all sentences are moralizing),
    transforms them into the desired output format.

    Args:
        string_list (str): list of spans
        genre_nbr (int): number associated with the genre of the spans
            (cf. _util_)

    Returns:
        list: 3d array with info data from the xmi of shape [
            [
                genre_nbr(int),
                [
                    'sentence1'(str),
                    'sentence2'(str)
                ],
                moralization_in_span?(bool - always True),
                [
                    moralization_in_sent1?(bool - always True),
                    moralization_in_sent2?(bool - always True)
                ]
            ]
        ]
    """

    mappings = []
    for span in string_list:
        sentences = sent_tokenize(span)
        sentences = util.clean_sentences(sentences)
        annotations = [
            genre_nbr,
            sentences,
            1,
            [1] * len(sentences)
        ]
        mappings.append(annotations)

    return mappings


def get_mappings_old(
    filepath,
    sheetname,
    categories,
    genre=None
):
    """
    Performs all necessary steps to create a list of annotation data
    given a filepath and (optionally) a genre number.
    This works for Excel files in the old format - in other words,
    where all even rows contain metadata and all odd rows contain
    text spans.

    Args:
        filepath (str): Path to the excel file
        sheetname (str): Excel-Sheet to be used
        categories (list): list of integers representing annotation categories
            that you want to retrieve; e.g. [0] to retrieve thematizations
        genre (int, optional): Int associated with genre of the subcorpus.
            Defaults to check the sheetname for corpus info.

    Raises:
        ValueError: The function can only handle nonmoralizing
            categories (0, 1, 2) or moralizations (3) at a time.
            Attempting to handle both, e.g. by passing a list
            such as [0, 3], will raise this error.

    Returns:
        list: 3d array with info data from the xmi of shape [
            [
                genre_nbr(int),
                ['sentence1'(str), 'sentence2'(str)],
                moralization_in_span?(bool),
                [moralization_in_sent1?(bool), moralization_in_sent2?(bool)]
            ]
        ]
    """

    if genre is None:
        genre = util.genre_labels(sheetname)

    strings = list_strings_from_xlsx_old(filepath,
                                         sheetname,
                                         categories)
    if 3 not in categories:
        mappings = annotate_nonmoral_strings(strings, genre)
    elif [3] == categories:
        mappings = annotate_moral_strings(strings, genre)
    else:
        raise ValueError(("This function cannot handle the list of categories"
                          " provided. Consider handling moralizations "
                          "and non-moralizing spans differntly."))

    mappings = util.remove_doubles(mappings)

    return mappings


def get_mappings_new(
    filepath,
    sheetname,
    categories,
    metadata_loc,
    genre=None
):
    """
    Performs all necessary steps to create a list of annotation data
    given a filepath and (optionally) a genre number.
    This works for Excel files in the new format - in other words,
    where all rows contain both metadata and the text span.

    Args:
        filepath (str): Path to the excel file
        sheetname (str): Excel-Sheet to be used
        categories (list): list of integers representing annotation categories
            that you want to retrieve; e.g. [0] to retrieve thematizations
        genre (int, optional): Int associated with genre of the subcorpus.
            Defaults to check the sheetname for corpus info.

    Raises:
        ValueError: The function can only handle nonmoralizing
            categories (0, 1, 2) or moralizations (3) at a time.
            Attempting to handle both, e.g. by passing a list
            such as [0, 3], will raise this error.

    Returns:
        list: 3d array with info data from the xmi of shape [
            [
                genre_nbr(int),
                ['sentence1'(str), 'sentence2'(str)],
                moralization_in_span?(bool),
                [moralization_in_sent1?(bool), moralization_in_sent2?(bool)]
            ]
        ]
    """

    if genre is None:
        genre = util.genre_labels(sheetname)

    strings = list_strings_from_xlsx_new(filepath,
                                         sheetname,
                                         categories,
                                         metadata_loc)
    if 3 not in categories:
        mappings = annotate_nonmoral_strings(strings, genre)
    elif [3] == categories:
        mappings = annotate_moral_strings(strings, genre)
    else:
        raise ValueError(("This function cannot handle the list of categories"
                          " provided. Consider handling moralizations "
                          "and non-moralizing spans differntly."))

    mappings = util.remove_doubles(mappings)

    return mappings
