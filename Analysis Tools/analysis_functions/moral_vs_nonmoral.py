"""
At the core of this module are the compare_... functions.

They allow you to compare the linuistic surface features of two list of texts.
You can compare the frequencies of lemmata, parts of speech (POS),
or types (word forms).


Author:
Bruno Brocai (bruno.brocai@gs.uni-heidelberg.de)
University of Heidelberg
Research Projekt "Moralisierungen in verschiedenen Wissensdomänen"
"""


import nltk
from scipy import stats
import xlsxwriter
from . import _nlp_ as nlp


def nlp_kwargs_handler(kwargs):
    language = kwargs.get("language", "german")
    tagger = kwargs.get("tagger", "Spacy")
    tokenizer = kwargs.get("tokenizer", "Spacy")
    lower = kwargs.get("lower", False)

    return language, tagger, tokenizer, lower


def get_stats(
        counter_moral_prot,
        counter_moral_n,
        counter_them_prot,
        counter_them_n
):
    """Given the counts of a linguistik surface feature in moralizing
    and non-moralizing segments, this function calculates analyzes
    its distribution and whether it is significantly different between
    the two groups.

    Args:
        counter_moral_prot (int): The count of the feature
            in moralizing segments.
        counter_moral_n (int): The total count of moralizing segments.
        counter_them_prot (int): The count of the feature
            in non-moralizing segments.
        counter_them_n (int): The total count of non-moralizing segments.
    Returns:
        dict: A dictionary with the following keys:
            - likelihood_moral: The likelihood of the feature
                in moralizing segments.
            - likelihood_nonmoral: The likelihood of the feature
                in non-moralizing segments.
            - ratio: The ratio of the likelihoods.
            - diff_coeficient: Difference coefficient as described by
                Yule (2014)
            - pvalue_fisher: The p-value of the Fisher's exact test.
            - contingency_table: The contingency table used for the test.
    """

    try:
        likelihood_moral = counter_moral_prot / counter_moral_n
        likelihood_them = counter_them_prot / counter_them_n

        not_prot_moral = counter_moral_n - counter_moral_prot
        not_prot_them = counter_them_n - counter_them_prot

        contingency_table = [
            [counter_moral_prot, not_prot_moral],
            [counter_them_prot, not_prot_them]
        ]

        res = stats.fisher_exact(contingency_table)

        ratio = (
            likelihood_moral
            / likelihood_them
        )
        diff_coeficient = (
            (likelihood_moral - likelihood_them)
            / (likelihood_moral + likelihood_them)
        )

        statistics = {
            "likelihood_moral": likelihood_moral,
            "likelihood_nonmoral": likelihood_them,
            "ratio": ratio,
            "diff_coeficient": diff_coeficient,
            "pvalue_fisher": res.pvalue,
            "contingency_table": contingency_table
        }

        return statistics

    except ZeroDivisionError:
        print("Error: Division by zero.")
        return None


def count_instances_lemma(
    text_list,
    lemmata_list,
    combined_mode,
    **kwargs
):
    """Counts the occurences of a list of lemmata in a list of text passages.

    Args:
        text_list (list): A list of strings.
        lemmata_list (list): A list of lemmata (strings).
        combined_mode (bool): If True, the function returns a dictionary
            with the counts of all lemmata combined, else, they are separate.
        language (str): The language of the text passages. Default is German.
        tagger (str): If HanTa, the function uses the Hanta tagger, else Spacy.
            Default is Spacy.

    Returns:
        dict: The key "_total_" contains the count of all tokens in the corpus,
            not just the ones specified, and is present in all modes.
            If combined_mode is False, the keys are the lemmata and the values
            are the associated counts.
            If combined_mode is True, the key is a tuple of all lemmata and the
            value is the total count of all lemmata, added up.
    """

    language, tagger, _, _ = nlp_kwargs_handler(kwargs)

    comparison_dict = {lemma: 0 for lemma in lemmata_list}
    comparison_dict["_total_"] = 0

    if tagger.lower() == "hanta":

        tagger, language = nlp.init_hanta_nltk(language)

        # Loop through the rows in the dataframe of moralizing segments
        for doc in text_list:
            doc = doc.replace('#', '')  # Data may contain '#' for highlighting
            tokenized_sents = nltk.tokenize.word_tokenize(
                doc, language=language)
            tags = tagger.tag_sent(tokenized_sents)
            for tag in tags:
                comparison_dict["_total_"] += 1
                if tag[1] in comparison_dict.keys():
                    comparison_dict[tag[1]] += 1

    else:

        model = nlp.init_spacy(language)

        for doc in text_list:
            doc = doc.replace('#', '')  # Data may contain '#' for highlighting
            tagged = model(doc)
            for tag in tagged:
                comparison_dict["_total_"] += 1
                if tag.lemma_ in comparison_dict.keys():
                    comparison_dict[tag.lemma_] += 1

    if combined_mode:
        combined_dict = {
            "_total_": comparison_dict.pop("_total_")
        }
        combined_dict[tuple(lemmata_list)] = sum(comparison_dict.values())
        return combined_dict

    return comparison_dict


