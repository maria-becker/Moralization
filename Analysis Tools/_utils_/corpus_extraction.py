"""Corpus Data Extraction from .XMI files

This module provides classes and functions that make it possible to
extract corpus data and annotation from an .xmi file.
The corpus/file must be in the annotation format used by the
Moralization Project @University of Heidelberg, see here:
https://github.com/maria-becker/Moralization.

The module's classes are used by most other modules
in the 'Analysis Tools' directory, but provide no immediate
analysis options themselves.

Author: Bruno Brocai
"""


import xml.etree.ElementTree as ET



class CorpusData:
    """
    A class to represent annotated corpus data.
    Initialized by passing it a filepath
    to a corpus in XMI format.


    Attributes
    ----------
    text : str
        corpus string
    moralizations : list of 2-tuples
        beginnings and ends of moralizing segments
    moralizations_extended : an extended version of moralization which not only contains the span widht
        but also the type of moralization
    obj_morals : list of dicts containing 2-tuples and annotation info
        beginnings and ends of moral value segments, together with their
        moral category according to MFT
    subj_morals: list of dicts containing 2-tuples and annotation info
        beginnings and ends of subjective expression segments, together with
        their moral category according to MFT
    all_morals: list of dicts containing 2-tuples and annotation info
        obj_morals + subj_morals
    protagonists: list of dicts containing 2-tuples and annotation info
        beginnings and ends of protagonist segments, together with their
        three categories they belong to. No duplicate segments!
    protagonists_doubles: list of dicts containing 2-tuples and annotation info
        beginnings and ends of protagonist segments, together with their
        three categories they belong to. Duplicate segments possible, for
        example when a protagonist has several roles at once!
    com_functions: list of dicts containing 2-tuples and annotation info
        beginnings and ends of one or more sentences and their specific
        communicative function according to Jacobson
    expl_demands: list of dicts containing 2-tuples and annotation info
        beginnings and ends of segments containing explicit demands
    impl_demands: list of dicts containing 2-tuples and annotation info
        beginnings and ends of segments containing implied demands,
        and an explication of those demands
    all_demands: list of dicts containing 2-tuples and annotation info
        expl_demands + impl_demands
    """

    def __init__(self, filepath):
        """
        Initializes all attributes with data from an xmi file
        specified by filepath.
        """
        self.text = ""
        self.moralizations = []
        
        self.moralizations_extended = []
        self.obj_morals = []
        self.subj_morals = []
        self.all_morals = []
        self.protagonists = []
        self.protagonists_doubles = []
        self.com_functions = []
        self.expl_demands = []
        self.impl_demands = []
        self.all_demands = []

        self.load_data_from_file(filepath)

    def load_data_from_file(self, filepath):
        """
        Assigns values to all attributes using data from an xmi file
        specified by filepath.
        """
        self.text = text_from_xmi(filepath)
        self.moralizations = list_moralizations_from_xmi(filepath)
        self.moralizations_extended = list_extended_moralizations_from_xmi(filepath)
        self.obj_morals = list_obj_moral_from_xmi(filepath)
        self.subj_morals = list_subj_moral_from_xmi(filepath)
        self.all_morals = self.obj_morals + self.subj_morals
        self.protagonists = list_protagonists_from_xmi(
            filepath,
            skip_duplicates=True)
        self.protagonists_doubles = list_protagonists_from_xmi(
            filepath,
            skip_duplicates=False)
        self.com_functions = list_comfunction_from_xmi(filepath)
        self.expl_demands = list_expldemand_from_xmi(filepath)
        self.impl_demands = list_impldemand_from_xmi(filepath)
        self.all_demands = self.expl_demands + self.impl_demands


class CorpusCollection:
    """
    This class represents a collection of corpus data
    from several corpora. The data is stored in the form of
    CorpusData objects (see above).
    Attributes
    ----------
    language: language that the corpus strings are in.
        options: 'de', 'en', 'it', 'fr',
                 'all' (if there is more that one language)
    collection: dict
        keys are the filepaths; values are associated
        CorpusData objects
    """

    def __init__(self, filepath_list, language='all'):
        self.collection = {}
        self.language = language
        for filepath in filepath_list:
            self.collection[filepath] = CorpusData(filepath)


def text_from_xmi(filepath):
    """
    Extracts the corpus string that the annotations are based on
    from an xmi file.

    Parameters:
        filepath: The xmi file you want to open.
    Returns:
        The corpus as a string
    """

    # Open the XMI file
    tree = ET.parse(filepath)
    root = tree.getroot()

    text = root.find("{http:///uima/cas.ecore}Sofa").get('sofaString')

    return text


