import re
import sys
import comparison_corpus_gen
import comparison_list_gen

sys.path.append('../_utils_')
import xmi_analysis_util as xau


def add_dicts(dict1, dict2):
    """
    Adds the values of two dictionaries together.
    """
    for key in dict2:
        if key in dict1:
            dict1[key] += dict2[key]
        else:
            dict1[key] = dict2[key]
    return dict1


def tokens_in_annotation(
    category,
    language,
    corpus
):

    tokens = {}
    for subcorpus in corpus.collection.values():
        temp_dict = comparison_list_gen.tokens_in_annotation_subcorpus(
            category,
            language,
            subcorpus
        )
        tokens = add_dicts(tokens, temp_dict)

    return tokens


def lemmata_in_annotation(
    category,
    language,
    corpus,
    hanta=False
):
    """
    Returns a dictionary with the lemmata in the annotation.
    """

    lemmata = {}
    for subcorpus in corpus.collection.values():
        temp_dict = comparison_list_gen.lemmata_in_annotation_subcorpus(
            category,
            language,
            subcorpus,
            hanta
        )
        lemmata = add_dicts(lemmata, temp_dict)

    return lemmata


def pos_in_annotation(
    pos_list,
    category,
    language,
    corpus,
    hanta=False
):
    """
    Returns a dictionary with the POS tags in the annotation.
    """

    pos = {}
    for subcorpus in corpus.collection.values():
        temp_dict = comparison_list_gen.pos_in_annotation_subcorpus(
            pos_list,
            category,
            language,
            subcorpus,
            hanta
        )
        pos = add_dicts(pos, temp_dict)

    return pos


def list_nonmoral_strings_from_corpus(
    corpus,
    metadata_regex=None
):

    corpus.filter_in("detailed_moralizations", ["Keine Moralisierung"])
    nonmoral_texts = []
    for subcorpus in corpus.collection.values():
        for span in subcorpus.detailed_moralizations:
            span_text = xau.get_span(subcorpus.text, span['Coordinates'])
            if metadata_regex:
                span_text = re.sub(metadata_regex, '', span_text)
            nonmoral_texts.append(span_text)
    return nonmoral_texts


def list_nonmoral_strings_from_xlsx(
    filepath,
    sheet_names,
    categories=None,
):

    nonmoral_texts = []
    for sheet in sheet_names:
        temp_list = comparison_corpus_gen.list_nonmoral_strings_from_xlsx(
            filepath,
            sheet,
            categories
        )
        nonmoral_texts += temp_list
    return nonmoral_texts


def list_moralization_strings_from_corpus(
    corpus
):

    moralizations = []
    for subcorpus in corpus.collection.values():
        temp_list = comparison_corpus_gen.list_moral_strings_from_subcorpus(
            subcorpus
        )
        moralizations += temp_list

    return moralizations