def count_instances_pos(
    text_list,
    pos_list,
    combined_mode,
    **kwargs
):
    """Counts the occurences of a list of parts of speech (POS) in a list
    of text passages.

    Keep in mind that Hanta and Spacy use different POS tags.

    Args:
        text_list (list): A list of strings.
        pos_list (list): A list of POS (strings).
        combined_mode (bool): If True, the function returns a dictionary
            with the counts of all POS combined, else, they are separate.
        language (str): The language of the text passages. Default is German.
        tagger (str): If HanTa, the function uses the Hanta tagger, else Spacy.
            Default is Spacy.

    Returns:
        dict: The key "_total_" contains the count of all tokens in the corpus,
            not just the ones specified, and is present in all modes.
            If combined_mode is False, the keys are the POS and the values
            are the associated counts.
            If combined_mode is True, the key is a tuple of all POS and the
            value is the total count of all POS, added up.
    """

    language, tagger, _, _ = nlp_kwargs_handler(kwargs)

    comparison_dict = {pos: 0 for pos in pos_list}
    comparison_dict["_total_"] = 0

    if tagger.lower() == "hanta":

        tagger, language = nlp.init_hanta_nltk(language)

        # Loop through the rows in the dataframe of moralizing segments
        for doc in text_list:
            doc = doc.replace('#', '')  # Data may contain '#' for highlighting
            tokenized_sents = nltk.tokenize.word_tokenize(
                doc, language=language)
            tags = tagger.tag_sent(tokenized_sents)
            for tag in tags:
                comparison_dict["_total_"] += 1
                if tag[2] in comparison_dict.keys():
                    comparison_dict[tag[2]] += 1

    else:

        model = nlp.init_spacy(language)

        for doc in text_list:
            doc = doc.replace('#', '')  # Data may contain '#' for highlighting
            tagged = model(doc)
            for tag in tagged:
                comparison_dict["_total_"] += 1
                if tag.pos_ in comparison_dict.keys():
                    comparison_dict[tag.pos_] += 1

    if combined_mode:
        combined_dict = {
            "_total_": comparison_dict.pop("_total_")
        }
        combined_dict[tuple(pos_list)] = sum(comparison_dict.values())
        return combined_dict

    return comparison_dict


def count_instances_type(
    text_list,
    token_list,
    combined_mode,
    **kwargs
):
    """Counts the occurences of a list of types (word forms) in a list
    of text passages.

    Args:
        text_list (list): A list of strings.
        pos_list (list): A list of types (strings).
        combined_mode (bool): If True, the function returns a dictionary
            with the counts of all types combined, else, they are separate.
        language (str): The language of the text passages. Default is German.
        tokenizer (str): If NLTK, the function uses NLTK to tokenize,
            else Spacy. Default is Spacy.
        lower (bool): If True, the types are converted to lowercase.

    Returns:
        dict: The key "_total_" contains the count of all tokens in the corpus,
            not just the ones specified, and is present in all modes.
            If combined_mode is False, the keys are the types and the values
            are the associated counts.
            If combined_mode is True, the key is a tuple of all types and the
            value is the total count of all types, added up.
    """

    language, _, tokenizer, lower = nlp_kwargs_handler(kwargs)

    if tokenizer.lower() == 'spacy':
        model = nlp.init_spacy(language)
    elif tokenizer.lower() == 'nltk':
        language = nlp.init_nltk_language(language)

    comparison_dict = {token: 0 for token in token_list}
    comparison_dict["_total_"] = 0

    # Loop through the rows in the dataframe of moralizing segments
    for doc in text_list:
        doc = doc.replace('#', '')  # Data may contain '#' for highlighting

        if tokenizer.lower() == 'spacy':
            tokenized_sents = [token.text for token in model(doc)]
        elif tokenizer.lower() == 'nltk':
            tokenized_sents = nltk.tokenize.word_tokenize(
                doc, language=language)
        if lower:
            tokenized_sents = [word.lower() for word in tokenized_sents]

        for word in tokenized_sents:
            comparison_dict["_total_"] += 1
            if word in comparison_dict.keys():
                comparison_dict[word] += 1

    if combined_mode:
        combined_dict = {
            "_total_": comparison_dict.pop("_total_")
        }
        combined_dict[tuple(token_list)] = sum(comparison_dict.values())
        return combined_dict

    return comparison_dict


