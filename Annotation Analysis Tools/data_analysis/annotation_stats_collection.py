import label_analysis as la
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator
import contextlib
import xmi_analysis_util as xau
import scipy.stats as stats
import annotation_stats_single as astats


def moral_values_freq_collection(corpus_collection, moral_type="all",
                                 sum_dimensions=False, plot=False,
                                 export=False):

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
                                     plot=False, export=False):
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
                                      plot=False, export=False):
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

    total = df['Vorkommen'].sum()
    df['Anteil'] = (df['Vorkommen'] / total)

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
                                         plot=False, export=False):
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
                                plot=False, export=False):
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
        print(corpus.com_functions)
        for comfunction in corpus.com_functions:
            if (comfunction['Category']
                    in df['Kommunikative Funktion'].values):
                df.loc[df['Kommunikative Funktion'] ==
                       comfunction['Category'], 'Vorkommen'] += 1

    total = df['Vorkommen'].sum()
    df['Anteil'] = (df['Vorkommen'] / total)

    df.at[5, 'Vorkommen'] = df.at[1, 'Vorkommen'] + df.at[5, 'Vorkommen']
    df.at[6, 'Vorkommen'] = df.at[2, 'Vorkommen'] + df.at[6, 'Vorkommen']
    df.at[7, 'Vorkommen'] = df.at[3, 'Vorkommen'] + df.at[7, 'Vorkommen']

    rows_to_delete = ['Beziehung',
                      'Darstellung',
                      'Expression']
    df = df[~df['Kommunikative Funktion'].isin(rows_to_delete)]

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
                           plot=False, export=False):
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


def freq_inside_spans_collection(corpus_collection, label_type,
                                 plot=False, export=False):

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
                                relative=False, export=False):
    df_list = []
    for corpus in corpus_collection.collection.values():
        sub_df = la.label_table(corpus.protagonists,
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


def association_measure_collection(corpus_collection, cat1, cat2,
                                   significance=True, export=False):
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
                                             ['Sig', 'PMI']])
        am_df = pd.DataFrame(index=xau.possible_labels(cat1),
                             columns=columns)
        for row_label in am_df.index:
            for col_label in xau.possible_labels(cat2):

                table = tables_df.loc[row_label, col_label]

                fisher_sig = stats.fisher_exact(table).pvalue
                pmi_norm = xau.calculate_normalized_pmi(table)

                am_df.loc[row_label, (col_label, 'Sig')] = fisher_sig
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