def list_moralizations_from_xmi(filepath):
    """
    Takes an xmi file and returns a list with 2-tuples.
    The tuples mark the beginning and ending of spans that were
    categorized as "moralizing speech acts".

    Parameters:
        filepath: The xmi file you want to open.
    Returns:
        List of 2-tuples.
    """

    # Open the XMI file
    tree = ET.parse(filepath)
    root = tree.getroot()

    span_list = root.findall("{http:///custom.ecore}Span")

    
    # Get all moralizing instances
    moral_spans_list = []
    for span in span_list:

        label = span.get('KAT1MoralisierendesSegment')
        
        if label:
            if label != "Keine Moralisierung":
                coordinates = (int(span.get("begin")), int(span.get("end")))

                # Test for duplicates, as there are some in the data
                if coordinates not in moral_spans_list:
                    moral_spans_list.append(coordinates)

    return moral_spans_list

def list_extended_moralizations_from_xmi(filepath):
    """
    Takes an xmi file and returns a list consisting of dicts.
    The tuples mark the beginning and ending of spans that were
    categorized as "moralizing speech acts".

    Parameters:
        filepath: The xmi file you want to open.
    Returns:
        List of dicts of form: [{Coordinates: (x, y), Label: String}, ...]
    """

    # Open the XMI file
    tree = ET.parse(filepath)
    root = tree.getroot()

    span_list = root.findall("{http:///custom.ecore}Span")

    
    # Get all moralizing instances
    moral_spans_list = []
    moral_spans_list_extended = []
    for span in span_list:

        label = span.get('KAT1MoralisierendesSegment')
        
        if label:
            if label != "Keine Moralisierung":
                coordinates = (int(span.get("begin")), int(span.get("end")))

                # Test for duplicates, as there are some in the data
                if coordinates not in moral_spans_list:
                    moral_spans_list.append(coordinates)
                    moral_spans_list_extended.append({'Coordinates': coordinates, 'Label': label})

    return moral_spans_list_extended


def list_protagonists_from_xmi(
    filepath,
    ignore_list=[],
    skip_duplicates=False
):
    """
    Takes an xmi file and returns a list of dictionaries
    representing annotations of 'protagonists'.
    The dictionaries contain:
        "Coordinates": 2-tuples marking the beginning and ending of the span
        "Rolle": the role that was annotated
        "Gruppe": the group that was annotated
        "own/other": whether the speaker regards the protagonist
                     as a member of their own group

    Parameters:
        filepath: The xmi file you want to open.
        ignore_list: If there are any categories you don't want returned,
                    add them to this list. Example: You don't care about
                    protagonists that don't have a clear role:
                    ignore_list = ["Kein Bezug"].
                    Default is None.
        skip_duplicates: Protagonists are annotated several times if they
                        have several roles. If this param is set to
                        True, they are only counted once (Which of their
                        several roles is counted is effectively random).
                        Default is False.
    Returns:
        List of dictionaries as described above.
    """

    # Open the XMI file
    tree = ET.parse(filepath)
    root = tree.getroot()
    span_list = root.findall("{http:///custom.ecore}Span")

    # Get all protagonist spans
    protagonist_spans_list = []
    for span in span_list:
        test = span.get('Protagonistinnen')
        if test:

            # Ignore categories on the ignore list
            # and duplicates if skip_duplicates=True
            attribute_list = []
            ignore = False
            for category in [
                "Protagonistinnen",
                "Protagonistinnen2",
                "Protagonistinnen3"
            ]:
                attribute_list.append(span.get(category))
                for element in ignore_list:
                    if element in attribute_list:
                        ignore = True

            if skip_duplicates:
                coordinates = (int(span.get("begin")), int(span.get("end")))
                for entry in protagonist_spans_list:
                    if coordinates == entry["Coordinates"]:
                        ignore = True

            # Add relevant spans in form of a dictionary containing
            # coordinates and annotation info such as role or group
            if not ignore:
                data_dict = {
                    "Coordinates": (
                        int(span.get("begin")), int(span.get("end"))
                    ),
                    "Rolle": span.get("Protagonistinnen"),
                    "Gruppe": span.get("Protagonistinnen2"),
                    "own/other": span.get("Protagonistinnen3")
                }
                protagonist_spans_list.append(data_dict)

    return protagonist_spans_list


