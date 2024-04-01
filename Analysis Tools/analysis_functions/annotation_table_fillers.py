"""
This module contains functions that fill out tables/dataframes
based on annotation data.

Author:
Bruno Brocai (bruno.brocai@gs.uni-heidelberg.de)
University of Heidelberg
Research Projekt "Moralisierungen in verschiedenen Wissensdomänen"
"""

import operator as op
import pandas as pd
import annotation_tables
import _util_ as util


def label_freq_table(moral_spans_list, annotation_list):
    """
    Returns the distribution of an annotation category over the moralizations.

    Parameters:
        moral_spans_list: List of 2-tuples ('Coordinates') which delimit
            moralizing instances in the corpus, as created by the
            list_moralizations_from_xmi() function.
        annotation_list: List of dictionaries that contain
            annotation data.
    Returns:
        Frequency table in form of a dictionary, where
            - keys are all occuring counts of that annotations in moralizations
            - values are the absolute frequencies of those counts in the data
    """

    # Using a dictionary of moralizing spans,
    # count the number of annotations for every span
    moralizations_dict = {}
    for moralization in moral_spans_list:
        moralizations_dict[moralization] = 0
    for annotation in annotation_list:
        moral_span = util.inside_of(
            moral_spans_list, annotation["Coordinates"])
        if moral_span:
            moralizations_dict[moral_span] += 1

    # Go through the dict of spans, count how often a specific
    # count of Protagonists (e.g. 3 in one moralization) appear in the dataset
    freq_table = {}
    stop_val = max(moralizations_dict.values()) + 1
    for value in range(0, stop_val):
        freq_table[value] = op.countOf(moralizations_dict.values(), value)

    return freq_table


def roles_groups_table(protagonists):
    """Creates a table of the distribution of roles and groups of protagonists.

    Parameters:
        protagonists: List of dictionaries that contain
            annotation data.
    Returns:
        A pandas Dataframe.
    """

    df = annotation_tables.get_roles_groups_df()

    for protagonist in protagonists:
        role = protagonist["role"]
        if protagonist["Gruppe"] == "Individuum":
            df.loc[df['Kategorie'] == "Individuum", role] += 1
        elif protagonist["Gruppe"] == "Institution":
            df.loc[df['Kategorie'] == "Institution", role] += 1
        elif protagonist["Gruppe"] == "Menschen":
            df.loc[df['Kategorie'] == "Menschen", role] += 1
        elif protagonist["Gruppe"] == "soziale Gruppe":
            df.loc[df['Kategorie'] == "soziale Gruppe", role] += 1
        elif protagonist["Gruppe"] == "OTHER":
            df.loc[df['Kategorie'] == "Sonstige", role] += 1

    return df


def coocurr_table(corpus, cat1, cat2):
    """
    Creates a table of co-occurrences of two annotation categories.

    Parameters:
        corpus: The corpus object.
        cat1: The first category.
        cat2: The second category.
    Returns:
        A pandas DataFrame with the co-occurrences of the two categories.
        The cells of the df are fourfould tables in the form of 2d lists.
    """

    cat_possibilities = [
        'obj_morals', 'subj_morals', 'all_morals',
        'prot_roles', 'prot_groups', 'prot_ownother',
        'com_functions',
        'demands'
    ]
    cat_trans = [
        'obj_morals', 'subj_morals', 'all_morals',
        'com_functions',
        'protagonists_doubles', 'protagonists', 'protagonists',
        'all_demands'
    ]

    cat1_trans = cat_trans[cat_possibilities.index(cat1)]
    cat2_trans = cat_trans[cat_possibilities.index(cat2)]

    df_tables = pd.DataFrame(
        index=util.possible_labels(cat1),
        columns=util.possible_labels(cat2)
    )

    associations1 = util.label_associations_category(
        corpus.concat_coords("moralizations"),
        corpus.concat_annos_coords(cat1_trans)
    )
    associations2 = util.label_associations_category(
        corpus.concat_coords("moralizations"),
        corpus.concat_annos_coords(cat2_trans)
    )

    for row_label in df_tables.index:
        for col_label in util.possible_labels(cat2):
            table = util.freq_table(
                corpus,
                associations1,
                associations2,
                row_label,
                col_label
            )
            df_tables.loc[row_label, col_label] = table

    return df_tables


def count_moral_values(value_list):
    df = annotation_tables.get_moral_df(False)
    for value in value_list:
        if value['Category'] in df['Moralwert'].values:
            df.loc[df['Moralwert'] == value['Category'], 'Vorkommen'] += 1
    return df


def count_protagonist_roles(protagonist_list):
    df = annotation_tables.get_prot_role_df()
    for protagonist in protagonist_list:
        if protagonist['Rolle'] in df['Rolle'].values:
            df.loc[df['Rolle'] == protagonist['Rolle'], 'Vorkommen'] += 1
    return df


def count_protagonist_groups(protagonist_list):
    df = annotation_tables.get_prot_group_df()
    for protagonist in protagonist_list:
        if protagonist['Gruppe'] in df['Gruppe'].values:
            df.loc[df['Gruppe'] == protagonist['Gruppe'], 'Vorkommen'] += 1
    return df


def count_comfunctions(comfunction_list):
    df = annotation_tables.get_comfunction_df()
    for func in comfunction_list:
        if func['Category'] in df['Kommunikative Funktion'].values:
            df.loc[
                df['Kommunikative Funktion'] == func['Category'],
                'Vorkommen'] += 1
    return df
