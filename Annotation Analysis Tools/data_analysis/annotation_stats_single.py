import label_analysis as la
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator
import xmi_analysis_util as xau
import scipy.stats as stats


def moral_values_freq(corpus, moral_type="all",
                      sum_dimensions=False, plot=False, export=False):

    if moral_type == "all":
        value_list = corpus.all_morals
    elif moral_type == "obj":
        value_list = corpus.obj_morals
    elif moral_type == "subj":
        value_list = corpus.subj_morals
    else:
        print("Error: Moral_type parameter must be 'all', 'obj', or 'subj'.")
        return

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
            'OTHER'
        ],
        'Vorkommen': [
            0, 0, 0, 0, 0, 0, 0,
            0, 0, 0, 0, 0, 0
        ]
    }
    df = pd.DataFrame(df)
    for value in value_list:
        if value['Category'] in df['Moralwert'].values:
            df.loc[df['Moralwert'] == value['Category'], 'Vorkommen'] += 1

    if sum_dimensions:
        temp_df = {
            'Moralwert': [
                'Care/harm',
                'Fairness/cheating',
                'Loyalty/betrayal',
                'Authority/subversion',
                'Sanctity/degradation',
                'Liberty/oppression',
                'OTHER'
            ],
            'Vorkommen': [
                0, 0, 0, 0, 0, 0, 0
            ]
        }
        temp_df = pd.DataFrame(temp_df)
        for i in range(0, 6):
            temp_df.loc[i, 'Vorkommen'] = (
                df.loc[i*2]['Vorkommen']
                + df.loc[i*2 + 1]['Vorkommen']
            )
        temp_df.loc[6, 'Vorkommen'] = df.loc[12, 'Vorkommen']

        df = temp_df

    total = df['Vorkommen'].sum()
    df['Anteil'] = (df['Vorkommen'] / total)

    # Create a new row with the 'sum' values
    sum_df = pd.DataFrame({
        'Moralwert': ['Summe'],
        'Vorkommen': [total],
        'Anteil': [1]
        })
    df = pd.concat([df, sum_df], ignore_index=True)

    if plot:
        df_nosum = df[df['Moralwert'] != 'Summe']
        plt.bar(df_nosum['Moralwert'], df_nosum['Vorkommen'])
        plt.xlabel('Moralwert', fontstyle='italic')
        plt.ylabel('Vorkommen', fontstyle='italic')
        plt.title('Frequenz Moralwerte')
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.show()
    if export:
        df.to_csv("protagonist_role_freq.csv", index=False, decimal=',')

    return df


def protagonist_role_freq(corpus, language, plot=False, export=False):
    df = {
        'Rolle': [
            'Adresassat:in',
            'Benefizient:in',
            'Forderer:in',
            'Malefizient:in',
            'Bezug unklar',
            'Kein Bezug'
        ],
        'Vorkommen': [
            0, 0, 0, 0, 0, 0
        ]
    }
    df = pd.DataFrame(df)

    for protagonist in corpus.protagonists_doubles:
        if protagonist['Rolle'] in df['Rolle'].values:
            df.loc[df['Rolle'] == protagonist['Rolle'], 'Vorkommen'] += 1

    total = df['Vorkommen'].sum()
    df['Anteil'] = (df['Vorkommen'] / total)

    # Create a new row with the 'sum' values
    sum_df = pd.DataFrame({
        'Rolle': ['Summe'],
        'Vorkommen': [total],
        'Anteil': [1]
        })
    df = pd.concat([df, sum_df], ignore_index=True)

    if language.lower() == 'de':
        rows_to_delete = ['Malefizient:in', 'Bezug unklar']
        df = df[~df['Rolle'].isin(rows_to_delete)]
    else:
        rows_to_delete = ['Kein Bezug']
        df = df[~df['Rolle'].isin(rows_to_delete)]

    if plot:
        df_nosum = df[df['Rolle'] != 'Summe']
        plt.bar(df_nosum['Rolle'], df_nosum['Vorkommen'])
        plt.xlabel('Rolle', fontstyle='italic')
        plt.ylabel('Vorkommen', fontstyle='italic')
        plt.title('Frequenz Rollen')
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.show()
    if export:
        df.to_csv("protagonist_role_freq.csv", index=False, decimal=',')

    return df


