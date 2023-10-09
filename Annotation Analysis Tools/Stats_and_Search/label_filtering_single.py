import nltk
import xmi_analysis_util as xau
from HanTa import HanoverTagger as ht
import spacy


def lemma_label_instances(
    corpus,
    lemma,
    label_type,
    language="ger",
    export=False
):

    possible_labels = ['obj_morals', 'subj_morals', 'all_morals',
                       'protagonists', 'protagonists_doubles',
                       'com_functions',
                       'expl_demands', 'impl_demands', 'all_demands']
    if label_type not in possible_labels:
        print("Error: label_type must be one of:\n" +
              "\n".join(possible_labels))
        return

    label = getattr(corpus, label_type)

    association = xau.label_associations(
        corpus.moralizations,
        label
    )

    relevant_spans_list = []

    if language == "ger" or language == "en":

        tagger = ht.HanoverTagger(f'morphmodel_{language}.pgz')

        if language == "ger":
            language = "german"
        elif language == "en":
            language = "english"

        for moralization in association.keys():
            for protagonist in association[moralization]:
                tokenized = nltk.tokenize.word_tokenize(
                    xau.get_span(corpus.text, protagonist), language=language)
                tags = tagger.tag_sent(tokenized)
                for tag in tags:
                    if tag[1] == lemma:
                        relevant_spans_list.append(moralization)
                        break

    if language == "fr" or language == "it":

        if language == "fr":
            model = spacy.load('fr_core_news_md')
        elif language == "it":
            model = spacy.load('it_core_news_md')

        for moralization in association.keys():
            for protagonist in association[moralization]:
                doc = model(xau.get_span(corpus.text, protagonist))
                for token in doc:
                    if token.lemma_ == lemma:
                        relevant_spans_list.append(moralization)
                        break

    return_string_list = []
    for moralization in relevant_spans_list:
        return_string_list.append(xau.get_span(corpus.text,
                                               moralization))

    if export:
        xau.list_to_excel(return_string_list,
                          f"{lemma}_{label_type}_instances.xlsx")

    return return_string_list


def poslist_label_instances(
    corpus,
    pos_list,
    label_type,
    language="ger",
    export=False
):

    label_possibilities = ['obj_morals', 'subj_morals', 'all_morals',
                           'protagonists', 'protagonists_doubles',
                           'com_functions',
                           'expl_demands', 'impl_demands', 'all_demands']
    if label_type not in label_possibilities:
        print("Error: label_type must be one of:\n" +
              "\n".join(label_possibilities))
        return
    label = getattr(corpus, label_type)

    association = xau.label_associations_category(
        corpus.moralizations,
        label
    )

    relevant_spans_dict = {}

    if language == "ger" or language == "en":

        tagger = ht.HanoverTagger(f'morphmodel_{language}.pgz')

        if language == "ger":
            language = "german"
        elif language == "en":
            language = "english"

        relevant_spans_list = []

        for moralization in association.keys():

            for protagonist in association[moralization]:

                tokenized = nltk.tokenize.word_tokenize(
                    xau.get_span(corpus.text, moralization), language=language)
                tags = tagger.tag_sent(tokenized)

                for tag in tags:

                    if tag[2] in pos_list and tag[0].lower() in xau.get_span(
                                corpus.text, protagonist["Coordinates"]
                                ).lower():

                        relevant_spans_list.append(protagonist)
                        break

        relevant_spans_dict = xau.label_associations(corpus.moralizations,
                                                     relevant_spans_list)

    if language == "fr" or language == "it":

        if language == "fr":
            model = spacy.load('fr_core_news_md')
        elif language == "it":
            model = spacy.load('it_core_news_md')

        relevant_spans_list = []

        for moralization in association.keys():

            for protagonist in association[moralization]:

                doc = model(xau.get_span(corpus.text, moralization))

                for tag in doc:

                    if tag.pos_ in pos_list and tag.text() in xau.get_span(
                                corpus.text,
                                protagonist["Coordinates"])():

                        relevant_spans_list.append(protagonist)
                        break

        relevant_spans_dict = xau.label_associations(corpus.moralizations,
                                                     relevant_spans_list)

    text = corpus.text
    return_string_list = []
    for moralization_tuple in relevant_spans_dict:
        if relevant_spans_dict[moralization_tuple] != []:
            for protagonist in relevant_spans_dict[moralization_tuple]:
                if xau.get_span(text, protagonist):
                    text = (
                        text[:(protagonist[0])]
                        + xau.special_upper(xau.get_span(text, protagonist))
                        + text[(protagonist[1]):]
                    )
            output_string = xau.get_span(text, moralization_tuple)
            return_string_list.append(output_string)

    if export:
        xau.list_to_excel(return_string_list,
                          f"[{pos_list[1]}, ...]_{label_type}_instances.xlsx")

    return return_string_list


def pos_label_instances(
    corpus,
    pos,
    label_type,
    language="ger",
    export=False
):
    return poslist_label_instances(
        corpus,
        [pos],
        label_type,
        language,
        export
    )


def count_label_instances(
    corpus,
    count,
    label_type,
    export=False
):

    label_possibilities = ['obj_morals', 'subj_morals', 'all_morals',
                           'protagonists', 'protagonists_doubles',
                           'com_functions',
                           'expl_demands', 'impl_demands', 'all_demands']
    if label_type not in label_possibilities:
        print("Error: label_type must be one of:\n" +
              "\n".join(label_possibilities))
        return
    label = getattr(corpus, label_type)

    association = xau.label_associations(
        corpus.moralizations,
        label
    )

    relevant_spans_dict = {
        key: association[key] for key
        in association.keys()
        if len(association[key]) == count
    }

    text = corpus.text
    return_string_list = []
    for moralization_tuple in relevant_spans_dict:
        for protagonist in relevant_spans_dict[moralization_tuple]:
            if xau.get_span(corpus.text, protagonist):
                text = (
                    text[:(protagonist[0])]
                    + xau.special_upper(xau.get_span(corpus.text, protagonist))
                    + text[(protagonist[1]):]
                )
        output_string = xau.get_span(text, moralization_tuple)
        return_string_list.append(output_string)

    if export:
        xau.list_to_excel(return_string_list,
                          f"{str(count)}_{label_type}_instances.xlsx")

    return return_string_list


def tag_label_instances(
    corpus,
    label,
    label_type,
    export=False
):

    text = corpus.text
    label_possibilities = ['obj_morals', 'subj_morals', 'all_morals',
                           'protagonists', 'protagonists_doubles',
                           'com_functions',
                           'expl_demands', 'impl_demands', 'all_demands']
    if label_type not in label_possibilities:
        print("Error: label_type must be one of:\n" +
              "\n".join(label_possibilities))
        return
    labels = getattr(corpus, label_type)

    matched_anno_list = []
    for span in labels:
        if label in span.values():
            matched_anno_list.append(span)

    relevant_spans_dict = xau.label_associations(corpus.moralizations,
                                                 matched_anno_list)

    return_string_list = []
    for moralization_tuple in relevant_spans_dict:
        if relevant_spans_dict[moralization_tuple] != []:
            for protagonist in relevant_spans_dict[moralization_tuple]:
                if xau.get_span(text, protagonist):
                    text = (
                        text[:(protagonist[0])]
                        + xau.special_upper(xau.get_span(text, protagonist))
                        + text[(protagonist[1]):]
                    )
            output_string = xau.get_span(text, moralization_tuple)
            return_string_list.append(output_string)

    if export:
        xau.list_to_excel(return_string_list,
                          f"{label}_{label_type}_instances.xlsx")

    return return_string_list
