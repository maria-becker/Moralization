"""
Look for moralizations in a subcorpus that match specific criteria.

Author:
Bruno Brocai (bruno.brocai@gs.uni-heidelberg.de)
University of Heidelberg
Research Projekt "Moralisierungen in verschiedenen Wissensdomänen"

TODO:
- Add tokenization for the type function
"""

import nltk
from . import filter_helpers
from . import _util_ as util
from . import _nlp_ as nlp


def lemmata_category_instances(
    subcorpus,
    lemmata,
    category,
    language="de",
    **kwargs
):
    """Look for a list of lemmatata in specific annotation categories.

    Args:
        subcorpus (Subcorpus): The subcorpus object.
        lemmata (str): The lemmata to look for.
        category (str): The annotation category to search in.
        language (str): The language of the subcorpus. Default is "de".
        hanta (bool): If True, the Hanta tagger is used. Default is False.
        export (bool): If True, the results are exported to an Excel file.
    """

    tagger = kwargs.get('tagger', "Spacy")
    export = kwargs.get('export', False)

    if not util.valid_category(category):
        return None

    label = getattr(subcorpus, category)

    if tagger.lower() == "hanta":
        relevant_spans_dict = hanta_lemmata_category_search(
            subcorpus,
            label,
            lemmata,
            language
        )
    elif tagger.lower() == "spacy":
        relevant_spans_dict = spacy_lemmata_category_search(
            subcorpus,
            label,
            lemmata,
            language
        )
    else:
        raise ValueError("Tagger must be 'HanTa' or 'Spacy'.")

    return_string_list = filter_helpers.highlighted_relevant_strings(
        subcorpus.text,
        relevant_spans_dict
    )

    if export:
        util.list_to_excel(
            return_string_list,
            f"{lemmata}_{category}_instances.xlsx"
        )

    return list(set(return_string_list))


def hanta_lemmata_category_search(
    subcorpus,
    label,
    lemmata,
    language
):
    """Use the Hanta tagger to search for lemmata in a specific category."""

    associations = util.label_associations_category(
        subcorpus.moralizations,
        label
    )

    tagger, language = nlp.init_hanta_nltk(language)

    relevant_spans_dict = {key: [] for key in associations}

    for moralization, instances in associations.items():
        for instance in instances:
            tokenized = nltk.tokenize.word_tokenize(
                util.get_span(subcorpus.text, instance['Coordinates']),
                language=language
            )
            tags = tagger.tag_sent(tokenized)
            for tag in tags:
                if tag[1] == lemmata:
                    relevant_spans_dict[moralization].append(
                        instance['Coordinates']
                    )
                    break

    return relevant_spans_dict


def spacy_lemmata_category_search(subcorpus, label, lemmata, language):
    """Use the Spacy tagger to search for lemmata in a specific category."""

    associations = util.label_associations_category(
        subcorpus.moralizations,
        label
    )

    model = nlp.init_spacy(language)

    relevant_spans_dict = {key: [] for key in associations}

    for moralization, instances in associations.items():
        for instance in instances:
            doc = model(util.get_span(subcorpus.text, instance['Coordinates']))
            for token_ in doc:
                if token_.lemma_ == lemmata:
                    relevant_spans_dict[moralization].append(
                        instance['Coordinates']
                    )
                    break

    return relevant_spans_dict


def poslist_category_instances(
    subcorpus,
    pos_list,
    category,
    language,
    **kwargs
):
    """
    Look for instances of annotated spans in a specific category
    where at least one POS from the pos_list is present.

    Keep in mind that the POS tags are different for the HanTa and Spacy.

    Args:
        subcorpus (Subcorpus): The subcorpus object.
        pos_list (list): A list of POS tags to look for.
        category (str): The annotation category to search in.
        language (str): The language of the subcorpus.
        tagger (str): The tagger to use. Default is "Spacy", alternative
            is "Hanta".
        export (bool): If True, the results are exported to an Excel file.

    Returns:
        list: A list of strings with the relevant instances in uppercase.
    """

    tagger = kwargs.get('tagger', "Spacy")
    export = kwargs.get('export', False)

    if not util.valid_category(category):
        return None

    label = getattr(subcorpus, category)

    if tagger.lower() == "hanta":
        relevant_spans_dict = hanta_poslist_category_search(
            subcorpus,
            label,
            pos_list,
            language
        )

    elif tagger.lower() == "spacy":
        relevant_spans_dict = spacy_poslist_category_search(
            subcorpus,
            label,
            pos_list,
            language
        )
    else:
        raise ValueError("Tagger must be 'HanTa' or 'Spacy'.")

    return_string_list = filter_helpers.highlighted_relevant_strings(
        subcorpus.text,
        relevant_spans_dict
    )

    if export:
        util.list_to_excel(
            return_string_list,
            f"[{pos_list[1]}, ...]_{category}_instances.xlsx"
        )

    return list(set(return_string_list))


