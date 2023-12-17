"""XMI Data Preparation for Binary Classifier

This module contains functions that allow one to retrieve annotated spans
from an XMI corpus file, map annotations onto corresponding sentences,
remove duplicates and standarize the data.

The data is assumed to be in the format used by the Moralization Project
@ University of Heidelberg; see here:
https://github.com/maria-becker/Moralization

Author: Bruno Brocai
"""


import xml.etree.ElementTree as ET
import re
from nltk.tokenize import sent_tokenize
import _util_ as util


ZEITUNG_PATTERN = " *[A-Z0-9]{3,}/.*?S.(\n| )[A-Z]?[0-9]+.*?\n?###"
PLENAR_PATTERN = " *[A-Z0-9]{3,}/.*Plenarprotokoll,.*[0-9]{4} ###"


def text_from_xmi(filepath):
    """
    Extracts the corpus string that the annotations are based on
    from an xmi file.

    Parameters:
        filepath: The xmi file you want to open.
    Returns:
        The corpus as a single string
    """

    # Open the XMI file
    tree = ET.parse(filepath)
    root = tree.getroot()

    text = root.find("{http:///uima/cas.ecore}Sofa").get('sofaString')

    return text


def get_span(text, coordinates):
    """
    Takes a corpus string and a 2-tuple. Returns the slice
    of the 2-tuple if possible;
    otherwise prints an Error message and returns None.
    """

    try:
        span = text[coordinates[0]:(coordinates[1])]
        return span
    except TypeError:
        print("Error getting span.")
        return None


def list_types_from_xmi(filepath):
    """
    Takes an xmi file and returns a list with 2-tuples.
    The tuples mark the beginning and ending of spans that were
    categorized as "moralizing speech acts".

    Args:
        filepath: The xmi file you want to open.
    Returns:
        List of 3-tuples.
        tuple[1] is a bool (whether the span was annotated as moralizing)
        tuple[2] and [3] are beginning and end of the annotation slice
    """

    # Open the XMI file
    tree = ET.parse(filepath)
    root = tree.getroot()

    # Namespace declaration
    namespace = "{http:///custom.ecore}"

    # Get all moralizing instances
    moral_spans_list = []

    for span in root.findall(f"{namespace}Span"):
        test = span.get('KAT1MoralisierendesSegment')

        if test:
            coordinates = (int(span.get("begin")), int(span.get("end")))
            category = 0
            if span.get('KAT1MoralisierendesSegment') != "Keine Moralisierung":
                category = 1

            moral_spans_list.append((category, coordinates))

    moral_spans_list = join_consecutive_elements(moral_spans_list)

    return moral_spans_list


def join_consecutive_elements(index_list):
    """
    Given a list of index tuples, creates a new list where all index tuples
    following directly after each other are joined into one bigger tuple

    Args:
        index_list (list): 2d array of start and end indices

    Returns:
        list: 2d array of start and end indices
    """

    joined_list = []

    for category, (start, end) in index_list:
        if (
            joined_list and joined_list[-1][0] == category
            and joined_list[-1][1][1] == start-1
        ):
            # Merge with the previous element
            joined_list[-1] = (category, (joined_list[-1][1][0], end))
        else:
            # Add a new element
            joined_list.append((category, (start, end)))

    return joined_list


def find_split_indices(pattern, text):
    """
    Given a regex pattern, matches all occurences of that pattern
    in a string and lists the start and end indices of these occurences

    Args:
        pattern (str): python regex pattern
        text (str): string that is going to be matched

    Returns:
        list: 2d array of start and end indices of the matches
    """

    indices_end = [match.end() for match in re.finditer(pattern, text)]
    indices_begin = [match.start() for match in re.finditer(pattern, text)]

    return list(zip(indices_begin, indices_end))


def get_inbetween(tuples, last):
    """
    Given a list of indices, returns a similar list of indices indexing
    all text that the original list did not index, except the text before
    the first index

    Args:
        tuples (list): 2d array of start and end indices
        last (int): index of final char

    Returns:
        list: 2d array of start and end indices of all everything not in
            the original list (except anything before the first entry)
    """

    tuples_inbetween = []

    for i in range(len(tuples) - 1):
        start = tuples[i][1] + 1
        end = tuples[i + 1][0] - 1
        tuples_inbetween.append((start, end))

    try:
        tuples_inbetween.append((tuples[-1][1], last-1))
    except IndexError:
        print("IndexError with get_inbetween()")

    return tuples_inbetween


