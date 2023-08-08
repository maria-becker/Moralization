import label_analysis as la
import pandas as pd
import matplotlib.pyplot as plt


def moral_values_freq(value_list, sum_dimensions=False, plot=False):
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

    if not plot:
        print(df)
    else:
        df_nosum = df[df['Moralwert'] != 'Summe']
        plt.bar(df_nosum['Moralwert'], df_nosum['Vorkommen'])
        plt.xlabel('Moralwert')
        plt.ylabel('Vorkommen')
        plt.title('Frequenz Moralwerte')
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.show()


def protagonist_role_freq(protag_list, language, plot=False):
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
    for protagonist in protag_list:
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

    if not plot:
        print(df)
    else:
        df_nosum = df[df['Rolle'] != 'Summe']
        plt.bar(df_nosum['Rolle'], df_nosum['Vorkommen'])
        plt.xlabel('Rolle')
        plt.ylabel('Vorkommen')
        plt.title('Frequenz Rollen')
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.show()


def protagonist_group_freq(protag_list, plot=False):
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
    for protagonist in protag_list:
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

    if not plot:
        print(df)
    else:
        df_nosum = df[df['Gruppe'] != 'Summe']
        plt.bar(df_nosum['Gruppe'], df_nosum['Vorkommen'])
        plt.xlabel('Gruppe')
        plt.ylabel('Vorkommen')
        plt.title('Frequenz Gruppen')
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.show()


def protagonist_ownother_freq(protag_list, plot=False):
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
    for protagonist in protag_list:
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

    if not plot:
        print(df)
    else:
        df_nosum = df[df['Own/Other'] != 'Summe']
        plt.bar(df_nosum['Own/Other'], df_nosum['Vorkommen'])
        plt.xlabel('Own/Other')
        plt.ylabel('Vorkommen')
        plt.title('Frequenz Own/Other')
        plt.show()


def comfunction_freq(comfunction_list, language, plot=False, export=False):
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
    for func in comfunction_list:
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

    if not plot:
        print(df)
    else:
        df_nosum = df[df['Kommunikative Funktion'] != 'Summe']
        plt.bar(df_nosum['Kommunikative Funktion'], df_nosum['Vorkommen'])
        plt.xlabel('Kommunikative Funktion')
        plt.ylabel('Vorkommen')
        plt.title('Frequenz kommunikativer Funktionen')
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.show()
    if export:
        df.to_csv("comfunction_freq.csv")


def demand_freq(expldemand_list, impldemand_list, plot=False, export=False):
    df = {
        'Forderungstyp': [
            'Explizite Forderung',
            'Implizite Forderung'
        ],
        'Vorkommen': [
            len(expldemand_list),
            len(impldemand_list)
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

    if not plot:
        print(df)
    else:
        df_nosum = df[df['Forderungstyp'] != 'Summe']
        plt.bar(df_nosum['Forderungstyp'], df_nosum['Vorkommen'])
        plt.xlabel('Forderungstyp')
        plt.ylabel('Vorkommen')
        plt.title('Frequenz Forderungstypen')
        plt.show()
    if export:
        df.to_csv("demand_freq.csv")


def freq_inside_spans(moral_spans, label_list, plot=False):
    data = la.label_freq_table(moral_spans, label_list)

    # Convert dictionary to DataFrame
    df = pd.DataFrame.from_dict(data, orient='index', columns=['Häufigkeit'])

    # Reset the index and assign the index values to a new column
    df.reset_index(inplace=True)
    df.rename(columns={'index': 'Label in einer Moralis.'}, inplace=True)

    if plot:
        # Create a bar plot
        plt.bar(df.index, df['Häufigkeit'])
        plt.xlabel('Label in einer Moralis.')
        plt.ylabel('Häufigkeit')
        plt.title('Häufigkeitsverteilung')
        plt.show()
    else:
        total = df['Häufigkeit'].sum()
        df['Anteil'] = (df['Häufigkeit'] / total)
        sum_df = pd.DataFrame({
            'Label in einer Moralis.': ['Summe'],
            'Häufigkeit': [total],
            'Anteil': [1]
            })
        df = pd.concat([df, sum_df], ignore_index=True)
        print(df)


def roles_and_groups(protagonists, language, percent=False):
    df = la.label_table(protagonists, language)

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
    print(df)
