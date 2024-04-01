"""
This module contains functions to extract certain lingustic forms
from annotations of different categories in a subcorpus.
You can choose to retrieve the counts of types (word forms),
lemmata, or parts of speech.


Author:
Bruno Brocai (bruno.brocai@gs.uni-heidelberg.de)
University of Heidelberg
Research Projekt "Moralisierungen in verschiedenen Wissensdomänen"

TODO:
- Inmprove style (remove code repetition)
- Improve performance (multiple-instance moralizations are tokenized
    multiple times)
- Improve tokenization in type function?
- Add warning if no valid tagger/tokenizer is chosen
- MAKE THE LEMMATA WITH... FUNCTION ITS OWN MODULE
"""


import nltk
import _util_ as util
import _nlp_ as nlp


def check_category(category):
    """Throws an error if the label type is not valid."""
    if not util.valid_category(category):
        raise ValueError("Invalid label type")


def find_phrase_position_nltk(sentence, phrase):
    """Finds the position of a phrase in a sentence.

    Args:
        sentence (list): A list of tokens in the entire sentence
        phrase (list): A list of tokens, representing phrase to find.

    Returns:
        int: The position of the phrase in the sentence.
            -1 if the phrase is not found.
    """

    for i in range(len(sentence)):
        if sentence[i:i + len(phrase)] == phrase:
            return i

    return -1


def find_phrase_position_spacy(sentence, phrase):
    """Finds the position of a phrase in a sentence.

    Args:
        sentence (list): A list of tokens in the entire sentence
        phrase (list): A list of tokens, representing phrase to find.

    Returns:
        int: The position of the phrase in the sentence.
            -1 if the phrase is not found.
    """

    phrase_tokens = [token.text for token in phrase]

    for i in range(len(sentence) - len(phrase_tokens) + 1):
        ngram = [token.text for token in sentence[i:i + len(phrase_tokens)]]
        if ngram == phrase_tokens:
            return i

    return -1


def get_relevant_tags_hanta(
    moralization,
    instance,
    subcorpus,
    language,
    tagger
):
    """Using HanTa, this function retrieves the tags for a phrase
    inside a moralization.

    Args:
        moralization (tuple): Slice of the moralization in the subcorpus
            text.
        instance (tuple): Slice of the annotated phrase in the subcorpus text.
        subcorpus (Subcorpus): The subcorpus object.
        language (str): The language of the subcorpus.
        tagger (HanTa): The HanTa tagger object.

    Returns:
        list: A list of tuples with the tags of the instance.
    """

    tokenized_sent = nltk.tokenize.word_tokenize(
        util.get_span(subcorpus.text, moralization),
        language=language
    )
    tokenized_instance = nltk.tokenize.word_tokenize(
        util.get_span(subcorpus.text, instance['Coordinates']),
        language=language
    )

    instance_position = find_phrase_position_nltk(
        tokenized_sent,
        tokenized_instance)

    tags = tagger.tag_sent(tokenized_sent)

    instance_tags = tags[
        instance_position:
        len(tokenized_instance)+instance_position
    ]
    return instance_tags


def get_relevant_tags_spacy(
    moralization,
    instance,
    subcorpus,
    tagger
):
    """Using Spacy, this function retrieves the tags for a phrase
    inside a moralization.

    Args:
        moralization (tuple): Slice of the moralization in the subcorpus
            text.
        instance (tuple): Slice of the annotated phrase in the subcorpus text.
        subcorpus (Subcorpus): The subcorpus object.
        tagger (Spacy): The Spacy tagger object.

    Returns:
        list: A list of tuples with the tags of the instance.
    """

    tokenized_sent = tagger(
        util.get_span(subcorpus.text, moralization)
    )
    tokenized_instance = tagger(
        util.get_span(subcorpus.text, instance['Coordinates'])
    )

    instance_position = find_phrase_position_spacy(
        tokenized_sent,
        tokenized_instance)

    instance_tags = tokenized_instance[
        instance_position:
        len(tokenized_instance)+instance_position
    ]
    return instance_tags


def types_in_annotation_subsubcorpus(
    category,
    language,
    subcorpus,
    tokenizer="Spacy"
):
    """Creates a word frequency dictionary for all types (word forms)
    in an annotation category.

    Args:
        category (str): The annotation category to analyze.
        language (str): The language of the subcorpus.
        subcorpus (Subcorpus): The subcorpus object.
        tokenizer (str): The tokenizer to use. Default is "Spacy",
            alternative is "NLTK".

    Returns:
        dict: A dictionary with the types as keys and the counts as values.
    """
    check_category(category)

    label = getattr(subcorpus, category)

    types_dict = {}

    if tokenizer.lower() == "nltk":
        language = nlp.init_nltk_language(language)
        for instance in label:
            text = util.get_span(subcorpus.text, instance['Coordinates'])
            tokenized = nltk.tokenize.word_tokenize(text, language=language)

            for token in tokenized:
                if token not in types_dict:
                    types_dict[token] = 1
                else:
                    types_dict[token] += 1

    elif tokenizer.lower() == "spacy":
        tagger = nlp.init_spacy(language)

        for instance in label:
            tokenized = tagger(util.get_span(
                subcorpus.text, instance['Coordinates'])
            )

            for token in tokenized:
                if token not in types_dict:
                    types_dict[token] = 1
                else:
                    types_dict[token] += 1

    # Sort dictionary by values
    types_dict = dict(
        sorted(types_dict.items(), key=lambda item: item[1])
    )

    return types_dict