def list_obj_moral_from_xmi(filepath):
    """
    Takes an xmi file and returns a list of dictionaries
    representing annotations of moral values.

    The dictionaries contain:
        "Coordinates": 2-tuples marking the beginning and ending of the span
        "Category": Moral Foundations Dimension of the span

    Parameters:
        filepath: The xmi file you want to open.
    Returns:
        List of dictionaries as described above.
    """
    tree = ET.parse(filepath)
    root = tree.getroot()

    span_list = root.findall("{http:///custom.ecore}Span")

    # Get all moralizing instances
    morals_list = []
    for span in span_list:
        category = span.get('Moralwerte')

        if category:
            data_dict = {
                "Coordinates":
                    (int(span.get("begin")), int(span.get("end"))),
                "Category":
                    category
            }
            morals_list.append(data_dict)

    return morals_list


def list_subj_moral_from_xmi(filepath):
    """
    Takes an xmi file and returns a list of dictionaries
    representing annotations of subjective expressions.

    The dictionaries contain:
        "Coordinates": 2-tuples marking the beginning and ending of the span
        "Category": Moral Foundations Dimension of the span

    Parameters:
        filepath: The xmi file you want to open.
    Returns:
        List of dictionaries as described above.
    """
    tree = ET.parse(filepath)
    root = tree.getroot()

    span_list = root.findall("{http:///custom.ecore}Span")

    # Get all moralizing instances
    morals_list = []
    for span in span_list:
        category = span.get('KAT2Subjektive_Ausdrcke')

        if category:
            data_dict = {
                "Coordinates":
                    (int(span.get("begin")), int(span.get("end"))),
                "Category":
                    category
            }
            morals_list.append(data_dict)

    return morals_list


def list_comfunction_from_xmi(filepath):
    """
    Takes an xmi file and returns a list of dictionaries
    representing annotations of communicative functions
    on or above the sentence level.

    The dictionaries contain:
        "Coordinates": 2-tuples marking the beginning and ending of the span
        "Category": Communicative function of the span (after Jacobson)

    Parameters:
        filepath: The xmi file you want to open.
    Returns:
        List of dictionaries as described above.
    """
    tree = ET.parse(filepath)
    root = tree.getroot()

    span_list = root.findall("{http:///custom.ecore}Span")

    # Get all moralizing instances
    comfunction_list = []
    for span in span_list:
        category = span.get('KommunikativeFunktion')

        if category:
            data_dict = {
                "Coordinates":
                    (int(span.get("begin")), int(span.get("end"))),
                "Category":
                    category
            }
            comfunction_list.append(data_dict)

    return comfunction_list


def list_impldemand_from_xmi(filepath):
    """
    Takes an xmi file and returns a list of dictionaries
    representing annotations of implicit demands.

    The dictionaries contain:
        "Coordinates": 2-tuples marking the beginning and ending of the span
        "Text": simple explication of the demand
        "Category": always the str "implizit" -
                    matters for the CorpusData attribute all_demands

    Parameters:
        filepath: The xmi file you want to open.
    Returns:
        List of dictionaries as described above.
    """
    tree = ET.parse(filepath)
    root = tree.getroot()

    span_list = root.findall("{http:///custom.ecore}Span")

    # Get all moralizing instances
    demand_list = []
    for span in span_list:
        category = span.get('KAT5Ausformulierung')

        if category:
            data_dict = {
                "Coordinates":
                    (int(span.get("begin")), int(span.get("end"))),
                "Text":
                    category,
                "Category":
                    "implizit"
            }
            demand_list.append(data_dict)

    return demand_list


def list_expldemand_from_xmi(filepath):
    """
    Takes an xmi file and returns a list of dictionaries
    representing annotations of explicit demands.

    The dictionaries contain:
        "Coordinates": 2-tuples marking the beginning and ending of the span
        "Category": always the str "explizit" -
                    matters for the CorpusData attribute all_demands

    Parameters:
        filepath: The xmi file you want to open.
    Returns:
        List of dictionaries as described above.
    """
    tree = ET.parse(filepath)
    root = tree.getroot()

    span_list = root.findall("{http:///custom.ecore}Span")

    # Get all moralizing instances
    demand_list = []
    for span in span_list:
        category = span.get('Forderung')

        if category:
            data_dict = {
                "Coordinates":
                    (int(span.get("begin")), int(span.get("end"))),
                "Category":
                    category
            }
            demand_list.append(data_dict)

    return demand_list