def protagonist_group_freq(corpus, plot=False, export=False):
    df = {
        'Gruppe': [
            'Individuum',
            'Institution',
            'Menschen',
            'soziale Gruppe',
            'OTHER'
        ],
        'Vorkommen': [
            0, 0, 0, 0, 0
        ]
    }
    df = pd.DataFrame(df)

    for protagonist in corpus.protagonists:
        if protagonist['Gruppe'] in df['Gruppe'].values:
            df.loc[df['Gruppe'] == protagonist['Gruppe'], 'Vorkommen'] += 1

    total = df['Vorkommen'].sum()
    df['Anteil'] = (df['Vorkommen'] / total)

    # Create a new row with the 'sum' values
    sum_df = pd.DataFrame({
        'Gruppe': ['Summe'],
        'Vorkommen': [total],
        'Anteil': [1]
        })
    df = pd.concat([df, sum_df], ignore_index=True)

    if plot:
        df_nosum = df[df['Gruppe'] != 'Summe']
        plt.bar(df_nosum['Gruppe'], df_nosum['Vorkommen'])
        plt.xlabel('Gruppe', fontstyle='italic')
        plt.ylabel('Vorkommen', fontstyle='italic')
        plt.title('Frequenz Gruppen')
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.show()
    if export:
        df.to_csv("protagonist_group_freq.csv", index=False, decimal=',')

    return df


def protagonist_ownother_freq(corpus, plot=False, export=False):
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

    for protagonist in corpus.protagonists:
        if protagonist['own/other'] in df['Own/Other'].values:
            df.loc[
                df['Own/Other'] == protagonist['own/other'], 'Vorkommen'
            ] += 1

    total = df['Vorkommen'].sum()
    df['Anteil'] = (df['Vorkommen'] / total)

    # Create a new row with the 'sum' values
    sum_df = pd.DataFrame({
        'Own/Other': ['Summe'],
        'Vorkommen': [total],
        'Anteil': [1]
        })
    df = pd.concat([df, sum_df], ignore_index=True)

    if plot:
        df_nosum = df[df['Own/Other'] != 'Summe']
        plt.bar(df_nosum['Own/Other'], df_nosum['Vorkommen'])
        plt.xlabel('Own/Other', fontstyle='italic')
        plt.ylabel('Vorkommen', fontstyle='italic')
        plt.title('Frequenz Own/Other')
        plt.show()
    if export:
        df.to_csv("protagonist_ownother_freq.csv", index=False, decimal=',')

    return df


def comfunction_freq(corpus, language, plot=False, export=False):
    df = {
        'Kommunikative Funktion': [
            'Appell',
            'Beziehung',
            'Darstellung',
            'Expression',
            'Appell+Beziehung',
            'Appell+Darstellung',
            'Appell+Expression'
        ],
        'Vorkommen': [
            0, 0, 0, 0, 0, 0, 0
        ]
    }
    df = pd.DataFrame(df)
    for func in corpus.com_functions:
        if func['Category'] in df['Kommunikative Funktion'].values:
            df.loc[
                df['Kommunikative Funktion'] == func['Category'],
                'Vorkommen'] += 1

    total = df['Vorkommen'].sum()
    df['Anteil'] = (df['Vorkommen'] / total)

    # Create a new row with the 'sum' values
    sum_df = pd.DataFrame({
        'Kommunikative Funktion': ['Summe'],
        'Vorkommen': [total],
        'Anteil': [1]
        })
    df = pd.concat([df, sum_df], ignore_index=True)

    if language.lower() == 'de':
        rows_to_delete = [
            'Appell+Beziehung',
            'Appell+Darstellung',
            'Appell+Expression'
        ]
    else:
        rows_to_delete = [
            'Beziehung',
            'Darstellung',
            'Expression'
        ]
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
        df.to_csv("comfunction_freq.csv", index=False, decimal=',')

    return df


