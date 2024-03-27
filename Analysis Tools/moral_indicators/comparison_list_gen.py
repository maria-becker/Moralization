import sys
import nltk
import spacy
import pandas as pd
from HanTa import HanoverTagger as ht

sys.path.append('../_utils_')
import xmi_analysis_util as xau


def tokens_in_annotation_subcorpus(
        label_type,
        language,
        corpus
):
    if not xau.valid_category(label_type):
        return

    label = getattr(corpus, label_type)

    token_dict = {}

    for instance in label:
        text = xau.get_span(corpus.text, instance['Coordinates'])
        tokenized = nltk.tokenize.word_tokenize(text, language=language)
        tokenized = [word.lower() for word in tokenized]

        for token in tokenized:
            if token not in token_dict:
                token_dict[token] = 1
            else:
                token_dict[token] += 1

    # Sort dictionary by values
    token_dict = dict(
        sorted(token_dict.items(), key=lambda item: item[1])
    )

    return token_dict


def find_phrase_position_hanta(sentence, phrase):
    for i in range(len(sentence)):
        if sentence[i:i + len(phrase)] == phrase:
            return i

    return -1


def find_phrase_position_spacy(sentence, phrase):
    phrase_tokens = [token.text for token in phrase]

    for i in range(len(sentence) - len(phrase_tokens) + 1):
        ngram = [token.text for token in sentence[i:i + len(phrase_tokens)]]
        if ngram == phrase_tokens:
            return i

    return -1


def lemmata_in_annotation_subcorpus(
        label_type,
        language,
        corpus,
        hanta=False
):
    if not xau.valid_category(label_type):
        return

    label = getattr(corpus, label_type)
    association = xau.label_associations_category(
        corpus.moralizations,
        label
    )

    lemma_dict = {}

    if (language == "de" or language == "en") and hanta:

        if language == "de":
            tagger = ht.HanoverTagger('morphmodel_ger.pgz')
            language = 'german'
        elif language == "en":
            tagger = ht.HanoverTagger('morphmodel_en.pgz')
            language = 'english'

        for moralization, instances in association.items():
            for instance in instances:
                tokenized_sent = nltk.tokenize.word_tokenize(
                    xau.get_span(corpus.text, moralization),
                    language=language
                )
                tokenized_instance = nltk.tokenize.word_tokenize(
                    xau.get_span(corpus.text, instance['Coordinates']),
                    language=language
                )

                instance_position = find_phrase_position_hanta(
                    tokenized_sent,
                    tokenized_instance)

                tags = tagger.tag_sent(tokenized_sent)

                relevant_tokens = tags[
                    instance_position:
                    len(tokenized_instance)+instance_position
                ]

                for tag in relevant_tokens:
                    if tag[1] not in lemma_dict:
                        lemma_dict[tag[1]] = 1
                    else:
                        lemma_dict[tag[1]] += 1

    else:

        model = spacy.load(f'{language}_core_news_md')

        for moralization, instances in association.items():
            for instance in instances:
                tokenized_sent = model(
                    xau.get_span(corpus.text, moralization)
                )
                tokenized_instance = model(
                    xau.get_span(corpus.text, instance['Coordinates'])
                )

                instance_position = find_phrase_position_spacy(
                    tokenized_sent,
                    tokenized_instance)

                relevant_tokens = tokenized_instance[
                    instance_position:
                    len(tokenized_instance)+instance_position
                ]

                for tag in relevant_tokens:
                    if tag.lemma_ not in lemma_dict:
                        lemma_dict[tag.lemma_] = 1
                    else:
                        lemma_dict[tag.lemma_] += 1

    # Sort dictionary by values
    lemma_dict = dict(
        sorted(lemma_dict.items(), key=lambda item: item[1])
    )

    return lemma_dict


