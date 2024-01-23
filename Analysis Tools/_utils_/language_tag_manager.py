dict_english = {
        'name': 'english',
        'iso639_1': 'en',
        'iso639_2T': 'eng',
        'iso639_2B': 'eng',
        'country_specific': ['en_US', 'en_GB', 'en_AU', 'en_CA']
}
dict_german = {
        'name': 'german',
        'iso639_1': 'de',
        'iso639_2T': 'deu',
        'iso639_2B': 'ger',
        'country_specific': ['de_DE', 'de_AT', 'de_CH']
}
dict_french = {
        'name': 'french',
        'iso639_1': 'fr',
        'iso639_2T': 'fra',
        'iso639_2B': 'fre',
        'country_specific': ['fr_FR', 'fr_CA', 'fr_BE']
}
dict_italian = {
        'name': 'italian',
        'iso639_1': 'it',
        'iso639_2T': 'ita',
        'iso639_2B': 'ita',
        'country_specific': ['it_IT', 'it_CH']
}
dict_spanish = {
        'name': 'spanish',
        'iso639_1': 'es',
        'iso639_2T': 'spa',
        'iso639_2B': 'spa',
        'country_specific': ['es_ES', 'es_MX', 'es_AR']
}

language_tag_dicts = [dict_english, dict_german, dict_french, dict_spanish, dict_italian]

def get_language_tag(language: str, form: str):
    for language_dict in language_tag_dicts:
       if language in language_dict.values():
            # If a match is found, return the value associated with the 'form' key.
            return language_dict.get(form, None)
    # If no match is found, throw an error
    error_message = "The given language tag `" + language + "` does not match any language. \nIf this is not a typo, consider adding your desired language to the language tag dictionaries in language_tag_manager.py."
    raise ValueError(error_message)



if __name__ == '__main__':
    test_language_tag = 'german'
    print(get_language_tag('ddeu', form='iso639_1'))

