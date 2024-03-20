import sys
import label_analysis as la
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator
from scipy import stats
import _stat_utils_ as su

sys.path.append("../_utils_")
import xmi_analysis_util as xau


def label_frequency(
    corpus,
    category,
    sum_dimensions=False,  # only relevant for moral values
    **kwargs
):
    """Creates a dataframe with the frequency of labels
    from a given annotation category.

    Parameters:
        - corpus: Corpus object
        - category: str - the annotation category you want to count.
            Possible values: "prot_roles", "prot_groups",
            "com_functions", "demands",
            "obj_morals", "subj_morals", "all_morals"
        - sum_dimensions: bool - only relevant for moral values. If true,
            the two sides of moral dimensions according to MFT are summed.
            Default is False.
        - **kwargs: additional boolean parameters for the specific functions:
            export (as csv) and plot (using matplotlib)
    Returns:
        Pandas dataframe with the label frequencies, or None if the
        category parameter is invalid.
    """

    match category:
        case "prot_roles":
            df = protagonist_role_freq(corpus, kwargs)
        case "prot_groups":
            df = protagonist_group_freq(corpus, kwargs)
        case "com_functions":
            df = comfunction_freq(corpus, kwargs)
        case "demands":
            df = demand_freq(corpus, kwargs)
        case "obj_morals":
            df = moral_values_freq(corpus, "obj", sum_dimensions, kwargs)
        case "subj_morals":
            df = moral_values_freq(corpus, "subj", sum_dimensions, kwargs)
        case "all_morals":
            df = moral_values_freq(corpus, "all", sum_dimensions, kwargs)
        case _:
            print("Error: label must be one of:\n",
                  "prot_roles, prot_groups, com_functions, demands, ",
                  "obj_morals, subj_morals, all_morals")
            return None

    return df


def moral_values_freq(
    corpus,
    moral_type="all",
    sum_dimensions=False,
    plot=False,
    export=False
):
    """
    Creates a Pandas dataframe with the counts of moral values (based on MFT)
    in a Corpus object.

    Parameters:
        - corpus: Corpus object
        - moral_type: str - valid options are:
            "obj": concrete moral values
            "subj": subjective moral expressions
            "all": both of the above
        - sum_dimensions: bool. If true, the two sides of moral dimensions
                          according to MFT (e.g. Care/Harm) are summed into
                          one row.
        - plot: bool. If true, output a plot of the results
        - export: bool. If true, store results in a csv file.
    Returns:
        Pandas dataframe as described above, or None if the moral_type
        parameter is invalid.
    """

    if moral_type == "all":
        value_list = corpus.concat_annos("all_morals")
    elif moral_type == "obj":
        value_list = corpus.concat_annos("obj_morals")
    elif moral_type == "subj":
        value_list = corpus.concat_annos("subj_morals")
    else:
        print("Error: Moral_type parameter must be 'all', 'obj', or 'subj'.")
        return None

    # Init empty dataframe and fill it with the counts
    df = su.get_moral_df(False)
    for value in value_list:
        if value['Category'] in df['Moralwert'].values:
            df.loc[df['Moralwert'] == value['Category'], 'Vorkommen'] += 1

    # If sum_dimensions is True, sum the two sides of each moral dimension
    if sum_dimensions:
        temp_df = su.get_moral_df(True)
        for i in range(0, 6):
            temp_df.loc[i, 'Vorkommen'] = (
                df.loc[i*2]['Vorkommen']
                + df.loc[i*2 + 1]['Vorkommen']
            )
        temp_df.loc[6, 'Vorkommen'] = df.loc[12, 'Vorkommen']

        df = temp_df

    # Create a new column with relative frequencies
    total = df['Vorkommen'].sum()
    df['Anteil'] = df['Vorkommen'] / total

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