def compare_lemma_likelihood(
    moral_list,
    nonmoral_list,
    lemmata,
    **kwargs
):
    """This function compares how a given list of lemmata is distributed
    in moralizing and non-moralizing segments.

    It calculates the stats for the lemmata in the list taken together,
    not separately.
    It prints the results to the console.

    Args:
        moral_list (list): A list of moralizing segments.
        nonmoral_list (list): A list of non-moralizing segments.
        lemmata (list): A list of lemmata to compare.
        language (str): The language of the text passages. Default is German.
        tagger (str): If HanTa, the function uses the Hanta tagger, else Spacy.
            Default is Spacy.

    Returns:
        A dictionary created by the get_stats function, see there.
    """

    moral_counts = count_instances_lemma(
        moral_list,
        lemmata,
        combined_mode=True,
        **kwargs
    )
    nonmoral_counts = count_instances_lemma(
        nonmoral_list,
        lemmata,
        combined_mode=True,
        **kwargs
    )

    results = get_stats(
        moral_counts[tuple(lemmata)],
        moral_counts["_total_"],
        nonmoral_counts[tuple(lemmata)],
        nonmoral_counts["_total_"]
    )

    for stat, value in results.items():
        print(stat, value)

    return results


def compare_pos_likelihood(
    moral_list,
    nonmoral_list,
    pos_list,
    **kwargs
):
    """This function compares how a given list of parts of speech (POS)
    is distributed in moralizing and non-moralizing segments.

    It calculates the stats for the POS in the list taken together,
    not separately.
    It prints the results to the console.

    Keep in mind that Hanta and Spacy use different POS tags.

    Args:
        moral_list (list): A list of moralizing segments.
        nonmoral_list (list): A list of non-moralizing segments.
        lemmata (list): A list of POS to compare.
        language (str): The language of the text passages. Default is German.
        tagger (str): If HanTa, the function uses the Hanta tagger, else Spacy.
            Default is Spacy.

    Returns:
        A dictionary created by the get_stats function, see there.
    """

    moral_counts = count_instances_pos(
        moral_list,
        pos_list,
        combined_mode=True,
        **kwargs
    )
    nonmoral_counts = count_instances_pos(
        nonmoral_list,
        pos_list,
        combined_mode=True,
        **kwargs
    )

    results = get_stats(
        moral_counts[tuple(pos_list)],
        moral_counts["_total_"],
        nonmoral_counts[tuple(pos_list)],
        nonmoral_counts["_total_"],
    )

    for stat, value in results.items():
        print(stat, value)

    return results


def compare_type_likelihood(
    moral_list,
    nonmoral_list,
    token_list,
    **kwargs
):
    """This function compares how a given list of types (word forms)
    is distributed in moralizing and non-moralizing segments.

    It calculates the stats for the lemmata in the list taken together,
    not separately.
    It prints the results to the console.

    Args:
        moral_list (list): A list of moralizing segments.
        nonmoral_list (list): A list of non-moralizing segments.
        lemmata (list): A list of lemmata to compare.
        language (str): The language of the text passages. Default is German.
        tokenizer (str): If HanTa, the function uses the Hanta tagger,
            else Spacy. Default is Spacy.
        lower (bool): If True, the types are converted to lowercase.
            Default is False.

    Returns:
        A dictionary created by the get_stats function, see there.
    """

    moral_counts = count_instances_type(
        moral_list,
        token_list,
        combined_mode=True,
        **kwargs
    )
    nonmoral_counts = count_instances_type(
        nonmoral_list,
        token_list,
        combined_mode=True,
        **kwargs
    )

    results = get_stats(
        moral_counts[tuple(token_list)],
        moral_counts["_total_"],
        nonmoral_counts[tuple(token_list)],
        nonmoral_counts["_total_"],
    )

    for stat, value in results.items():
        print(stat, value)

    return results


