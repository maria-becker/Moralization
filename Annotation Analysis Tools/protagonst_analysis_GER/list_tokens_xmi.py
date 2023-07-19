"""
This module is similar to list_tokens_excel.py,
but it uses lists of string to perform its tasks.
Such lists can be created directly from the xmi data,
using the protagonist_analysis module.


Functions:
    list_to_dict_span(string_list, lower=True)
    list_to_dict_lemma(string_list)
    count_pos_freq(dictionary)
    list_pos_examples(dictionary, pos)
"""

import nltk
from HanTa import HanoverTagger as ht
import regex as re


def list_to_dict_span(string_list, lower=True):
    """
    This function count how often the different protagonist spans,
    appear inside the data, either in their original case or lowercase.
    Use with functions from protagonist_analysis.py to create string_list.

    Parameters:
        string_list: List of protagonist spans in the form of strings.
        lower: Whether the strings should be made lowercase before counting.

    Returns:
        A dictionary where keys are lemmas and values are number of occurences
    """
    if lower:
        string_dict = {}
        for protagonist in string_list:
            if protagonist.lower() in string_dict.keys():
                string_dict[protagonist.lower()] += 1
            else:
                string_dict[protagonist.lower()] = 1
        sorted_dict = {
            k: v for k, v in sorted(
                string_dict.items(), key=lambda item: item[1]
            )
        }

    else:
        string_dict = {}
        for protagonist in string_list:
            if protagonist in string_dict.keys():
                string_dict[protagonist] += 1
            else:
                string_dict[protagonist] = 1
        sorted_dict = {
            k: v for k, v in sorted(
                string_dict.items(), key=lambda item: item[1]
            )
        }

    return sorted_dict


def list_to_dict_lemma(string_list):
    """
    This function count how often the different lemmas appear
    inside the protagonist spans, using HanTa and NLTK.
    Use with functions from protagonist_analysis.py to create string_list.


    Parameters:
        string_list: List of protagonist spans in the form of strings.

    Returns:
        A dictionary where keys are lemmas and values are number of occurences
    """

    tagger = ht.HanoverTagger('morphmodel_ger.pgz')

    string_dict = {}
    for string in string_list:
        for word in nltk.tokenize.word_tokenize(
            string,
            language="German"
        ):
            word = tagger.analyze(word)[0]
            if word in string_dict.keys():
                string_dict[word] += 1
            else:
                string_dict[word] = 1
    sorted_dict = {k: v for k, v in sorted(
            string_dict.items(), key=lambda item: item[1]
        )
    }
    return sorted_dict


def count_pos_freq(spans_dict):
    """
    This function gives a bad approximation for how frequent different POS
    are as heads in protagonist phrases. If it finds a noun or name anywhere
    in the phrase, it is categorized as having a noun/name as head.
    Otherwise, it counts as a phrase with a pronoun at the head.
    Note that this algorithm is VERY IMPRECISE.

    A better workflow is to use list_pos_examples in conjunction with this
    function.
    The other function lists the phrases it categorizes, making it easy to
    spot mistaken categorizations.

    Parameters:
        spans_dict: Dictionary created by list_to_dict_spans#

    Returns:
        Nothing, prints the results to console.
    """

    tagger = ht.HanoverTagger('morphmodel_ger.pgz')

    sum_nouns = 0
    sum_name = 0
    sum_pronouns = 0

    for key in spans_dict:

        for word in nltk.tokenize.word_tokenize(
                key,
                language="German"
        ):
            pos = tagger.analyze(word)[1]
            if pos == "NE":
                sum_name += spans_dict[key]
                break
            elif pos == "NN":
                sum_nouns += spans_dict[key]
                break
        else:
            sum_pronouns += spans_dict[key]

    print("NOMEN: ", str(sum_nouns))
    print("NAMEN: ", str(sum_name))
    print("PRONOMEN: ", str(sum_pronouns))

    return None


def list_pos_examples(string_list, pos):
    """
    Returns a list of phrases that, according to the rudimentary
    algorithm in count_pos_freq(), were categorized as the pos that
    is passed as argument.
    Use to refine the results from count_pos_freq() (see there).

    Parameters:
        string_list: List of protagonist spans in the form of strings
        pos: Part of speech to look for; options are:
            NN (noun), NE (name), P (pronouns)

    Returns:
        List of phrases categorized as heaving a head with the given POS.
    """

    tagger = ht.HanoverTagger('morphmodel_ger.pgz')
    example_list = []

    for phrase in string_list:
        for word in nltk.tokenize.word_tokenize(
                phrase,
                language="German"
        ):
            test = tagger.analyze(word)[1]
            if test == pos:
                example_list.append(phrase)
                break
            if test == "NN" or test == "NE":
                break
            elif pos == "P":
                example_list.append(phrase)

    return example_list
