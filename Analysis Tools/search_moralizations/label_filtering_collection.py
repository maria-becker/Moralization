import sys
import label_filtering_single as lfs

sys.path.append("../_utils_")
import xmi_analysis_util as xau
import language_tag_manager as langtag


def lemma_label_instances_collection(
    corpus_collection,
    lemma,
    label_type,
    hanta=False,
    export=False
):
    output_dict = {}
    for corpus in corpus_collection.collection.keys():
        output_dict[corpus] = lfs.lemma_label_instances_single(
            corpus_collection.collection[corpus],
            lemma,
            label_type,
            language=corpus_collection.language,
            hanta=hanta,
            export=False
        )

    if export:
        xau.dict_to_excel(
            output_dict,
            f"{lemma}_{label_type}_instances.xlsx"
        )

    return output_dict


def pos_label_instances_collection(
    corpus_collection,
    pos,
    label_type,
    hanta=False,
    export=False
):
    output_dict = {}
    for corpus in corpus_collection.collection.keys():
        output_dict[corpus] = lfs.pos_label_instances_single(
            corpus_collection.collection[corpus],
            pos,
            label_type,
            language=corpus_collection.language,
            hanta=hanta,
            export=False
        )

    if export:
        xau.dict_to_excel(
            output_dict,
            f"{pos}_{label_type}_instances.xlsx"
        )

    return output_dict


def poslist_label_instances_collection(
    corpus_collection,
    pos_list,
    label_type,
    hanta=False,
    export=False
):
    output_dict = {}
    for corpus in corpus_collection.collection.keys():
        output_dict[corpus] = lfs.poslist_label_instances_single(
            corpus_collection.collection[corpus],
            pos_list,
            label_type,
            language=corpus_collection.language,
            hanta=hanta,
            export=False
        )

    if export:
        xau.dict_to_excel(
            output_dict,
            f"[{pos_list[1]}, ...]_{label_type}_instances.xlsx"
        )

    return output_dict


def count_label_instances_collection(
    corpus_collection,
    count,
    label_type,
    export=False
):
    output_dict = {}
    for corpus in corpus_collection.collection.keys():
        output_dict[corpus] = lfs.count_label_instances_single(
            corpus_collection.collection[corpus],
            count,
            label_type,
            export=False
        )

    if export:
        xau.dict_to_excel(
            output_dict,
            f"{str(count)}_{label_type}_instances.xlsx"
        )

    return output_dict


def tag_label_instances_collection(
    corpus_collection,
    tag,
    label_type,
    export=False
):
    output_dict = {}
    for corpus in corpus_collection.collection.keys():
        output_dict[corpus] = lfs.tag_label_instances_single(
            corpus_collection.collection[corpus],
            tag,
            label_type,
            export=False
        )

    if export:
        xau.dict_to_excel(
            output_dict,
            f"{tag}_{label_type}_instances.xlsx"
        )

    return output_dict


def search_annotation_count_collection(
    corpus,
    category,
    count,
    export=False
):
    output_dict = {}
    for corp in corpus.collection.keys():
        output_dict[corpus] = lfs.annotation_count_instances_single(
            corp.collection[corpus],
            category,
            count,
            export=False
        )

    if export:
        xau.dict_to_excel(
            output_dict,
            f"{str(count)}_{category}_instances.xlsx"
        )

    return output_dict
