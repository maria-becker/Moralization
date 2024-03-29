import sys
import contextlib
import label_analysis as la
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator
import scipy.stats as stats
import annotation_stats_single as astats

sys.path.append("../_utils_")
import xmi_analysis_util as xau


def moral_values_freq_collection(corpus_collection,
                                 moral_type="all",
                                 sum_dimensions=False,
                                 plot=False,
                                 export=False):
    """
    Creates a Pandas dataframe with the counts of moral values (based on MFT)
    in a CorpusCollection object (i.e. in all subcorpora).

    Parameters:
        - corpus_collection: CorpusCollection object
        - moral_type: str - valid options are:
                            obj: concrete moral values
                            subj: subjective moral expressions
                            all: both of the above
        - sum_dimensions: bool. If true, the two sides of moral dimensions
                          according to MFT (e.g. Care/Harm) are summed into one row.
        - plot: bool. If true, output a plot of the results
        - export: bool. If true, store results in a csv file.
    Returns:
        - Pandas dataframe as described above.
    """

    if moral_type not in ['all', 'subj', 'obj']:
        print("Error: Moral_type parameter must be 'all', 'obj', or 'subj'.")
        return

    df = None
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

    for corpus in corpus_collection.collection.values():
        # Surpress print statements in function
        with contextlib.redirect_stdout(None):
            sub_df = astats.moral_values_freq(corpus,
                                              moral_type,
                                              sum_dimensions)
        df['Vorkommen'] = df['Vorkommen'].add(sub_df['Vorkommen'],
                                              axis='index')

    if plot:
        df_nosum = df[df['Moralwert'] != 'Summe']
        plt.bar(df_nosum['Moralwert'], df_nosum['Vorkommen'])
        plt.xlabel('Moralwert', fontstyle='italic')
        plt.ylabel('Vorkommen', fontstyle='italic')
        plt.title('Frequenz Moralwerte')
        plt.xticks(rotation=45)
        ax = plt.gca()
        ax.yaxis.set_major_locator(MaxNLocator(integer=True))
        plt.tight_layout()
        plt.show()
    if export:
        df.to_csv("protagonist_role_freq_collection.csv",
                  index=False, decimal=',')

    return df


def protagonist_role_freq_collection(corpus_collection,
                                     plot=False,
                                     export=False):
    """
    Creates a Pandas dataframe with the counts of the roles
    of the protagonists in a CorpusCollection object (i.e. in all subcorpora).

    Parameters:
        - corpus_collection: CorpusCollection object
        - plot: bool. If true, output a plot of the results
        - export: bool. If true, store results in a csv file.
    Returns:
        - Pandas dataframe as described above.
    """

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

    for corpus in corpus_collection.collection.values():
        for protagonist in corpus.protagonists_doubles:
            if protagonist['Rolle'] in df['Rolle'].values:
                df.loc[df['Rolle'] == protagonist['Rolle'], 'Vorkommen'] += 1

    if corpus_collection.language.lower() == 'all':
        df.at[7, 'Vorkommen'] = df['Vorkommen'].sum()
        df.at[6, 'Vorkommen'] = df.at[4, 'Vorkommen'] + df.at[5, 'Vorkommen']
        df = df.drop(4)
        df = df.drop(5)
    elif corpus_collection.language.lower() == 'de':
        df = df.drop(3)
        df = df.drop(5)
        df = df.drop(6)
    else:
        df = df.drop(4)
        df = df.drop(6)

    if plot:
        df_nosum = df[df['Rolle'] != 'Summe']
        plt.bar(df_nosum['Rolle'], df_nosum['Vorkommen'])
        plt.xlabel('Rolle', fontstyle='italic')
        plt.ylabel('Vorkommen', fontstyle='italic')
        plt.title('Frequenz Rollen')
        plt.xticks(rotation=45)
        ax = plt.gca()
        ax.yaxis.set_major_locator(MaxNLocator(integer=True))
        plt.tight_layout()
        plt.show()
    if export:
        df.to_csv("protagonist_role_freq_collection.csv",
                  index=False, decimal=',')

    return df


