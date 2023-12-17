"""Utility for Binary Classifier Data Preparation

This module contains utility functions used in preparing
XMI/Excel Annotation and Text Data for use as training/validation data
for a language model.

Author: Bruno Brocai
"""

import string


def genre_labels(name):
    """
    Given a string, returns the genre number corresponding to the genre
    the string mentions.

    Args:
        name: str - usualy a filename or an excel sheet name
    Returns:
        int corresponging to the genre
        (0 if the genre could not be identified).
    """

    if name.startswith("Gerichtsurteile"):
        return 1
    elif name.startswith("Interviews"):
        return 2
    elif name.startswith("Kommentare"):
        return 3
    elif name.startswith("Leserbriefe"):
        return 4
    elif name.startswith("Plenarprotokolle"):
        return 5
    elif name.startswith("Wikipedia"):
        return 6
    elif name.startswith("Sachbücher"):
        return 7
    elif name.startswith("Allgemein"):
        return 99
    return 0


def remove_doubles(mappings):
    """
    Compares all sentences with each other and returns a list
    where all douplicate sentences and their annotations have been removed.

    Args:
        mappings: list of lists of sentences, their genres and annotations
                  as created by the map_annotations()-functions.
    Returns:
        list in the mappings format, but with duplicate sentences
        and their corresponding annotations removed.
    """

    # Give spans with an annotation higher priority
    sorted_mappings = sorted(mappings, key=lambda x: x[2])

    seen_sentences = set()
    new_mappings = []

    for index, entry in enumerate(sorted_mappings):
        new_entry = entry.copy()
        seen_positions = set()

        # Create new entries that include only unseed sentences
        for position, sentence in enumerate(entry[1]):
            if sentence not in seen_sentences:
                seen_sentences.add(sentence)
                seen_positions.add(position)
            else:
                new_entry[1][position] = ""
                new_entry[3][position] = ""
        new_entry[1] = [
            x for i, x in enumerate(entry[1]) if i in seen_positions
        ]
        new_entry[3] = [
            x for i, x in enumerate(entry[3]) if i in seen_positions
        ]

        # Refresh the span annotation (a moralization may have been removed)
        if 1 in new_entry[3]:
            new_entry[2] = 1
        else:
            new_entry[2] = 0

        if new_entry[1]:
            new_mappings.append(new_entry)

    return new_mappings


def clean_sentences(sentences):
    """Somewhat standardizes a list of strings."""
    cleaned_sents = []

    for sentence in sentences:

        # Remove unwanted characters
        unwanted_chars = ["\n", "#"]
        for char in unwanted_chars:
            sentence = sentence.replace(char, " ")

        # Standardize Quotation Marks
        quot_marks = ['“', "„", "”", "»", "«"]
        for quotation_mark in quot_marks:
            sentence = sentence.replace(quotation_mark, '"')

        # Standardize dashes
        dashes = ["–", "—"]
        for dash in dashes:
            sentence = sentence.replace(dash, " - ")

        # Remove unnecessary whitespace
        while "  " in sentence:
            sentence = sentence.replace("  ", " ")
        while sentence[0] in string.whitespace:
            sentence = sentence[1:]

        cleaned_sents.append(sentence)

    return cleaned_sents
