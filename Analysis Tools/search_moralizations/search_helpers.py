import sys
from HanTa import HanoverTagger as ht
import spacy

sys.path.append("../_utils_")
import xmi_analysis_util as xau
import language_tag_manager as langtag


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
    nltk_language = langtag.get_language_tag(
        language, langtag.TagForm.ENGLISH_NAME
    )

    return tagger, nltk_language


def init_spacy(language):
    """Initializes a spacy model for a given language."""

    language = langtag.get_language_tag(
        language, langtag.TagForm.ISO639_1
    )

    nlp = spacy.load(f'{language}_core_news_lg')

    return nlp


def highlighted_relevant_strings(text, relevant_spans_dict):
    return_strings = []
    for moralization, relevant_instances in relevant_spans_dict.items():
        if relevant_instances != []:
            for instance in relevant_instances:
                if xau.get_span(text, instance):
                    text = "".join((
                        text[:(instance[0])],
                        xau.special_upper(xau.get_span(text, instance)),
                        text[(instance[1]):]
                    ))
            output_string = xau.get_span(text, moralization)
            return_strings.append(output_string)
    return return_strings


def relevant_strings(text, relevant_spans):
    return_strings = []
    for moralization in relevant_spans:
        return_strings.append(
            xau.get_span(text, moralization)
        )
    return return_strings
