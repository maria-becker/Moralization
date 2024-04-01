"""
Utility module used by different other modules. Makes initializing
taggers/tokenizers easier and can handle different languages,
no matter in which format they are represented.

Author:
Bruno Brocai (bruno.brocai@gs.uni-heidelberg.de)
University of Heidelberg
Research Projekt "Moralisierungen in verschiedenen Wissensdomänen"
"""


import spacy
from HanTa import HanoverTagger as ht
from . import _language_tag_manager as langtag


def init_nltk_language(language):
    """Initializes a NLTK language tag for a given language."""

    language = langtag.get_language_tag(
        language, langtag.TagForm.NAME_ENGLISH
    )

    return language


def init_hanta_nltk(language):
    """Initializes a Hanover Tagger and a NLTK language tag
    for a given language.
    """

    language = langtag.get_language_tag(
        language, langtag.TagForm.HANTA
    )

    if language not in ("ger", "en"):
        raise ValueError("Hanover Tagger only supports German and English")

    tagger = ht.HanoverTagger(f'morphmodel_{language}.pgz')

    nltk_language = init_nltk_language(language)

    return tagger, nltk_language


def init_spacy(language):
    """Initializes a spacy model for a given language."""

    language = langtag.get_language_tag(
        language, langtag.TagForm.ISO639_1_ENGLISH
    )

    nlp = spacy.load(f'{language}_core_news_lg')

    return nlp
