"""Helps create nicely looking lists of strings found by the
filter functions.

Author:
Bruno Brocai (bruno.brocai@gs.uni-heidelberg.de)
University of Heidelberg
Research Projekt "Moralisierungen in verschiedenen Wissensdomänen"

TODO:
- Small module. Maybe move somewhere else?
"""

from . import _util_ as util


def highlighted_relevant_strings(text, relevant_spans_dict, allow_zero=False):
    """Creates a list of strings where the relevant instances are uppercase.

    Args:
        text (str): The text where the relevant instances are found.
        relevant_spans_dict (dict): A dictionary with the moralizations as keys
            and the relevant instances as values (lists of 2-tuples).

    Returns:
        list: A list of strings where the relevant instances are uppercase.
    """

    return_strings = []
    for moralization, relevant_instances in relevant_spans_dict.items():
        if relevant_instances != [] or allow_zero:
            for instance in relevant_instances:
                if util.get_span(text, instance):
                    text = "".join((
                        text[:(instance[0])],
                        util.special_upper(util.get_span(text, instance)),
                        text[(instance[1]):]
                    ))
            output_string = util.get_span(text, moralization)
            return_strings.append(output_string)
    return return_strings


def relevant_strings(text, relevant_spans):
    """Creates a list of strings based whose slices are in relevant_spans."""
    return_strings = []
    for moralization in relevant_spans:
        return_strings.append(
            util.get_span(text, moralization)
        )
    return return_strings
