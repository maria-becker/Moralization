import sys
import nltk
import search_helpers

sys.path.append("../_utils_")
import xmi_analysis_util as xau
import language_tag_manager as langtag


def lemma_label_instances_single(
    corpus,
    lemma,
    category,
    language="de",
    **kwargs
):

    hanta = kwargs.get('hanta', False)
    export = kwargs.get('export', False)

    if not xau.valid_category(category):
        return None

    label = getattr(corpus, category)

    if hanta:
        relevant_spans_list = hanta_lemma_label_search(
            corpus,
            label,
            lemma,
            language
        )
    else:
        relevant_spans_list = spacy_lemma_label_search(
            corpus,
            label,
            lemma,
            language
        )

    return_string_list = search_helpers.relevant_strings(
        corpus.text,
        relevant_spans_list
    )

    if export:
        xau.list_to_excel(return_string_list,
                          f"{lemma}_{category}_instances.xlsx")

    return list(set(return_string_list))


def hanta_lemma_label_search(corpus, label, lemma, language):

    associations = xau.label_associations(
        corpus.moralizations,
        label
    )

    tagger, language = search_helpers.init_hanta_nltk(language)

    relevant_spans_list = []

    for moralization, instances in associations.items():
        for instance in instances:
            tokenized = nltk.tokenize.word_tokenize(
                xau.get_span(corpus.text, instance), language=language)
            tags = tagger.tag_sent(tokenized)
            for tag in tags:
                if tag[1] == lemma:
                    relevant_spans_list.append(moralization)
                    break

    return list(set(relevant_spans_list))


def spacy_lemma_label_search(corpus, label, lemma, language):

    associations = xau.label_associations(
        corpus.moralizations,
        label
    )

    model = search_helpers.init_spacy(language)

    relevant_spans_list = []

    for moralization, instances in associations.items():
        for instance in instances:
            doc = model(xau.get_span(corpus.text, instance))
            for token in doc:
                if token.lemma_ == lemma:
                    relevant_spans_list.append(moralization)
                    break

    return list(set(relevant_spans_list))


def poslist_label_instances_single(
    corpus,
    pos_list,
    category,
    language,
    **kwargs
):

    hanta = kwargs.get('hanta', False)
    export = kwargs.get('export', False)

    if not xau.valid_category(category):
        return None

    label = getattr(corpus, category)

    if hanta:
        relevant_spans_list = hanta_poslist_label_search(
            corpus,
            label,
            pos_list,
            language
        )

    else:
        relevant_spans_list = spacy_poslist_label_search(
            corpus,
            label,
            pos_list,
            language
        )

    relevant_spans_dict = xau.label_associations(
        corpus.moralizations,
        relevant_spans_list
    )
    return_string_list = search_helpers.highlighted_relevant_strings(
        corpus.text,
        relevant_spans_dict
    )

    if export:
        xau.list_to_excel(return_string_list,
                          f"[{pos_list[1]}, ...]_{category}_instances.xlsx")

    return list(set(return_string_list))


def hanta_poslist_label_search(corpus, label, pos_list, language):

    associations = xau.label_associations(
        corpus.moralizations,
        label
    )

    tagger, language = search_helpers.init_hanta_nltk(language)

    relevant_spans_list = []

    for moralization, instances in associations.items():
        for instance in instances:
            tokenized = nltk.tokenize.word_tokenize(
                xau.get_span(corpus.text, instance), language=language)
            tags = tagger.tag_sent(tokenized)
            for tag in tags:
                if tag[2] in pos_list:
                    relevant_spans_list.append(moralization)
                    break

    return list(set(relevant_spans_list))


def spacy_poslist_label_search(corpus, label, pos_list, language):

    associations = xau.label_associations(
        corpus.moralizations,
        label
    )

    model = search_helpers.init_spacy(language)

    relevant_spans_list = []

    for moralization, instances in associations.items():
        for instance in instances:
            doc = model(xau.get_span(corpus.text, instance))
            for token in doc:
                if token.pos_ in pos_list:
                    relevant_spans_list.append(moralization)
                    break

    return list(set(relevant_spans_list))


def pos_label_instances_single(
    corpus,
    pos,
    category,
    language,
    **kwargs
):

    hanta = kwargs.get('hanta', False)
    export = kwargs.get('export', False)

    hits_list = poslist_label_instances_single(
        corpus,
        [pos],
        category,
        language,
        hanta=hanta,
        export=False
    )

    if export:
        xau.list_to_excel(hits_list,
                          f"[{pos}_{category}_instances.xlsx")

    return list(set(hits_list))


def count_label_instances_single(
    corpus,
    count,
    category,
    export=False
):

    if not xau.valid_category(category):
        return None

    label = getattr(corpus, category)

    association = xau.label_associations(
        corpus.moralizations,
        label
    )

    relevant_spans_dict = {
        key: entry for key, entry
        in association.items()
        if len(entry) == count
    }

    text = corpus.text
    return_string_list = search_helpers.highlighted_relevant_strings(
        text,
        relevant_spans_dict
    )

    if export:
        xau.list_to_excel(return_string_list,
                          f"{str(count)}_{category}_instances.xlsx")

    return list(set(return_string_list))


def tag_label_instances_single(
    corpus,
    label,
    category,
    export=False
):

    if not xau.valid_category(category):
        return None

    text = corpus.text

    labels = getattr(corpus, category)

    matched_anno_list = []
    for span in labels:
        if label in span.values():
            matched_anno_list.append(span)

    relevant_spans_dict = xau.label_associations(
        corpus.moralizations,
        matched_anno_list
    )

    return_string_list = search_helpers.highlighted_relevant_strings(
        text,
        relevant_spans_dict
    )

    if export:
        xau.list_to_excel(return_string_list,
                          f"{label}_{category}_instances.xlsx")

    return list(set(return_string_list))


def annotation_count_instances_single(
    corpus,
    category,
    count,
    export=False
):

    if not xau.valid_category(category):
        return None

    label = getattr(corpus, category)

    associations = xau.label_associations(
        corpus.moralizations,
        label
    )

    associations = {
        key: entry for key, entry
        in associations.items()
        if len(entry) == count
    }

    return_strings = search_helpers.highlighted_relevant_strings(
        corpus.text,
        associations
    )

    if export:
        xau.list_to_excel(return_strings,
                          f"{str(count)}_{category}_instances.xlsx")

    return list(set(return_strings))


def token_label_instances_single(
    corpus,
    token,
    category,
    lower=False,
    export=False
):

    if not xau.valid_category(category):
        return None

    label = getattr(corpus, category)

    associations = xau.label_associations(
        corpus.moralizations,
        label
    )

    relevant_spans_list = []
    text = corpus.text
    for moraliz, anno in associations.items():
        if lower:
            if token in xau.get_span(text, anno).lower():
                relevant_spans_list.append(moraliz)
        elif token in xau.get_span(text, anno):
            relevant_spans_list.append(moraliz)

    return_string_list = search_helpers.relevant_strings(
        corpus.text,
        relevant_spans_list
    )

    if export:
        xau.list_to_excel(return_string_list,
                          f"{token}_{category}_instances.xlsx")

    return list(set(return_string_list))
