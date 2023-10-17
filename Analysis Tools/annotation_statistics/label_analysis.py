"""
This module includes functions that can be used to perform
analyses on the moralization corpus in an xmi format.

Functions:
    filenames(text_type=None)
    text_from_xmi(filepath)
    list_moralizations_from_xmi(filepath)
    list_protagonists_from_xmi(filepath, ignore_list=[], skip_duplicates=False)
    protagonist_freq_table(moral_spans_list, protagonist_spans_list)
    protagonists_in_context(word_list, filepath, protagonist_list=None)
    highlight_protagonist_count(filepath, count, protagonist_list=None)
    highlight_protagonists(filepath, condition_list=[], protagonist_list=None)
    get_protag_spans_condition(filepath, condition_list)
    double_role_highlight(filepath, protagonist_list=None)
    protagonist_combinations(filepath)
    multi_role_protagonists(file)
    multi_role_combinations(double_role_output)
    combine_dicts(dict_1, dict_2)
"""

import sys
import operator as op
import pandas as pd

sys.path.append("../_utils_")
import xmi_analysis_util as xau


def label_freq_table(moral_spans_list, protagonist_spans_list):
    """
    Returns the distribution of the label 'Protagonist'.

    Parameters:
        moral_spans_list: List of 2-tuples ('Coordinates') which delimit
            moralizing instances in the corpus, as created by the
            list_moralizations_from_xmi() function.
        protagonist_spans_list: List of dictionaries that contain
            annotation data regarding the 'protagonist' label,
            as returned by the list_protagonists_from_xmi() function.
    Returns:
        Frequency table in form of a dictionary, where
            - keys are the number of 'Protagonists' in a span
            - values are their absolute frequencies in the dataset
    """

    # Using a dictionary of moralizing spans,
    # count the number of Protagonists for every span
    moralizations_dict = {}
    for moralization in moral_spans_list:
        moralizations_dict[moralization] = 0
    for protagonist in protagonist_spans_list:
        moral_span = xau.inside_of(
            moral_spans_list, protagonist["Coordinates"])
        if moral_span:
            moralizations_dict[moral_span] += 1

    # Go through the dict of spans, count how often a specific
    # count of Protagonists (e.g. 3 in one moralization) appear in the dataset
    freq_table = {}
    stop_val = max(moralizations_dict.values()) + 1
    for value in range(0, stop_val):
        freq_table[value] = op.countOf(moralizations_dict.values(), value)

    return freq_table


def roles_groups_table(protagonists, language='all'):
    """
    For a given genres, creates a dataframe that shows
    how different label categories are associated.

    Parameters:
        Genre: genre you want the table for
    Returns:
        Pandas dataframe
    """

    data_dict = {
            'Kategorie': [
                "Individuum",
                "Institution",
                "Menschen",
                "soziale Gruppe",
                "Sonstige"
            ],
            'Adresassat:in': [
                0, 0, 0, 0, 0
            ],
            'Benefizient:in': [
                0, 0, 0, 0, 0
            ],
            'Forderer:in': [
                0, 0, 0, 0, 0
            ],
            'Kein Bezug': [
                0, 0, 0, 0, 0
            ],
            'Malefizient:in': [
                0, 0, 0, 0, 0
            ],
            'Bezug unklar': [
                0, 0, 0, 0, 0
            ]
        }

    for protagonist in protagonists:
        rolle = protagonist["Rolle"]
        if protagonist["Gruppe"] == "Individuum":
            data_dict[rolle][0] += 1
        elif protagonist["Gruppe"] == "Institution":
            data_dict[rolle][1] += 1
        elif protagonist["Gruppe"] == "Menschen":
            data_dict[rolle][2] += 1
        elif protagonist["Gruppe"] == "soziale Gruppe":
            data_dict[rolle][3] += 1
        elif protagonist["Gruppe"] == "OTHER":
            data_dict[rolle][4] += 1

    df = pd.DataFrame(data_dict)

    if language.lower() == 'de':
        df.drop('Malefizient:in', axis=1, inplace=True)
        df.drop('Bezug unklar', axis=1, inplace=True)
    elif language.lower() != 'all':
        df.drop('Kein Bezug', axis=1, inplace=True)

    return df