def demand_freq(corpus, plot=False, export=False):
    df = {
        'Forderungstyp': [
            'Explizite Forderung',
            'Implizite Forderung'
        ],
        'Vorkommen': [
            len(corpus.expl_demands),
            len(corpus.impl_demands)
        ]
    }
    df = pd.DataFrame(df)

    total = df['Vorkommen'].sum()
    df['Anteil'] = (df['Vorkommen'] / total)

    # Create a new row with the 'sum' values
    sum_df = pd.DataFrame({
        'Forderungstyp': ['Summe'],
        'Vorkommen': [total],
        'Anteil': [1]
        })
    df = pd.concat([df, sum_df], ignore_index=True)

    if plot:
        df_nosum = df[df['Forderungstyp'] != 'Summe']
        plt.bar(df_nosum['Forderungstyp'], df_nosum['Vorkommen'])
        plt.xlabel('Forderungstyp', fontstyle='italic')
        plt.ylabel('Vorkommen', fontstyle='italic')
        plt.title('Frequenz Forderungstypen')
        plt.show()
    if export:
        df.to_csv("demand_freq.csv", index=False, decimal=',')

    return df


def freq_inside_spans(corpus, label_type, plot=False, export=False):
    label_possibilities = ['obj_morals', 'subj_morals', 'all_morals',
                           'protagonists', 'protagonists_doubles',
                           'com_functions',
                           'expl_demands', 'impl_demands', 'all_demands']
    if label_type not in label_possibilities:
        print("Error: label_type must be one of:\n" +
              "\n".join(label_possibilities))
        return

    label_list = getattr(corpus, label_type)
    data = la.label_freq_table(corpus.moralizations, label_list)

    # Convert dictionary to DataFrame
    df = pd.DataFrame.from_dict(data, orient='index', columns=['Häufigkeit'])

    # Reset the index and assign the index values to a new column
    df.reset_index(inplace=True)
    df.rename(columns={'index': 'Label in einer Moralis.'}, inplace=True)

    total = df['Häufigkeit'].sum()
    df['Anteil'] = (df['Häufigkeit'] / total)
    sum_df = pd.DataFrame({
        'Label in einer Moralis.': ['Summe'],
        'Häufigkeit': [total],
        'Anteil': [1]
        })
    df = pd.concat([df, sum_df], ignore_index=True)

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


def roles_and_groups(corpus, language, percent=False, export=False):
    df = la.roles_groups_table(corpus.protagonists, language)

    if percent:
        if language.lower() == 'de':
            df[['Adresassat:in',
                'Benefizient:in',
                'Forderer:in',
                'Kein Bezug'
                ]] \
                = df[[
                    'Adresassat:in',
                    'Benefizient:in',
                    'Forderer:in',
                    'Kein Bezug'
                ]].apply(lambda x: x / x.sum() * 100)
        else:
            df[['Adresassat:in',
                'Benefizient:in',
                'Forderer:in',
                'Malefizient:in',
                'Bezug unklar'
                ]] \
                = df[[
                    'Adresassat:in',
                    'Benefizient:in',
                    'Forderer:in',
                    'Malefizient:in'
                    'Bezug unklar'
                ]].apply(lambda x: x / x.sum() * 100)

    if export:
        df.to_csv("roles_and_groups.csv", index=False, decimal=',')

    return df


def groups_and_ownother(corpus, percent=False, export=False):
    df = la.groups_and_ownother(corpus.protagonists)

    if percent:
        df[['Own Group',
            'Other Group',
            'Neutral',
            ]] \
            = df[['Own Group',
                  'Other Group',
                  'Neutral',
                  ]].apply(lambda x: x / x.sum() * 100)

    if export:
        df.to_csv("roles_and_ownother.csv", index=False, decimal=',')

    return df


def roles_and_ownother(corpus, language, percent=False, export=False):
    df = la.roles_ownother_table(corpus.protagonists, language)

    if percent:
        df[['Own Group',
            'Other Group',
            'Neutral',
            ]] \
            = df[['Own Group',
                  'Other Group',
                  'Neutral',
                  ]].apply(lambda x: x / x.sum() * 100)

    if export:
        df.to_csv("groups_and_ownother.csv", index=False, decimal=',')

    return df


def association_measure(corpus, cat1, cat2, significance=True):
    cat_possibilities = ['obj_morals', 'subj_morals', 'all_morals',
                         'prot_roles', 'prot_groups', 'prot_ownother',
                         'com_functions',
                         'demands']

    if (cat1 not in cat_possibilities or cat2 not in cat_possibilities):
        print("Error: label_type must be one of:\n" +
              "\n".join(cat_possibilities))
        return
    if (cat1 in cat_possibilities[3:6] and cat2 in cat_possibilities[3:6]):
        print("It is better to use ------ here!")

    tables_df = xau.table_table(corpus, cat1, cat2)

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

    return am_df