def protagonist_group_freq_collection(corpus_collection,
                                      plot=False,
                                      export=False):
    """
    Creates a Pandas dataframe with the counts of the group categories
    of the protagonists in a CorpusCollection object (i.e. in all subcorpora).

    Parameters:
        - corpus_collection: CorpusCollection object
        - plot: bool. If true, output a plot of the results
        - export: bool. If true, store results in a csv file.
    Returns:
        - Pandas dataframe as described above.
    """

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

    for corpus in corpus_collection.collection.values():
        # Surpress print statements in function
        with contextlib.redirect_stdout(None):
            sub_df = astats.protagonist_group_freq(corpus)
        df['Vorkommen'] = df['Vorkommen'].add(sub_df['Vorkommen'],
                                              axis='index')

    df['Anteil'] = (df['Vorkommen'] / df['Vorkommen'][5])

    if plot:
        df_nosum = df[df['Gruppe'] != 'Summe']
        plt.bar(df_nosum['Gruppe'], df_nosum['Vorkommen'])
        plt.xlabel('Gruppe', fontstyle='italic')
        plt.ylabel('Vorkommen', fontstyle='italic')
        plt.title('Frequenz Gruppen')
        ax = plt.gca()
        ax.yaxis.set_major_locator(MaxNLocator(integer=True))
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.show()
    if export:
        df.to_csv("protagonist_group_freq_collection.csv",
                  index=False, decimal=',')

    return df


def protagonist_ownother_freq_collection(corpus_collection,
                                         plot=False,
                                         export=False):
    """
    Creates a Pandas dataframe with the counts of own group/other group
    references in a CorpusCollection object (i.e. in all subcorpora).

    Parameters:
        - corpus_collection: CorpusCollection object
        - plot: bool. If true, output a plot of the results
        - export: bool. If true, store results in a csv file.
    Returns:
        - Pandas dataframe as described above.
    """

    df = {
        'Own/Other': [
            'Own Group',
            'Other Group',
            'Neutral',
        ],
        'Vorkommen': [
            0, 0, 0
        ]
    }
    df = pd.DataFrame(df)

    for corpus in corpus_collection.collection.values():
        # Surpress print statements in function
        with contextlib.redirect_stdout(None):
            sub_df = astats.protagonist_ownother_freq(corpus)
        df['Vorkommen'] = df['Vorkommen'].add(sub_df['Vorkommen'],
                                              axis='index')

    if plot:
        df_nosum = df[df['Own/Other'] != 'Summe']
        plt.bar(df_nosum['Own/Other'], df_nosum['Vorkommen'])
        plt.xlabel('Own/Other', fontstyle='italic')
        plt.ylabel('Vorkommen', fontstyle='italic')
        plt.title('Frequenz Own/Other')
        plt.show()
    if export:
        df.to_csv("protagonist_ownother_freq_collection.csv",
                  index=False, decimal=',')

    return df