def compare_lemma_likelihood_dict(
    moral_list,
    nonmoral_list,
    lemmata,
    **kwargs
):
    """This function compares how a given list of lemmata is distributed
    in moralizing and non-moralizing segments.

    It calculates the stats for the lemmata in the list taken separately
    and returns a dicitonary of stats for each lemma.

    Args:
        moral_list (list): A list of moralizing segments.
        nonmoral_list (list): A list of non-moralizing segments.
        lemmata (list): A list of lemmata to compare.
        language (str): The language of the text passages. Default is German.
        tagger (str): If HanTa, the function uses the Hanta tagger, else Spacy.
            Default is Spacy.

    Returns:
        dict: Keys are the lemmata and the values are dictionaries as
            created by the get_stats function, see there.
    """

    moral_counts = count_instances_lemma(
        moral_list,
        lemmata,
        combined_mode=False,
        **kwargs
    )
    nonmoral_counts = count_instances_lemma(
        nonmoral_list,
        lemmata,
        combined_mode=False,
        **kwargs
    )

    results_dict = {}
    for lemma in lemmata:
        results_dict[lemma] = get_stats(
            moral_counts[lemma],
            moral_counts["_total_"],
            nonmoral_counts[lemma],
            nonmoral_counts["_total_"]
        )

    return results_dict


def compare_pos_likelihood_dict(
    moral_list,
    nonmoral_list,
    pos_list,
    **kwargs
):
    """This function compares how a given list of parts of speech (POS)
    is distributed in moralizing and non-moralizing segments.

    It calculates the stats for the POS in the list taken separately,
    creating a dictionary of stats for each POS.

    Keep in mind that Hanta and Spacy use different POS tags.

    Args:
        moral_list (list): A list of moralizing segments.
        nonmoral_list (list): A list of non-moralizing segments.
        lemmata (list): A list of POS to compare.
        language (str): The language of the text passages. Default is German.
        tagger (str): If HanTa, the function uses the Hanta tagger, else Spacy.
            Default is Spacy.

    Returns:
        dict: Keys are the POS and the values are dictionaries as
            created by the get_stats function, see there.
    """

    moral_counts = count_instances_pos(
        moral_list,
        pos_list,
        combined_mode=False,
        **kwargs
    )
    nonmoral_counts = count_instances_pos(
        nonmoral_list,
        pos_list,
        combined_mode=False,
        **kwargs
    )

    results_dict = {}
    for pos in pos_list:
        results_dict[pos] = get_stats(
            moral_counts[pos],
            moral_counts["_total_"],
            nonmoral_counts[pos],
            nonmoral_counts["_total_"]
        )

    return results_dict


def compare_token_likelihood_dict(
    moral_list,
    nonmoral_list,
    token_list,
    **kwargs
):
    """This function compares how a given list of types (word forms)
    is distributed in moralizing and non-moralizing segments.

    It calculates the stats for the lemmata in the list separately,
    creating a dictionary of stats for each type.

    Args:
        moral_list (list): A list of moralizing segments.
        nonmoral_list (list): A list of non-moralizing segments.
        lemmata (list): A list of lemmata to compare.
        language (str): The language of the text passages. Default is German.
        tokenizer (str): If HanTa, the function uses the Hanta tagger,
            else Spacy. Default is Spacy.
        lower (bool): If True, the types are converted to lowercase.
            Default is False.

    Returns:
        dict: Keys are the types and the values are dictionaries as
            created by the get_stats function, see there.
    """

    moral_counts = count_instances_type(
        moral_list,
        token_list,
        combined_mode=False,
        **kwargs
    )
    nonmoral_counts = count_instances_type(
        nonmoral_list,
        token_list,
        combined_mode=False,
        **kwargs
    )

    results_dict = {}
    for token in token_list:
        results_dict[token] = get_stats(
            moral_counts[token],
            moral_counts["_total_"],
            nonmoral_counts[token],
            nonmoral_counts["_total_"]
        )

    return results_dict


def dictdict_to_xlsx(dictionary, filename):
    """Writes a dictionary of dictionaries to an Excel file.

    The columns are the keys of the outer dictionary,
    the rows are the keys of the inner dictionaries.

    Args:
        dictionary (dict): A dictionary of dictionaries.
        filename (str): The name of the Excel file to write to.

    Returns:
        None
    """

    if filename[-5:] != ".xlsx":
        print("Filename is not an excel file!")
        print(f"The file ending is {filename[-5:]} when it should be .xlsx!")

    # Create a workbook and add a worksheet.
    workbook = xlsxwriter.Workbook(filename)
    worksheet = workbook.add_worksheet()

    # Write header row
    bold = workbook.add_format({'bold': True})
    row = 0
    col = 1
    for key in next(iter(dictionary.values())):
        worksheet.write(row, col, key, bold)
        col += 1

    # Iterate over the data and write it out row by row.
    row = 1
    for key, statistics in dictionary.items():
        col = 0
        worksheet.write(row, col, key)
        for value in statistics.values():
            col += 1
            try:
                worksheet.write(row, col, value)
            except TypeError:
                worksheet.write(row, col, str(value))
        row += 1

    workbook.close()
