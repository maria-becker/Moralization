import sys
import label_filtering_single as lfs

sys.path.append("../_utils_")
import xmi_analysis_util as xau
import language_tag_manager as langtag


def lemma_label_instances(
    corpus,
    lemma,
    label_type,
    hanta=False,
    export=False
):
    output_dict = {}
    for subcorpus in corpus.collection.keys():
        output_dict[subcorpus] = lfs.lemma_label_instances_single(
            corpus.collection[subcorpus],
            lemma,
            label_type,
            language=corpus.language,
            hanta=hanta,
            export=False
        )

    if export:
        xau.dict_to_excel(
            output_dict,
            f"{lemma}_{label_type}_instances.xlsx"
        )

    return output_dict


def pos_label_instances(
    corpus,
    pos,
    label_type,
    hanta=False,
    export=False
):
    output_dict = {}
    for subcorpus in corpus.collection.keys():
        output_dict[subcorpus] = lfs.pos_label_instances_single(
            corpus.collection[subcorpus],
            pos,
            label_type,
            language=corpus.language,
            hanta=hanta,
            export=False
        )

    if export:
        xau.dict_to_excel(
            output_dict,
            f"{pos}_{label_type}_instances.xlsx"
        )

    return output_dict


def poslist_label_instances(
    corpus,
    pos_list,
    label_type,
    hanta=False,
    export=False
):
    output_dict = {}
    for subcorpus in corpus.collection.keys():
        output_dict[subcorpus] = lfs.poslist_label_instances_single(
            corpus.collection[subcorpus],
            pos_list,
            label_type,
            language=corpus.language,
            hanta=hanta,
            export=False
        )

    if export:
        xau.dict_to_excel(
            output_dict,
            f"[{pos_list[1]}, ...]_{label_type}_instances.xlsx"
        )

    return output_dict


def count_label_instances(
    corpus,
    count,
    label_type,
    export=False
):
    output_dict = {}
    for subcorpus in corpus.collection.keys():
        output_dict[subcorpus] = lfs.count_label_instances_single(
            corpus.collection[subcorpus],
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


def tag_label_instances(
    corpus,
    tag,
    label_type,
    export=False
):
    output_dict = {}
    for subcorpus in corpus.collection.keys():
        output_dict[subcorpus] = lfs.tag_label_instances_single(
            corpus.collection[subcorpus],
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


def search_annotation_count(
    corpus,
    category,
    count,
    export=False
):
    output_dict = {}
    for subcorpus in corpus.collection.keys():
        output_dict[subcorpus] = lfs.annotation_count_instances_single(
            corpus.collection[subcorpus],
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


def token_label_instances(
    corpus,
    token,
    label_type,
    export=False
):
    output_dict = {}
    for subcorpus in corpus.collection.keys():
        output_dict[subcorpus] = lfs.token_label_instances_single(
            corpus.collection[subcorpus],
            token,
            label_type,
            export=False
        )

    if export:
        xau.dict_to_excel(
            output_dict,
            f"{token}_{label_type}_instances.xlsx"
        )

    return output_dict
)