def protagonist_role_freq(
    corpus,
    plot=False,
    export=False
):
    """
    Creates a Pandas dataframe with the counts of the roles
    of the protagonists in a Corpus object.

    Parameters:
        - corpus: Corpus object
        - plot: bool. If true, output a plot of the results
        - export: bool. If true, store results in a csv file.
    Returns:
        Pandas dataframe as described above.
    """

    # Init empty dataframe and fill it with the counts
    df = su.get_prot_role_df()
    protagonist_list = corpus.concat_annos("protagonists_doubles")
    for protagonist in protagonist_list:
        if protagonist['Rolle'] in df['Rolle'].values:
            df.loc[df['Rolle'] == protagonist['Rolle'], 'Vorkommen'] += 1

    # Create a new column with relative frequencies
    total = df['Vorkommen'].sum()
    df['Anteil'] = df['Vorkommen'] / total

    # Create a new row with the 'sum' values
    sum_df = pd.DataFrame({
        'Rolle': ['Summe'],
        'Vorkommen': [total],
        'Anteil': [1]
        })
    df = pd.concat([df, sum_df], ignore_index=True)

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


def protagonist_group_freq(
    corpus,
    plot=False,
    export=False
):
    """
    Creates a Pandas dataframe with the counts of the group categories
    of the protagonists in a Corpus object.

    Parameters:
        - corpus: Corpus object
        - plot: bool. If true, output a plot of the results
        - export: bool. If true, store results in a csv file.
    Returns:
        Pandas dataframe as described above.
    """

    # Init empty dataframe and fill it with the counts
    df = su.get_prot_group_df()
    protagonist_list = corpus.concat_annos("protagonists")
    for protagonist in protagonist_list:
        if protagonist['Gruppe'] in df['Gruppe'].values:
            df.loc[df['Gruppe'] == protagonist['Gruppe'], 'Vorkommen'] += 1

    # Create a new column with relative frequencies
    total = df['Vorkommen'].sum()
    df['Anteil'] = df['Vorkommen'] / total

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


def comfunction_freq(
    corpus,
    plot=False,
    export=False
):
    """
    Creates a Pandas dataframe with the counts of communicative functions
    in a CorpusCollection object (i.e. in all subcorpora).

    Parameters:
        - corpus: Corpus object
        - plot: bool. If true, output a plot of the results
        - export: bool. If true, store results in a csv file.
    Returns:
        Pandas dataframe as described above.
    """

    # Init empty dataframe and fill it with the counts
    df = su.get_comfunction_df()
    comfunctions = corpus.concat_annos("com_functions")
    for func in comfunctions:
        if func['Category'] in df['Kommunikative Funktion'].values:
            df.loc[
                df['Kommunikative Funktion'] == func['Category'],
                'Vorkommen'] += 1

    # Create a new column with relative frequencies
    total = df['Vorkommen'].sum()
    df['Anteil'] = df['Vorkommen'] / total

    # Create a new row with the 'sum' values
    sum_df = pd.DataFrame({
        'Kommunikative Funktion': ['Summe'],
        'Vorkommen': [total],
        'Anteil': [1]
        })
    df = pd.concat([df, sum_df], ignore_index=True)

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


def demand_freq(
    corpus,
    plot=False,
    export=False
):
    """
    Creates a Pandas dataframe with the counts of explicit and implicit
    demands in a Corpus object.

    Parameters:
        - corpus: Corpus object
        - plot: bool. If true, output a plot of the results
        - export: bool. If true, store results in a csv file.
    Returns:
        - Pandas dataframe as described above.
    """

    # Create dataframe with the counts
    expl_demands = corpus.concat_annos("expl_demands")
    impl_demands = corpus.concat_annos("impl_demands")
    df = {
        'Forderungstyp': [
            'Explizite Forderung',
            'Implizite Forderung'
        ],
        'Vorkommen': [
            len(expl_demands),
            len(impl_demands)
        ]
    }
    df = pd.DataFrame(df)

    # Create a new column with relative frequencies
    total = df['Vorkommen'].sum()
    df['Anteil'] = df['Vorkommen'] / total

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


