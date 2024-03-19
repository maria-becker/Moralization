from enum import Enum


class TagForm(Enum):
    WRITTEN_NAME_ENGLISH = 'name'
    TWO_DIGIT_ISO639_1_ENGLISH = 'iso639_1'
    THREE_DIGIT_ISO639_2T_NATIONAL = 'iso639_2T'
    THREE_DIGIT_ISO639_2B_ENGLISH = 'iso639_2B'


dict_english = {
        'name': 'english',
        'german': 'Englisch',
        'iso639_1': 'en',
        'iso639_2T': 'eng',
        'iso639_2B': 'eng',
        'country_specific': ['en_US', 'en_GB', 'en_AU', 'en_CA']
}
dict_german = {
        'name': 'german',
        'german': 'Deutsch',
        'iso639_1': 'de',
        'iso639_2T': 'deu',
        'iso639_2B': 'ger',
        'country_specific': ['de_DE', 'de_AT', 'de_CH']
}
dict_french = {
        'name': 'french',
        'german': 'Französisch',
        'iso639_1': 'fr',
        'iso639_2T': 'fra',
        'iso639_2B': 'fre',
        'country_specific': ['fr_FR', 'fr_CA', 'fr_BE']
}
dict_italian = {
        'name': 'italian',
        'german': 'Italienisch',
        'iso639_1': 'it',
        'iso639_2T': 'ita',
        'iso639_2B': 'ita',
        'country_specific': ['it_IT', 'it_CH']
}
dict_spanish = {
        'name': 'spanish',
        'german': 'Spanisch',
        'iso639_1': 'es',
        'iso639_2T': 'spa',
        'iso639_2B': 'spa',
        'country_specific': ['es_ES', 'es_MX', 'es_AR']
}


# to add support for another language, create a dict like above and add it here
language_tag_dicts = [
        dict_english, dict_german, dict_french, dict_spanish, dict_italian
]

def get_language_tag(language: str, form: TagForm):

    """
    Retrieve the language tag information for a specified language and form.

    This function searches through a predefined list of language dictionaries. Each dictionary
    contains various abbreviations for a language, such as its written name,
    ISO 639-1 two-letter code, ISO 639-2/T and ISO 639-2/B three-letter codes, and country-specific codes.
    The function returns the information corresponding to the requested form.

    Parameters:
    - language (str): The language to search for. This can be a name or an ISO code.
    - form (TagForm): An enum member representing the form in which the tag information is requested.
                    It can be TagForm.WRITTEN_NAME, TagForm.TWO_DIGIT_ISO639_1,
                    TagForm.THREE_DIGIT_ISO639_2T, or TagForm.THREE_DIGIT_ISO639_2B.

    Returns:
    - str: The requested tag information for the specified language.

    Raises:
    - ValueError: If the given language tag does not match any language in the predefined list.

    How to use:

    from language_tag_manager import get_language_tag, TagForm
    print(get_language_tag('de', form=TagForm.WRITTEN_NAME))

    'german'

    """

    for language_dict in language_tag_dicts:
        if language in language_dict.values():
            # If a match is found, return the value associated with the 'form' key.
            return language_dict.get(form.value, None)
    # If no match is found, throw an error
    error_message = "The given language tag `" + language + "` does not match any language. \nIf this is not a typo, consider adding your desired language to the language tag dictionaries in language_tag_manager.py."
    raise ValueError(error_message)


if __name__ == '__main__':
    test_language_tag = 'german'
    print(get_language_tag('deu', form=TagForm.WRITTEN_NAME_ENGLISH))