def narrow_tuples(tuples, text):
    """
    Given a list of 2-tuples of (begin and end) indices and a string to which
    these indices apply, narrows there tuples until they do no longer start
    or end with space, # or newline.

    Args:
        tuples (list): 2d array of start and end indices
        text (string): string that the tuples-list applies to

    Returns:
        list: 2d array of start and end indices
    """

    new_tuples = []
    for tuple in tuples:
        begin = tuple[0]
        end = tuple[1]

        whitespace = [' ', '#', '\n']

        while text[begin] in whitespace:
            begin += 1
        while text[end] in whitespace:
            end -= 1
        try:
            end += 1
        except IndexError:
            pass

        new_tuples.append((begin, end))

    return new_tuples


def get_sentence_slices(text):
    """
    Takes a long string and returns two lists:
    One is the string split into sentences via NLTK,
    the other is a list of start and end indices of these sentences.

    Args:
        text (string): string you want to split

    Returns:
        tuple:
            tuple[0]: List of sentences (strings)
            tuple[1]: List of start and end indices of the sentences -
                2-tuples of ints
            Example: (
                ['Hello World!', 'How are you?']
                [(0, 12), (13, 25)]
    """

    # Sentence tokenization
    sentences = sent_tokenize(text)

    # Get start and end indices for each sentence
    sentence_slices = []
    start_index = 0

    for sentence in sentences:
        end_index = start_index + len(sentence)
        sentence_slices.append((start_index, end_index))
        start_index = end_index + 1

    return sentences, sentence_slices


def ranges_overlap(range1, range2):
    """
    Checks whether two 2-tuples overlap at least by one element,
    assuming slicing. This means that the end index is not counted.
    """
    start1, end1 = range1
    start2, end2 = range2

    return end1 > start2 and end2 > start1


def map_annotation_on_sents(annotations, spans, text):
    """
    Creates a list of annotation data about spans in a corpus string.
    Output includes the text spans split into sentences, whether the
    span as a whole contains a moralization, and whether each sentence
    is part of that moralization.

    Args:
        annotations (list): 2d array of start and end of text categorized
            as moralizing speechact
        spans (list): 2d array of start and end indices of text fragments
            without metadata
        text (string): string containing the text that the spans are found
            in and the annotations are based on

    Returns:
        list: 3d array of shape [
            [
                ['sentence1'(str), 'sentence2'(str)],
                moralization_in_span?(bool),
                [moralization_in_sent1?(bool), moralization_in_sent2?(bool)]
            ]
        ]
    """

    mappings = []

    for span in spans:
        span_text = get_span(text, span)
        sentences, sent_slices = get_sentence_slices(span_text)

        sent_annos = [0] * len(sent_slices)
        for index, slice in enumerate(sent_slices):
            for annotation in annotations:
                absolute_sent_slice = (
                    span[0] + slice[0],
                    span[0] + slice[1]
                )
                if annotation[0] and ranges_overlap(
                    absolute_sent_slice, annotation[1]
                ):
                    sent_annos[index] = 1

        sentences = util.clean_sentences(sentences)
        if 1 in sent_annos:
            mappings.append([sentences, 1, sent_annos])
        else:
            mappings.append([sentences, 0, sent_annos])

    return mappings


def map_from_file(filepath, genre_nbr=None):
    """
    Performs all necessary steps to create a list of annotation data
    given a filepath and (optionally) a genre number.

    Args:
        filepath (str): Path to the XMI file to be used
        genre_nbr (int, optional): Int associated with genre of the subcorpus.
            Defaults to check the filepath for corpus info.

    Returns:
        list: 3d array with info data from the xmi of shape [
            [
                genre_nbr(int),
                ['sentence1'(str), 'sentence2'(str)],
                moralization_in_span?(bool),
                [moralization_in_sent1?(bool), moralization_in_sent2?(bool)]
            ]
        ]
    """

    if genre_nbr is None:
        genre_nbr = util.genre_labels(filepath)

    text = text_from_xmi(filepath)
    if genre_nbr == 5:
        pattern = PLENAR_PATTERN
    else:
        pattern = ZEITUNG_PATTERN

    spans = find_split_indices(pattern, text)
    spans = get_inbetween(spans, len(text))
    spans = narrow_tuples(spans, text)

    annos = list_types_from_xmi(filepath)

    mappings = map_annotation_on_sents(annos, spans, text)
    mappings = [([genre_nbr] + entry) for entry in mappings]
    mappings = util.remove_doubles(mappings)

    return mappings