def freq_inside_spans(
    corpus,
    category,
    plot=False,
    export=False
):
    """
    Creates a Pandas dataframe that represents the absolute frequencies of
    how often an annotation category appears in a moralizing speech acts.
    For example, the function can count how many moralizations
    contain 0, 1, 2, ... references to protagonists.

    Parameters:
        - corpus: Corpus object'
        - label_type: the annotation category that you're counting
        - plot: bool. If true, output a plot of the results
        - export: bool. If true, store results in a csv file
    Returns:
        - Pandas dataframe as described above.
    """

    # Check if category is valid
    categories = [
        'obj_morals', 'subj_morals', 'all_morals',
        'protagonists', 'protagonists_doubles',
        'com_functions',
        'expl_demands', 'impl_demands', 'all_demands'
    ]
    if category not in categories:
        print("Error: label_type must be one of:\n" +
              "\n".join(categories))
        return None

    # Get the data from the corpus and create a table
    concat_labels = corpus.concat_annos_coords(category)
    concat_morals = corpus.concat_coords("moralizations")
    data = la.label_freq_table(concat_morals, concat_labels)

    # Convert dictionary to DataFrame
    df = pd.DataFrame.from_dict(data, orient='index', columns=['Häufigkeit'])

    # Reset the index and assign the index values to a new column
    df.reset_index(inplace=True)
    df.rename(columns={'index': 'Label in einer Moralis.'}, inplace=True)

    # Create a new column with relative frequencies
    total = df['Häufigkeit'].sum()
    df['Anteil'] = df['Häufigkeit'] / total
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
        df.to_csv(("freq_inside_spans_" + category + ".csv"),
                  index=False, decimal=',')

    return df


def roles_and_groups(
    corpus,
    percent=False,
    export=False
):
    """
    Counts how often a specific group of protagonists (such as
    'individual') is associated with a specific role inside
    a Corpus object.

    Parameters:
        - corpus_collection: Corpus object
        - relative: bool. If true, calculate relative frequencies
                          of every association.
        - export: bool. If true, store results in a csv file.
    Returns:
        Pandas dataframe as described above.
    """

    protagonists = corpus.concat_annos("protagonists")
    df = la.roles_groups_table(protagonists)

    if percent:
        df[['Adressat:in',
            'Benefizient:in',
            'Forderer:in',
            'Kein Bezug',
            'Malefizient:in',
            'Bezug unklar'
            ]] \
            = df[[
                'Adressat:in',
                'Benefizient:in',
                'Forderer:in',
                'Kein Bezug',
                'Malefizient:in',
                'Bezug unklar'
            ]].apply(lambda x: x / x.sum() * 100)

    if export:
        df.to_csv("roles_and_groups.csv", index=False, decimal=',')

    return df


def association_measure(
    corpus,
    cat1,
    cat2,
    significance=True,
    export=True
):
    """
    For two annotation categories, calculates how every lables in
    one of the categories is associated with every label of the other
    category using PMI (pointwise mutual information). Creates a table
    with the results. It does this for a single Corpus object.

    Parameters:
        - corpus: Corpus object
        - cat1: str. category you want to associate with the other category
        - cat2: str. category you want to associate with the other category
        - significance: bool. If true, calculates the significance with
                              Fisher's exact test for every association
        - export: bool. If true, store results in a csv file.
    Returns:
        Pandas dataframe as described above.
    """

    # Check if categories are valid
    cat_possibilities = ['obj_morals', 'subj_morals', 'all_morals',
                         'prot_roles', 'prot_groups', 'prot_ownother',
                         'com_functions',
                         'demands']
    if (cat1 not in cat_possibilities or cat2 not in cat_possibilities):
        print("Error: cat1 and cat2 must be one of:\n" +
              "\n".join(cat_possibilities))
        return None
    if (cat1 in cat_possibilities[3:6] and cat2 in cat_possibilities[3:6]):
        print("It is better to use roles_and_groups() here!")

    # Create a table of cooccurrences
    tables_df = la.table_table(corpus, cat1, cat2)

    # If significance is True, calculate the significance for each combination
    # Calculate the PMI for each combination
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

    # If significance is False, calculate only the PMI
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
