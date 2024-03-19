import pandas as pd


def get_moral_df(sum_dimensions):
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
                'Summe'
            ],
            'Vorkommen': [
                0, 0, 0, 0, 0, 0, 0, 0
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
                'Summe'
            ],
            'Vorkommen': [
                0, 0, 0, 0, 0, 0, 0,
                0, 0, 0, 0, 0, 0, 0
            ]
        }
    df = pd.DataFrame(df)

    return df


def get_prot_role_df():
    df = {
        'Rolle': [
            'Adresassat:in',
            'Benefizient:in',
            'Forderer:in',
            'Malefizient:in',
            'Kein Bezug',
            'Bezug unklar',
            'Bezug unklar/kein Bezug',
            'Summe'
        ],
        'Vorkommen': [
            0, 0, 0, 0, 0, 0, 0, 0
        ]
    }
    df = pd.DataFrame(df)

    return df


def get_prot_group_df():
    df = {
        'Gruppe': [
            'Individuum',
            'Institution',
            'Menschen',
            'soziale Gruppe',
            'OTHER',
            'Summe'
        ],
        'Vorkommen': [
            0, 0, 0, 0, 0, 0
        ]
    }
    df = pd.DataFrame(df)

    return df


def get_comfunction_df():

    df = {
        'Kommunikative Funktion': [
            'Appell',
            'Beziehung',
            'Darstellung',
            'Expression',
            'Appell+Beziehung',
            'Appell+Darstellung',
            'Appell+Expression',
            'Summe'
        ],
        'Vorkommen': [
            0, 0, 0, 0, 0, 0, 0, 0
        ]
    }
    df = pd.DataFrame(df)

    return df


def get_demand_df():
    df = {
        'Forderungstyp': [
            'Explizite Forderung',
            'Implizite Forderung',
            'Summe'
        ],
        'Vorkommen': [
            0, 0, 0
        ]
    }
    df = pd.DataFrame(df)

    return df


def get_roles_groups_df():
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