def comfunction_freq_collection(corpus_collection,
                                plot=False,
                                export=False):
    """
    Creates a Pandas dataframe with the counts of communicative functions
    in a CorpusCollection object (i.e. in all subcorpora).

    Parameters:
        - corpus_collection: CorpusCollection object
        - plot: bool. If true, output a plot of the results
        - export: bool. If true, store results in a csv file.
    Returns:
        - Pandas dataframe as described above.
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
            'Summe'
        ],
        'Vorkommen': [
            0, 0, 0, 0, 0, 0, 0, 0
        ]
    }
    df = pd.DataFrame(df)

    for corpus in corpus_collection.collection.values():
        for comfunction in corpus.com_functions:
            if (comfunction['Category']
                    in df['Kommunikative Funktion'].values):
                df.loc[df['Kommunikative Funktion'] ==
                       comfunction['Category'], 'Vorkommen'] += 1

    df.at[4, 'Vorkommen'] = df.at[1, 'Vorkommen'] + df.at[4, 'Vorkommen']
    df.at[5, 'Vorkommen'] = df.at[2, 'Vorkommen'] + df.at[5, 'Vorkommen']
    df.at[6, 'Vorkommen'] = df.at[3, 'Vorkommen'] + df.at[6, 'Vorkommen']

    rows_to_delete = ['Beziehung',
                      'Darstellung',
                      'Expression']
    df = df[~df['Kommunikative Funktion'].isin(rows_to_delete)]

    total = df['Vorkommen'].sum()
    df.at[7, 'Vorkommen'] = total
    df['Anteil'] = (df['Vorkommen'] / total)

    if plot:
        df_nosum = df[df['Kommunikative Funktion'] != 'Summe']
        plt.bar(df_nosum['Kommunikative Funktion'], df_nosum['Vorkommen'])
        plt.xlabel('Kommunikative Funktion', fontstyle='italic')
        plt.ylabel('Vorkommen', fontstyle='italic')
        plt.title('Frequenz kommunikativer Funktionen')
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.show()
    if export:
        df.to_csv("comfunction_freq_collection.csv", index=False, decimal=',')

    return df


def demand_freq_collection(corpus_collection,
                           plot=False,
                           export=False):
    """
    Creates a Pandas dataframe with the counts of explicit and implicit
    demands in a CorpusCollection object (i.e. in all subcorpora).

    Parameters:
        - corpus_collection: CorpusCollection object
        - plot: bool. If true, output a plot of the results
        - export: bool. If true, store results in a csv file.
    Returns:
        - Pandas dataframe as described above.
    """

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

    for corpus in corpus_collection.collection.values():
        # Surpress print statements in function
        with contextlib.redirect_stdout(None):
            sub_df = astats.demand_freq(corpus)
        df['Vorkommen'] = df['Vorkommen'].add(sub_df['Vorkommen'],
                                              axis='index')

    if plot:
        df_nosum = df[df['Forderungstyp'] != 'Summe']
        plt.bar(df_nosum['Forderungstyp'], df_nosum['Vorkommen'])
        plt.xlabel('Forderungstyp', fontstyle='italic')
        plt.ylabel('Vorkommen', fontstyle='italic')
        plt.title('Frequenz Forderungstypen')
        plt.show()
    if export:
        df.to_csv("demand_freq_collection.csv", index=False, decimal=',')

    return df


def freq_inside_spans_collection(corpus_collection,
                                 label_type,
                                 plot=False,
                                 export=False):
    """
    Creates a Pandas dataframe that represents the absolute frequencies of
    how often an annotation category appears in a moralizing speech acts.
    For example, the function can count how many moralizations
    contain 0, 1, 2, ... references to protagonists.
    It does this for a CorpusCollection object (i.e. in all subcorpora).

    Parameters:
        - corpus_collection: CorpusCollection object'
        - label_type: the annotation category that you're counting
        - plot: bool. If true, output a plot of the results
        - export: bool. If true, store results in a csv file
    Returns:
        - Pandas dataframe as described above.
    """

    label_possibilities = ['obj_morals', 'subj_morals', 'all_morals',
                           'protagonists', 'protagonists_doubles',
                           'com_functions',
                           'expl_demands', 'impl_demands', 'all_demands']
    if label_type not in label_possibilities:
        print("Error: label_type must be one of:\n" +
              "\n".join(label_possibilities))
        return

    df = {'Label in einer Moralis.': [0, 'Summe'],
          'Häufigkeit': [0, 0]}
    df = pd.DataFrame(df)

    for corpus in corpus_collection.collection.values():
        # Surpress print statements in function
        with contextlib.redirect_stdout(None):
            sub_df = astats.freq_inside_spans(corpus, label_type)
        df = pd.concat([df, sub_df], ignore_index=True)
        df = df.groupby('Label in einer Moralis.', as_index=False).sum()

    sum = df.loc[df['Label in einer Moralis.'] == 'Summe', 'Häufigkeit'].values
    df['Anteil'] = df['Häufigkeit'] / sum

    if plot:
        df_nosum = df[df['Label in einer Moralis.'] != 'Summe']
        plt.bar(df_nosum.index, df_nosum['Häufigkeit'])
        plt.xlabel('Label in einer Moralisierung', fontstyle='italic')
        plt.ylabel('Häufigkeit', fontstyle='italic')
        plt.title('Häufigkeitsverteilung')
        plt.xticks(range(0, len(df_nosum['Label in einer Moralis.'])))
        ax = plt.gca()
        ax.yaxis.set_major_locator(MaxNLocator(integer=True))
        plt.show()
    if export:
        df.to_csv(("freq_inside_spans_" + label_type + ".csv"),
                  index=False, decimal=',')

    return df


def roles_and_groups_collection(corpus_collection,
                                relative=False,
                                export=False):
    """
    Counts how often a specific group of protagonists (such as
    'individual') is associated with a specific role inside
    a CorpusCollection object (i.e. in all subcorpora).

    Parameters:
        - corpus_collection: CorpusCollection object
        - relative: bool. If true, calculate relative frequencies
                          of every association.
        - export: bool. If true, store results in a csv file.
    Returns:
        - Pandas dataframe as described above.
    """

    df_list = []
    for corpus in corpus_collection.collection.values():
        sub_df = la.roles_groups_table(corpus.protagonists,
                                       corpus_collection.language)
        df_list.append(sub_df)

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

    for df in df_list:
        df_full.iloc[:, 1:] += df.iloc[:, 1:]

    if corpus_collection.language.lower() == 'de':
        df_full.drop('Malefizient:in', axis=1, inplace=True)
        df_full.drop('Bezug unklar', axis=1, inplace=True)
    elif corpus_collection.language.lower() != 'all':
        df_full.drop('Kein Bezug', axis=1, inplace=True)
    else:
        df_full['Kein Bezug/Bezug unklar'] = (df_full['Kein Bezug'] +
                                              df_full['Bezug unklar'])
        df_full.drop('Bezug unklar', axis=1, inplace=True)
        df_full.drop('Kein Bezug', axis=1, inplace=True)

    if relative:
        if corpus_collection.language.lower() == 'de':
            df_full[['Adresassat:in',
                     'Benefizient:in',
                     'Forderer:in',
                     'Kein Bezug'
                     ]] \
                = df_full[['Adresassat:in',
                           'Benefizient:in',
                           'Forderer:in',
                           'Kein Bezug'
                           ]].apply(lambda x: x / x.sum())
        elif corpus_collection.language.lower() != 'all':
            df_full[['Adresassat:in',
                     'Benefizient:in',
                     'Forderer:in',
                     'Malefizient:in',
                     'Bezug unklar'
                     ]] \
                = df_full[['Adresassat:in',
                           'Benefizient:in',
                           'Forderer:in',
                           'Malefizient:in',
                           'Bezug unklar'
                           ]].apply(lambda x: x / x.sum())
        else:
            df_full[['Adresassat:in',
                     'Benefizient:in',
                     'Forderer:in',
                     'Malefizient:in',
                     'Bezug unklar/kein Bezug'
                     ]] \
                = df_full[['Adresassat:in',
                           'Benefizient:in',
                           'Forderer:in',
                           'Malefizient:in',
                           'Bezug unklar/kein Bezug'
                           ]].apply(lambda x: x / x.sum())

    if export:
        df_full.to_csv("roles_and_groups_collection.csv",
                       index=False, decimal=',')

    return df_full


def groups_and_ownother_collection(corpus_collection,
                                   relative=False,
                                   export=False):
    """
    Counts how often a specific group of protagonists (such as
    'individual') is associated with own group/other group identification
    inside a CorpusCollection object (i.e. in all subcorpora).

    Parameters:
        - corpus_collection: CorpusCollection object
        - relative: bool. If true, calculate relative frequencies
                          of every association.
        - export: bool. If true, store results in a csv file.
    Returns:
        - Pandas dataframe as described above.
    """

    df_list = []
    for corpus in corpus_collection.collection.values():
        sub_df = la.groups_ownother_table(corpus.protagonists)
        df_list.append(sub_df)

    df = df_list[0]
    for i in range(0, len(df_list)-1):
        df.iloc[:, 1:] += df_list[i + 1].iloc[:, 1:]

    if relative:
        df[['Own Group',
            'Other Group',
            'Neutral',
            ]] \
            = df[['Own Group',
                  'Other Group',
                  'Neutral',
                  ]].apply(lambda x: x / x.sum())

    if export:
        df.to_csv("groups_and_ownother.csv", index=False, decimal=',')

    return df


def roles_and_ownother_collection(corpus_collection,
                                  relative=False,
                                  export=False):
    """
    Counts how often a specific roles of protagonists (such as
    'individual') is associated with own group/other group identification
    inside a CorpusCollection object (i.e. in all subcorpora).

    Parameters:
        - corpus_collection: CorpusCollection object
        - relative: bool. If true, calculate relative frequencies
                          of every association.
        - export: bool. If true, store results in a csv file.
    Returns:
        - Pandas dataframe as described above.
    """

    df_list = []
    for corpus in corpus_collection.collection.values():
        sub_df = la.roles_ownother_table(corpus.protagonists,
                                         language=corpus_collection.language)
        df_list.append(sub_df)

    df = df_list[0]
    for i in range(0, len(df_list)-1):
        df.iloc[:, 1:] += df_list[i + 1].iloc[:, 1:]

    if relative:
        df[['Own Group',
            'Other Group',
            'Neutral',
            ]] \
            = df[['Own Group',
                  'Other Group',
                  'Neutral',
                  ]].apply(lambda x: x / x.sum())

    if export:
        df.to_csv("roles_and_ownother.csv", index=False, decimal=',')

    return df


def association_measure_collection(corpus_collection,
                                   cat1,
                                   cat2,
                                   significance=True,
                                   export=False):
    """
    For two annotation categories, calculates how every lables in
    one of the categories is associated with every label of the other
    category using PMI (pointwise mutual information). Creates a table
    with the results. It does this for a CorpusCollection object
    (i.e. all its subcorpora).

    Parameters:
        - corpus_collection: CorpusCollection object
        - cat1: str. category you want to associate with the other category
        - cat2: str. category you want to associate with the other category
        - significance: bool. If true, calculates the significance with
                              Fisher's exact test for every association
        - export: bool. If true, store results in a csv file.
    Returns:
        - Pandas dataframe as described above.
    """

    cat_possibilities = ['obj_morals', 'subj_morals', 'all_morals',
                         'prot_roles', 'prot_groups', 'prot_ownother',
                         'com_functions',
                         'demands']

    if (cat1 not in cat_possibilities or cat2 not in cat_possibilities):
        print("Error: label_type must be one of:\n" +
              "\n".join(cat_possibilities))
        return
    if (cat1 in cat_possibilities[3:6] and cat2 in cat_possibilities[3:6]):
        print("Note: It might be better to use roles_and_groups(),"
              " roles_and_ownother() or groups_and_ownother() here!")

    tables_df = pd.DataFrame(index=xau.possible_labels(cat1),
                             columns=xau.possible_labels(cat2))
    for row_label in tables_df.index:
        for col_label in tables_df.columns:
            tables_df.loc[row_label, col_label] = [[0, 0], [0, 0]]

    for corpus in corpus_collection.collection.values():
        sub_df = la.table_table(corpus, cat1, cat2)
        for row_label in tables_df.index:
            # Iterate over column labels
            for col_label in tables_df.columns:
                # Get the value from the original_df
                original_value = tables_df.loc[row_label, col_label]

                # Get the value from the additional_df
                additional_value = sub_df.loc[row_label, col_label]

                # Perform the addition and update the value in the original_df
                tables_df.loc[row_label, col_label] = [
                    [original_value[0][0] + additional_value[0][0],
                     original_value[0][1] + additional_value[0][1]],
                    [original_value[1][0] + additional_value[1][0],
                     original_value[1][1] + additional_value[1][1]]
                ]

    if significance:
        columns = pd.MultiIndex.from_product([xau.possible_labels(cat2),
                                             ['Significance', 'PMI']])
        am_df = pd.DataFrame(index=xau.possible_labels(cat1),
                             columns=columns)
        for row_label in am_df.index:
            for col_label in xau.possible_labels(cat2):

                table = tables_df.loc[row_label, col_label]

                fisher_sig = stats.fisher_exact(table).pvalue
                pmi_norm = xau.calculate_normalized_pmi(table)

                am_df.loc[row_label, (col_label, 'Significance')] = fisher_sig
                am_df.loc[row_label, (col_label, 'PMI')] = pmi_norm

    else:
        am_df = tables_df
        for row_label in am_df.index:
            for col_label in xau.possible_labels(cat2):
                table = tables_df.loc[row_label, col_label]

                pmi_norm = xau.calculate_normalized_pmi(table)
                am_df.loc[row_label, col_label] = pmi_norm

    if export:
        am_df.to_csv("association.csv", index=False, decimal=',')

    return am_df