def pos_in_annotation_subcorpus(
        pos_list,
        label_type,
        language,
        corpus,
        hanta=False
):
    if not xau.valid_category(label_type):
        return

    label = getattr(corpus, label_type)
    association = xau.label_associations_category(
        corpus.moralizations,
        label
    )

    lemma_dict = {}

    if (language == "de" or language == "en") and hanta:

        if language == "de":
            tagger = ht.HanoverTagger('morphmodel_ger.pgz')
            language = 'german'
        elif language == "en":
            tagger = ht.HanoverTagger('morphmodel_en.pgz')
            language = 'english'

        for moralization, instances in association.items():
            for instance in instances:
                tokenized_sent = nltk.tokenize.word_tokenize(
                    xau.get_span(corpus.text, moralization),
                    language=language
                )
                tokenized_instance = nltk.tokenize.word_tokenize(
                    xau.get_span(corpus.text, instance['Coordinates']),
                    language=language
                )
                instance_position = find_phrase_position_hanta(
                    tokenized_sent,
                    tokenized_instance)

                tags = tagger.tag_sent(tokenized_sent)

                relevant_tokens = tags[
                    instance_position:
                    len(tokenized_instance)+instance_position
                ]

                for tag in relevant_tokens:
                    if tag[2] in pos_list:
                        if tag[1] not in lemma_dict:
                            lemma_dict[tag[1]] = 1
                        else:
                            lemma_dict[tag[1]] += 1

    else:

        model = spacy.load(f'{language}_core_news_md')

        for moralization, instances in association.items():
            for instance in instances:
                tokenized_sent = model(
                    xau.get_span(corpus.text, moralization)
                )
                tokenized_instance = model(
                    xau.get_span(corpus.text, instance['Coordinates'])
                )
                instance_position = find_phrase_position_spacy(
                    tokenized_sent,
                    tokenized_instance)

                relevant_tokens = tokenized_instance[
                    instance_position:
                    len(tokenized_instance)+instance_position
                ]

                for tag in relevant_tokens:
                    if tag.pos_ in pos_list:
                        if tag.lemma_ not in lemma_dict:
                            lemma_dict[tag.lemma_] = 1
                        else:
                            lemma_dict[tag.lemma_] += 1

    lemma_dict = dict(
        sorted(lemma_dict.items(), key=lambda item: item[1])
    )

    return lemma_dict


def lemmata_with_annotations(
        label_type,
        language,
        corpus,
        hanta=False
):
    if not xau.valid_category(label_type):
        return

    label = getattr(corpus, label_type)
    association = xau.label_associations_category(
        corpus.moralizations,
        label
    )

    lemma_dict = {}

    if (language == "de" or language == "en") and hanta:

        if language == "de":
            tagger = ht.HanoverTagger('morphmodel_ger.pgz')
            language = 'german'
        elif language == "en":
            tagger = ht.HanoverTagger('morphmodel_en.pgz')
            language = 'english'

        for moralization, instances in association.items():
            for instance in instances:
                tokenized_sent = nltk.tokenize.word_tokenize(
                    xau.get_span(corpus.text, moralization),
                    language=language
                )
                tokenized_instance = nltk.tokenize.word_tokenize(
                    xau.get_span(corpus.text, instance['Coordinates']),
                    language=language
                )

                instance_position = find_phrase_position_hanta(
                    tokenized_sent,
                    tokenized_instance)

                tags = tagger.tag_sent(tokenized_sent)

                relevant_tokens = tags[
                    instance_position:
                    len(tokenized_instance)+instance_position
                ]

                for tag in relevant_tokens:
                    if tag[1] not in lemma_dict:
                        lemma_dict[tag[1]] = [1, [instance]]
                    else:
                        lemma_dict[tag[1]][0] += 1
                        lemma_dict[tag[1]][1].append(instance)

    else:

        model = spacy.load(f'{language}_core_news_md')

        for moralization, instances in association.items():
            for instance in instances:
                tokenized_sent = model(
                    xau.get_span(corpus.text, moralization)
                )
                tokenized_instance = model(
                    xau.get_span(corpus.text, instance['Coordinates'])
                )

                instance_position = find_phrase_position_spacy(
                    tokenized_sent,
                    tokenized_instance)

                relevant_tokens = tokenized_instance[
                    instance_position:
                    len(tokenized_instance)+instance_position
                ]

                for tag in relevant_tokens:
                    if tag.lemma_ not in lemma_dict:
                        lemma_dict[tag.lemma_] = [1, [instance]]
                    else:
                        lemma_dict[tag.lemma_][0] += 1
                        lemma_dict[tag.lemma_][1].append(instance)

    return lemma_dict
