import label_filtering_single as lfs
import xmi_analysis_util as xau
import os


def print_dict(dictionary):
    for key in dictionary.keys():
        name = os.path.basename(key)
        print(xau.special_upper(name))
        for entry in dictionary[key]:
            print(entry)
        print("\n")
    return


def word_label_instances_collection(
    corpus_collection,
    word,
    label_type,
    export=False
):
    output_dict = {}
    for corpus in corpus_collection.collection.keys():
        output_dict[corpus] = lfs.word_label_instances(
            corpus_collection.collection[corpus],
            word,
            label_type,
            language=corpus_collection.language,
            export=False
        )

    if export:
        xau.dict_to_excel(output_dict,
                          f"{word}_{label_type}_instances.xlsx")

    return output_dict


def pos_label_instances_collection(
    corpus_collection,
    pos,
    label_type,
    export=False
):
    output_dict = {}
    for corpus in corpus_collection.collection.keys():
        output_dict[corpus] = lfs.pos_label_instances(
            corpus_collection.collection[corpus],
            pos,
            label_type,
            language=corpus_collection.language,
            export=False
        )

    if export:
        xau.dict_to_excel(output_dict,
                          f"{pos}_{label_type}_instances.xlsx")

    return output_dict


def poslist_label_instances_collection(
    corpus_collection,
    pos_list,
    label_type,
    export=False
):
    output_dict = {}
    for corpus in corpus_collection.collection.keys():
        output_dict[corpus] = lfs.poslist_label_instances(
            corpus_collection.collection[corpus],
            pos_list,
            label_type,
            language=corpus_collection.language,
            export=False
        )

    if export:
        xau.dict_to_excel(output_dict,
                          f"[{pos_list[1]}, ...]_{label_type}_instances.xlsx")

    return output_dict


def count_label_instances_collection(
    corpus_collection,
    count,
    label_type,
    export=False
):
    output_dict = {}
    for corpus in corpus_collection.collection.keys():
        output_dict[corpus] = lfs.count_label_instances(
            corpus_collection.collection[corpus],
            count,
            label_type,
            export=False
        )

    if export:
        xau.dict_to_excel(output_dict,
                          f"{str(count)}_{label_type}_instances.xlsx")

    return output_dict


def tag_label_instances_collection(
    corpus_collection,
    tag,
    label_type,
    export=False
):
    output_dict = {}
    for corpus in corpus_collection.collection.keys():
        output_dict[corpus] = lfs.tag_label_instances(
            corpus_collection.collection[corpus],
            tag,
            label_type,
            export=False
        )

    if export:
        xau.dict_to_excel(output_dict,
                          f"{tag}_{label_type}_instances.xlsx")

    return output_dict
