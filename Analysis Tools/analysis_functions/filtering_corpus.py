"""
Look for moralizations in the corpus that match specific criteria.
For example, all protagonists that contain proper nouns or all
moral values with the Lemma "Gerechtigkeit".

Author:
Bruno Brocai (bruno.brocai@gs.uni-heidelberg.de)
University of Heidelberg
Research Projekt "Moralisierungen in verschiedenen Wissensdomänen"

TODO:
- Add tokenization for the type function
"""


import filtering_subcorpus
import _util_ as util


def lemmata_category_instances(
    corpus,
    lemmata,
    category,
    tagger="Spacy",
    export=False
):
    """Look for a list of lemmata in specific annotation types in the corpus.

    Args:
        corpus (Corpus): The corpus object.
        lemma (str): The lemmata to look for.
        category (str): The annotation category to search in.
        tagger (str): The tagger to use. Default is "Spacy",
            alternative is "Hanta".
        export (bool): If True, the results are exported to an Excel file.

    Returns:
        dict: A dictionary with the subcorpora as keys and a list of strs
            with the instances as values.
    """

    output_dict = {}
    for subcorp in corpus.collection.keys():
        output_dict[subcorp] = filtering_subcorpus.lemmata_category_instances(
            corpus.collection[subcorp],
            lemmata,
            category,
            language=corpus.language,
            tagger=tagger,
            export=False
        )

    if export:
        util.dict_to_xlsx(
            output_dict,
            f"{lemmata}_{category}_instances.xlsx"
        )

    return output_dict


def pos_category_instances(
    corpus,
    pos,
    category,
    tagger="Spacy",
    export=False
):
    """Look for a specific part of speech in specific annotation categories
    in the corpus.

    Args:
        corpus (Corpus): The corpus object.
        pos (str): The part of speech to look for.
        category (str): The annotation category to search in.
        tagger (str): The tagger to use. Default is "Spacy", alternative
            is "Hanta".
        export (bool): If True, the results are exported to an Excel file.

    Returns:
        dict: A dictionary with the subcorpora as keys and a list of strs
            with the instances as values.
    """

    output_dict = {}
    for subcorpus in corpus.collection.keys():
        output_dict[subcorpus] = filtering_subcorpus.pos_category_instances(
            corpus.collection[subcorpus],
            pos,
            category,
            language=corpus.language,
            tagger=tagger,
            export=False
        )

    if export:
        util.dict_to_xlsx(
            output_dict,
            f"{pos}_{category}_instances.xlsx"
        )

    return output_dict


def poslist_category_instances(
    corpus,
    pos_list,
    category,
    tagger="Spacy",
    export=False
):
    """Look for instances of annotated spans in a specific category
    where at least one POS from the pos_list is present.

    Args:
        corpus (Corpus): The corpus object.
        pos_list (list): A list of POS tags to look for.
        category (str): The annotation category to search in.
        tagger (str): The tagger to use. Default is "Spacy", alternative
            is "Hanta".
        export (bool): If True, the results are exported to an Excel file.

    Returns:
        dict: A dictionary with the subcorpora as keys and a list of strs
            with the instances as values.
    """

    output_dict = {}
    for subcorp in corpus.collection.keys():
        output_dict[subcorp] = filtering_subcorpus.poslist_category_instances(
            corpus.collection[subcorp],
            pos_list,
            category,
            language=corpus.language,
            tagger=tagger,
            export=False
        )

    if export:
        util.dict_to_xlsx(
            output_dict,
            f"[{pos_list[1]}, ...]_{category}_instances.xlsx"
        )

    return output_dict


def count_category_instances(
    corpus,
    count,
    category,
    export=False
):
    """Look for moralizations where a specific category occurs exactly
    count times, e.g. 5 protagonists.

    Args:
        corpus (Corpus): The corpus object.
        count (int): The number of instances to look for.
        category (str): The annotation category to search in.
        export (bool): If True, the results are exported to an Excel file.

    Returns:
        dict: A dictionary with the subcorpora as keys and a list of strs
            with the instances as values.
    """

    output_dict = {}
    for subcorpus in corpus.collection.keys():
        output_dict[subcorpus] = filtering_subcorpus.count_category_instances(
            corpus.collection[subcorpus],
            count,
            category,
            export=False
        )

    if export:
        util.dict_to_xlsx(
            output_dict,
            f"{str(count)}_{category}_instances.xlsx"
        )

    return output_dict


def label_category_instances(
    corpus,
    label,
    category,
    export=False
):
    """Find all instances of a specific label inside a category
    (such as "Harm" or "Benefizient:in").

    Args:
        corpus (Corpus): The corpus object.
        label (str): The label to search for.
        category (str): The category to search in.
        export (bool): If True, the results will be exported to an Excel file.

    Returns:
        dict: A dictionary with the subcorpora as keys and a list of strs
            with the instances as values.
    """
    output_dict = {}
    for subcorpus in corpus.collection.keys():
        output_dict[subcorpus] = filtering_subcorpus.tag_category_instances(
            corpus.collection[subcorpus],
            label,
            category,
            export=False
        )

    if export:
        util.dict_to_xlsx(
            output_dict,
            f"{label}_{category}_instances.xlsx"
        )

    return output_dict


def type_category_instances(
    corpus,
    type_,
    category,
    export=False
):
    """Look for instances of a specific type (word form)
    in a specific category.

    Args:
        corpus (Corpus): The corpus object.
        type (str): The type to search for.
        category (str): The category to search in.
        export (bool): If True, the results will be exported to an Excel file.

    Returns:
        dict: A dictionary with the subcorpora as keys and a list of strs
            with the instances as values.
    """

    output_dict = {}
    for subcorpus in corpus.collection.keys():
        output_dict[subcorpus] = filtering_subcorpus.token_category_instances(
            corpus.collection[subcorpus],
            type_,
            category,
            export=False
        )

    if export:
        util.dict_to_xlsx(
            output_dict,
            f"{type_}_{category}_instances.xlsx"
        )

    return output_dict
