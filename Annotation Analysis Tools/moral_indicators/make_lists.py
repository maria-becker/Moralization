import corpus_extraction as ce
import nltk
import spacy
from HanTa import HanoverTagger as ht
import xmi_analysis_util as xau

def tokens_in_annotations(
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
    token_dict = {k: v for k, v in sorted(token_dict.items(), key=lambda item: item[1])}

    return token_dict


def find_phrase_position(sentence, phrase):
    for i in range(len(sentence)):
        if sentence[i:i + len(phrase)] == phrase:
            return i

    # Return -1 if the phrase is not found in the sentence
    return -1


def lemmata_in_annotations(
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
                    xau.get_span(corpus.text, moralization), language=language)
                tokenized_instance = nltk.tokenize.word_tokenize(
                    xau.get_span(corpus.text, instance['Coordinates']), language=language)
                instance_position = find_phrase_position(tokenized_sent, tokenized_instance)
                
                tags = tagger.tag_sent(tokenized_sent)

                for tag in tags[instance_position:len(tokenized_instance)+instance_position]:
                    if tag[1] not in lemma_dict:
                        lemma_dict[tag[1]] = 1
                    else:
                        lemma_dict[tag[1]] += 1

    # Sort dictionary by values
    lemma_dict = {k: v for k, v in sorted(lemma_dict.items(), key=lambda item: item[1])}

    return lemma_dict


def pos_lemmata_in_annotations(
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
                    xau.get_span(corpus.text, moralization), language=language)
                tokenized_instance = nltk.tokenize.word_tokenize(
                    xau.get_span(corpus.text, instance['Coordinates']), language=language)
                instance_position = find_phrase_position(tokenized_sent, tokenized_instance)
                
                tags = tagger.tag_sent(tokenized_sent)

                for tag in tags[instance_position:len(tokenized_instance)+instance_position]:
                    if tag[2] in pos_list:
                        if tag[1] not in lemma_dict:
                            lemma_dict[tag[1]] = 1
                        else:
                            lemma_dict[tag[1]] += 1

    # Sort dictionary by values
    lemma_dict = {k: v for k, v in sorted(lemma_dict.items(), key=lambda item: item[1])}

    return lemma_dict
