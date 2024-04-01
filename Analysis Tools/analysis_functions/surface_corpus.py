"""
This module provides functions that can be used to retrieve data about
the linguistic surface of a corpus (a collection of xmi-based subcorpora).

It allows one to collect the counts of all word forms (lemmatized or not)
and parts of speech.

You can also retrieve all passages that were marked as non-moralizing or
moralizing, both from the corpora and the xlsx files used for pre-filtering.

Author:
Bruno Brocai (bruno.brocai@gs.uni-heidelberg.de)
University of Heidelberg
Research Projekt "Moralisierungen in verschiedenen Wissensdomänen"
"""


import re
from . import surface_sents_subcorpus
from . import surface_words_subcorpus
from . import _util_ as util


def add_dicts(dict1, dict2):
    """Adds the values of two dictionaries together."""
    for key in dict2:
        if key in dict1:
            dict1[key] += dict2[key]
        else:
            dict1[key] = dict2[key]
    return dict1


def tokens_in_annotation(
    category,
    language,
    corpus,
    tokenizer="Spacy",
    lower=False
):
    """Counts the occurences of tokens in each subcorpus and adds them up.

    If lower is True, the tokens are converted to lowercase.

    Args:
        category (str): The annotation category of the annotation,
            e.g., "all_morals".
        language (str): The language of the corpus.
        corpus (Corpus): The corpus object, containing one or more subcorpora.
        tokenizer (str): The tokenizer to use. Default is "Spacy", alternative
            is "NLTK".
        lower (bool): If True, the tokens are converted to lowercase.
            Default is False.

    Returns:
        dict: A dictionary with the tokens as keys and the counts as values.
    """

    tokens = {}
    for subcorpus in corpus.collection.values():
        temp_dict = surface_words_subcorpus.types_in_annotation_subsubcorpus(
            category,
            language,
            subcorpus,
            tokenizer=tokenizer
        )
        tokens = add_dicts(tokens, temp_dict)

    if lower:
        lower_tokens = {}
        for token, count in tokens:
            if token.lower() in lower_tokens:
                lower_tokens[token.lower()] += count
            else:
                lower_tokens[token.lower()] = count
        return lower_tokens

    return tokens


def lemmata_in_annotation(
    category,
    language,
    corpus,
    tagger="Spacy"
):
    """Counts the occurences of lemma in each subcorpus and adds them up.

    Args:
        category (str): The annotation category of the annotation,
            e.g., "all_morals".
        language (str): The language of the corpus.
        corpus (Corpus): The corpus object, containing one or more subcorpora.
        tagger (str): The tagger to use. Default is "Spacy", alternative
            is "NLTK".

    Returns:
        dict: A dictionary with the lemmata as keys and the counts as values.
    """

    lemmata = {}
    for subcorpus in corpus.collection.values():
        temp_dict = surface_words_subcorpus.lemmata_in_annotation_subsubcorpus(
            category,
            language,
            subcorpus,
            tagger
        )
        lemmata = add_dicts(lemmata, temp_dict)

    return lemmata


def pos_in_annotation(
    pos_list,
    category,
    language,
    corpus,
    tagger="Spacy"
):
    """Counts the occurences of Parts of Speech (POS) in each subcorpus
    and adds them up.

    Args:
        pos_list (list): A list of POS tags to count.
        category (str): The annotation category of the annotation,
            e.g., "all_morals".
        language (str): The language of the corpus.
        corpus (Corpus): The corpus object, containing one or more subcorpora.
        tagger (str): The tagger to use. Default is "Spacy", alternative
            is "NLTK".

    Returns:
        dict: A dictionary with the lemmata as keys and the counts as values.
    """

    pos = {}
    for subcorpus in corpus.collection.values():
        temp_dict = surface_words_subcorpus.pos_in_annotation_subsubcorpus(
            pos_list,
            category,
            language,
            subcorpus,
            tagger
        )
        pos = add_dicts(pos, temp_dict)

    return pos


def list_nonmoral_strings_from_corpus(
    corpus,
    metadata_regex=None
):
    """Lists all passages in the corpus that were marked as non-moralizing.

    Args:
        corpus (Corpus): The corpus object, containing one or more subcorpora.
        metadata_regex (str): A regular expression that is used to remove
            metadata from the text. Default is None.

    Returns:
        list: A list of strings that were marked as non-moralizing.
    """

    corpus.filter_in("detailed_moralizations", ["Keine Moralisierung"])
    nonmoral_texts = []
    for subcorpus in corpus.collection.values():
        for span in subcorpus.detailed_moralizations:
            span_text = util.get_span(subcorpus.text, span['Coordinates'])
            if metadata_regex:
                span_text = re.sub(metadata_regex, '', span_text)
            nonmoral_texts.append(span_text)
    return nonmoral_texts


def list_nonmoral_strings_from_xlsx(
    filepath,
    sheet_names,
    categories=None,
):
    """List all passages in an xslx file that were marked as non-moralizing,
    ambiguous, uninterpretable, or, though this makes little sense, moralizing.

    What passages you get depends on the list of categories you provide, where
    0 is non-moralizing, 1 ambiguous, 2 uninterpretable, and 3 moralizing.

    Args:
        filepath (str): The path to the xlsx file.
        sheet_names (list): A list of sheet names (specifying the genre).
        categories (list): A list of categories. Default is [0, 1, 2].

    Returns:
        list: A list of strings that were marked as non-moralizing.
    """

    nonmoral_texts = []
    for sheet in sheet_names:
        temp_list = surface_sents_subcorpus.list_nonmoral_strings_from_xlsx(
            filepath,
            sheet,
            categories
        )
        nonmoral_texts += temp_list
    return nonmoral_texts


def list_moralization_strings_from_corpus(
    corpus
):
    """Lists all passages in the corpus that were marked as moralizing.

    Args:
        corpus (Corpus): The corpus object, containing one or more subcorpora.

    Returns:
        list: A list of strings that were marked as moralizing.
    """

    moralizations = []
    for subcorpus in corpus.collection.values():
        temp_list = surface_sents_subcorpus.list_moral_strings_from_subcorpus(
            subcorpus
        )
        moralizations += temp_list

    return moralizations