def lemmata_in_annotation_subsubcorpus(
    category,
    language,
    subcorpus,
    tagger="Spacy"
):
    """Creates a lemma frequency dictionary for all lemmata in an annotation
    category.

    Args:
        category (str): The annotation category to analyze.
        language (str): The language of the subcorpus.
        subcorpus (Subcorpus): The subcorpus object.
        tagger (str): The tagger to use. Default is "Spacy",
            alternative is "HanTa".

    Returns:
        dict: A dictionary with the lemmata as keys and the counts as values.
    """

    check_category(category)

    label = getattr(subcorpus, category)
    association = util.label_associations_category(
        subcorpus.moralizations,
        label
    )

    lemma_dict = {}

    if tagger.lower() == "hanta":
        tagger, language = nlp.init_hanta_nltk(language)

        for moralization, instances in association.items():
            for instance in instances:
                instance_tags = get_relevant_tags_hanta(
                    moralization,
                    instance,
                    subcorpus,
                    language,
                    tagger
                )

                for tag in instance_tags:
                    if tag[1] not in lemma_dict:
                        lemma_dict[tag[1]] = 1
                    else:
                        lemma_dict[tag[1]] += 1

    elif tagger.lower() == "spacy":

        tagger = nlp.init_spacy(language)

        for moralization, instances in association.items():
            for instance in instances:
                instance_tags = get_relevant_tags_spacy(
                    moralization,
                    instance,
                    subcorpus,
                    tagger
                )

                for tag in instance_tags:
                    if tag.lemma_ not in lemma_dict:
                        lemma_dict[tag.lemma_] = 1
                    else:
                        lemma_dict[tag.lemma_] += 1

    # Sort dictionary by values
    lemma_dict = dict(
        sorted(lemma_dict.items(), key=lambda item: item[1])
    )

    return lemma_dict


def pos_in_annotation_subsubcorpus(
    pos_list,
    category,
    language,
    subcorpus,
    tagger="Spacy"
):
    """Creates a dictionary with all words that
    1) appear in the annotation category
    2) have a POS tag from the pos_list.

    Args:
        pos_list (list): A list of POS tags to look for.
        category (str): The annotation category to analyze.
        language (str): The language of the subcorpus.
        subcorpus (Subcorpus): The subcorpus object.
        tagger (str): The tagger to use. Default is "Spacy",
            alternative is "HanTa".

    Returns:
        dict: A dictionary with the lemmata as keys and the counts as values.
    """

    check_category(category)

    label = getattr(subcorpus, category)
    association = util.label_associations_category(
        subcorpus.moralizations,
        label
    )

    lemma_dict = {}

    if tagger.lower() == "hanta":
        tagger, language = nlp.init_hanta_nltk(language)

        for moralization, instances in association.items():
            for instance in instances:
                instance_tags = get_relevant_tags_hanta(
                    moralization,
                    instance,
                    subcorpus,
                    language,
                    tagger
                )

                for tag in instance_tags:
                    if tag[2] in pos_list and tag[1] not in lemma_dict:
                        lemma_dict[tag[1]] = 1
                    elif tag[2] in pos_list:
                        lemma_dict[tag[1]] += 1

    elif tagger.lower() == "spacy":

        tagger = nlp.init_spacy(language)

        for moralization, instances in association.items():
            for instance in instances:
                instance_tags = get_relevant_tags_spacy(
                    moralization,
                    instance,
                    subcorpus,
                    tagger
                )

                for tag in instance_tags:
                    if tag.pos_ in pos_list and tag.lemma_ not in lemma_dict:
                        lemma_dict[tag.lemma_] = 1
                    elif tag.pos_ in pos_list:
                        lemma_dict[tag.lemma_] += 1

    lemma_dict = dict(
        sorted(lemma_dict.items(), key=lambda item: item[1])
    )

    return lemma_dict


def lemmata_with_annotations(
    category,
    language,
    subcorpus,
    tagger="Spacy"
):
    """Creates a dictionary with all lemmata that appear in the annotation
    and the labels that were assigned to them as values.

    Args:
        category (str): The annotation category to analyze.
        language (str): The language of the subcorpus.
        subcorpus (Subcorpus): The subcorpus object.
        tagger (str): The tagger to use. Default is "Spacy",
            alternative is "HanTa".

    Returns:
        dict: A dictionary with the lemmata as keys and a list of strs
            with the instances as values.
    """

    check_category(category)

    association = util.label_associations_category(
        subcorpus.moralizations,
        getattr(subcorpus, category)
    )

    lemma_dict = {}

    if tagger.lower() == "hanta":
        tagger, language = nlp.init_hanta_nltk(language)

        for moralization, instances in association.items():
            for instance in instances:
                instance_tags = get_relevant_tags_hanta(
                    moralization,
                    instance,
                    subcorpus,
                    language,
                    tagger
                )

                for tag in instance_tags:
                    if tag[1] not in lemma_dict:
                        lemma_dict[tag[1]] = [1, [instance]]
                    else:
                        lemma_dict[tag[1]][0] += 1
                        lemma_dict[tag[1]][1].append(instance)

    else:
        tagger = nlp.init_spacy(language)

        for moralization, instances in association.items():
            for instance in instances:
                instance_tags = get_relevant_tags_spacy(
                    moralization,
                    instance,
                    subcorpus,
                    tagger
                )

                for tag in instance_tags:
                    if tag.lemma_ not in lemma_dict:
                        lemma_dict[tag.lemma_] = [1, [instance]]
                    else:
                        lemma_dict[tag.lemma_][0] += 1
                        lemma_dict[tag.lemma_][1].append(instance)

    return lemma_dict