def hanta_poslist_category_search(
    subcorpus,
    label,
    pos_list,
    language
):
    """Use the Hanta tagger to search for POS tags in a specific category."""

    associations = util.label_associations_category(
        subcorpus.moralizations,
        label
    )

    tagger, language = nlp.init_hanta_nltk(language)

    relevant_spans_dict = {key: [] for key in associations}

    for moralization, instances in associations.items():
        for instance in instances:
            tokenized = nltk.tokenize.word_tokenize(
                util.get_span(subcorpus.text, instance["Coordinates"]),
                language=language
            )
            tags = tagger.tag_sent(tokenized)
            for tag in tags:
                if tag[2] in pos_list:
                    relevant_spans_dict[moralization].append(
                        instance["Coordinates"]
                    )
                    break

    return relevant_spans_dict


def spacy_poslist_category_search(
    subcorpus,
    label,
    pos_list,
    language
):
    """Use the Spacy tagger to search for POS tags in a specific category."""

    associations = util.label_associations_category(
        subcorpus.moralizations,
        label
    )

    model = nlp.init_spacy(language)

    relevant_spans_dict = {key: [] for key in associations}

    for moralization, instances in associations.items():
        for instance in instances:
            doc = model(util.get_span(subcorpus.text, instance['Coordinates']))
            for token_ in doc:
                if token_.pos_ in pos_list:
                    relevant_spans_dict[moralization].append(
                        instance['Coordinates']
                    )
                    break

    return relevant_spans_dict


def pos_category_instances(
    subcorpus,
    pos,
    category,
    language,
    **kwargs
):
    """Look for instances of one specific POS tag in a specific category.

    Keep in mind that the POS tags are different for the HanTa and Spacy.

    Args:
        subcorpus (Subcorpus): The subcorpus object.
        pos (str): The POS tag to look for.
        category (str): The annotation category to search in.
        language (str): The language of the subcorpus.
        tagger (str): The tagger to use. Default is "Spacy", alternative
            is "Hanta".
        export (bool): If True, the results are exported to an Excel file.

    Returns:
        list: A list of strings with the relevant instances in uppercase.
    """

    hits_list = poslist_category_instances(
        subcorpus,
        [pos],
        category,
        language,
        **kwargs
    )

    return list(set(hits_list))


def tag_category_instances(
    subcorpus,
    label,
    category,
    export=False
):
    """Find all instances of a specific label inside a category
    (such as "Harm" or "Benefizient:in").

    Args:
        subcorpus (subcorpus): The subcorpus object.
        label (str): The label to search for.
        category (str): The category to search in.
        export (bool): If True, the results will be exported to an Excel file.

    Returns:
        list: A list of strings with the relevant instances.
    """

    if not util.valid_category(category):
        return None

    text = subcorpus.text

    labels = getattr(subcorpus, category)

    matched_anno_list = []
    for span in labels:
        if label in span.values():
            matched_anno_list.append(span)

    relevant_spans_dict = util.label_associations(
        subcorpus.moralizations,
        matched_anno_list
    )

    return_string_list = filter_helpers.highlighted_relevant_strings(
        text,
        relevant_spans_dict
    )

    if export:
        util.list_to_excel(
            return_string_list,
            f"{label}_{category}_instances.xlsx"
        )

    return list(set(return_string_list))


def count_category_instances(
    subcorpus,
    count,
    category,
    export=False
):
    """Find all instances of a specific count of annotations in a category."""

    if not util.valid_category(category):
        return None

    label = getattr(subcorpus, category)

    associations = util.label_associations(
        subcorpus.moralizations,
        label
    )

    associations = {
        key: entry for key, entry
        in associations.items()
        if len(entry) == count
    }

    return_strings = filter_helpers.highlighted_relevant_strings(
        subcorpus.text,
        associations,
        allow_zero=True  # To handle count = 0
    )

    if export:
        util.list_to_excel(
            return_strings,
            f"{str(count)}_{category}_instances.xlsx"
        )

    return list(set(return_strings))


def token_category_instances(
    subcorpus,
    token_,
    category,
    lower=False,
    export=False
):
    """Find all instances of a specific token (word form) in a category.

    Args:
        subcorpus (Subcorpus): The subcorpus object.
        token_ (str): The token to search for.
        category (str): The annotation category to search in.
        lower (bool): If True, the search is case-insensitive.
        export (bool): If True, the results are exported to an Excel file.

    Returns:
        list: A list of strings with the relevant instances.
    """

    if not util.valid_category(category):
        return None

    label = getattr(subcorpus, category)

    associations = util.label_associations(
        subcorpus.moralizations,
        label
    )

    relevant_spans_list = []
    text = subcorpus.text
    for moraliz, annotations in associations.items():
        for anno in annotations:
            if lower:
                if token_ in util.get_span(text, anno).lower():
                    relevant_spans_list.append(moraliz)
            elif token_ in util.get_span(text, anno):
                relevant_spans_list.append(moraliz)

    return_string_list = filter_helpers.relevant_strings(
        subcorpus.text,
        relevant_spans_list
    )

    if export:
        util.list_to_excel(
            return_string_list,
            f"{token_}_{category}_instances.xlsx"
        )

    return list(set(return_string_list))
