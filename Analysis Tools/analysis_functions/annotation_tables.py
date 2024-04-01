"""
This utility module just contains functions that return
different types of dataframes with hardcoded values
based on the annotation manual.

Author:
Bruno Brocai (bruno.brocai@gs.uni-heidelberg.de)
University of Heidelberg
Research Projekt "Moralisierungen in verschiedenen Wissensdomänen"
"""


import pandas as pd


def get_moral_df(sum_dimensions):
    """Creates a dataframe with all possible moral value types.

    Args:
        sum_dimensions (bool): If True, the two ends of each moral
            value dimension is summed in one column.

    Returns:
        pd.DataFrame: A dataframe with the columns 'Moralwert' and 'Vorkommen'.
    """

    if sum_dimensions:
        df = {
            'Moralwert': [
                'Care/harm',
                'Fairness/cheating',
                'Loyalty/betrayal',
                'Authority/subversion',
                'Sanctity/degradation',
                'Liberty/oppression',
                'OTHER',
            ],
            'Vorkommen': [
                0, 0, 0, 0, 0, 0, 0
            ]
        }
    else:
        df = {
            'Moralwert': [
                'Care',
                'Harm',
                'Fairness',
                'Cheating',
                'Loyalty',
                'Betrayal',
                'Authority',
                'Subversion',
                'Sanctity',
                'Degradation',
                'Liberty',
                'Oppression',
                'OTHER',
            ],
            'Vorkommen': [
                0, 0, 0, 0, 0, 0, 0,
                0, 0, 0, 0, 0, 0
            ]
        }
    df = pd.DataFrame(df)

    return df


def get_prot_role_df():
    """Creates a dataframe with all possible protagonist roles.

    Returns:
        pd.DataFrame: A dataframe with the columns 'Rolle' and 'Vorkommen'.
    """

    df = {
        'Rolle': [
            'Adressat:in',
            'Benefizient:in',
            'Forderer:in',
            'Malefizient:in',
            'Kein Bezug',
            'Bezug unklar',
        ],
        'Vorkommen': [
            0, 0, 0, 0, 0, 0
        ]
    }
    df = pd.DataFrame(df)

    return df


def get_prot_group_df():
    """Creates a dataframe with all possible protagonist groups.

    Returns:
        pd.DataFrame: A dataframe with the columns 'Gruppe' and 'Vorkommen'.
    """

    df = {
        'Gruppe': [
            'Individuum',
            'Institution',
            'Menschen',
            'soziale Gruppe',
            'OTHER',
        ],
        'Vorkommen': [
            0, 0, 0, 0, 0
        ]
    }
    df = pd.DataFrame(df)

    return df


def get_comfunction_df():
    """Creates a dataframe with all possible communicative functions.

    Returns:
        pd.DataFrame: A dataframe with the columns 'Kommunikative Funktion'
        and 'Vorkommen'.
    """

    df = {
        'Kommunikative Funktion': [
            'Appell',
            'Beziehung',
            'Darstellung',
            'Expression',
            'Appell+Beziehung',
            'Appell+Darstellung',
            'Appell+Expression',
        ],
        'Vorkommen': [
            0, 0, 0, 0, 0, 0, 0
        ]
    }
    df = pd.DataFrame(df)

    return df


def get_demand_df():
    """Creates a dataframe with all possible demand types.

    Returns:
        pd.DataFrame: A dataframe with the columns 'Forderungstyp'
        and 'Vorkommen'.
    """

    df = {
        'Forderungstyp': [
            'Explizite Forderung',
            'Implizite Forderung',
        ],
        'Vorkommen': [
            0, 0
        ]
    }
    df = pd.DataFrame(df)

    return df


def get_roles_groups_df():
    """Creates a dataframe with all possible combinations of
    protagonist roles and groups.

    Returns:
        pd.DataFrame: A dataframe with the columns 'Kategorie',
        'Adresassat:in', 'Benefizient:in', 'Forderer:in',
    """

    df_full = {
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
    df_full = pd.DataFrame(df_full)

    return df_full