def groups_ownother_table(protagonists):
    """
    For a given genres, creates a dataframe that shows
    how different label categories are associated.

    Parameters:
        Genre: genre you want the table for
    Returns:
        Pandas dataframe
    """

    data_dict = {
            'Kategorie': [
                "Individuum",
                "Institution",
                "Menschen",
                "soziale Gruppe",
                "Sonstige"
            ],
            'Own Group': [
                0, 0, 0, 0, 0
            ],
            'Other Group': [
                0, 0, 0, 0, 0
            ],
            'Neutral': [
                0, 0, 0, 0, 0
            ]
        }

    for protagonist in protagonists:
        ownother = protagonist["own/other"]
        if ownother is None:
            continue
        if protagonist["Gruppe"] == "Individuum":
            data_dict[ownother][0] += 1
        elif protagonist["Gruppe"] == "Institution":
            data_dict[ownother][1] += 1
        elif protagonist["Gruppe"] == "Menschen":
            data_dict[ownother][2] += 1
        elif protagonist["Gruppe"] == "soziale Gruppe":
            data_dict[ownother][3] += 1
        elif protagonist["Gruppe"] == "OTHER":
            data_dict[ownother][4] += 1

    df = pd.DataFrame(data_dict)

    return df


def roles_ownother_table(protagonists, language='all'):
    """
    For a given genres, creates a dataframe that shows
    how different label categories are associated.

    Parameters:
        Genre: genre you want the table for
    Returns:
        Pandas dataframe
    """

    data_dict = {
            'Kategorie': [
                "Adresassat:in",
                "Benefizient:in",
                "Forderer:in",
                "Malefizient:in",
                "Kein Bezug",
                "Bezug unklar"
            ],
            'Own Group': [
                0, 0, 0, 0, 0, 0
            ],
            'Other Group': [
                0, 0, 0, 0, 0, 0
            ],
            'Neutral': [
                0, 0, 0, 0, 0, 0
            ]
        }

    for protagonist in protagonists:
        ownother = protagonist["own/other"]
        if ownother is None:
            continue
        if protagonist["Rolle"] == "Adresassat:in":
            data_dict[ownother][0] += 1
        elif protagonist["Rolle"] == "Benefizient:in":
            data_dict[ownother][1] += 1
        elif protagonist["Rolle"] == "Forderer:in":
            data_dict[ownother][2] += 1
        elif protagonist["Rolle"] == "Malefizient:in":
            data_dict[ownother][3] += 1
        elif protagonist["Rolle"] == "Kein Bezug":
            data_dict[ownother][4] += 1
        elif protagonist["Rolle"] == "Bezug unklar":
            data_dict[ownother][5] += 1

    df = pd.DataFrame(data_dict)

    if language.lower() == 'de':
        df.drop(3, axis=0, inplace=True)
        df.drop(5, axis=0, inplace=True)
    elif language.lower() != 'all':
        df.drop(4, axis=0, inplace=True)
    df.reset_index(drop=True, inplace=True)

    return df


def table_table(corpus, cat1, cat2):
    cat_possibilities = ['obj_morals', 'subj_morals', 'all_morals',
                         'prot_roles', 'prot_groups', 'prot_ownother',
                         'com_functions',
                         'demands']
    cat_trans = ['obj_morals', 'subj_morals', 'all_morals',
                 'protagonists_doubles', 'protagonists', 'protagonists',
                 'com_functions',
                 'all_demands']

    cat1_trans = cat_trans[cat_possibilities.index(cat1)]
    cat2_trans = cat_trans[cat_possibilities.index(cat2)]

    df_tables = pd.DataFrame(index=xau.possible_labels(cat1),
                             columns=xau.possible_labels(cat2))

    associations1 = xau.label_associations_category(
        corpus.moralizations,
        getattr(corpus, cat1_trans)
    )
    associations2 = xau.label_associations_category(
        corpus.moralizations,
        getattr(corpus, cat2_trans)
    )

    for row_label in df_tables.index:
        for col_label in xau.possible_labels(cat2):
            table = xau.freq_table(corpus,
                                   associations1,
                                   associations2,
                                   row_label,
                                   col_label)
            df_tables.loc[row_label, col_label] = table

    return df_tables
