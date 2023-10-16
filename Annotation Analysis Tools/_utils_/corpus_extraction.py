import xml.etree.ElementTree as ET


class CorpusData:
    def __init__(self, filepath):
        self.text = ""
        self.moralizations = []
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
        self.text = text_from_xmi(filepath)
        self.moralizations = list_moralizations_from_xmi(filepath)
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
    def __init__(self, filepath_list, language='all'):
        self.collection = {}
        self.language = language
        for filepath in filepath_list:
            self.collection[filepath] = CorpusData(filepath)


def text_from_xmi(filepath):
    """
    Extracts from the xmi the corpus that the annotations are based on.
    It is necessary to call this function if you want to output
    annotated text at some point.

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
    categorized as "moralizing speechacts".

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
        test = span.get('KAT1MoralisierendesSegment')

        if test:
            if test != "Keine Moralisierung":
                coordinates = (int(span.get("begin")), int(span.get("end")))

                # Test for duplicates, as there are some in the data
                if coordinates not in moral_spans_list:
                    moral_spans_list.append(coordinates)
                else:
                    # print('Error: ', str(coordinates))
                    pass

    return moral_spans_list


def list_protagonists_from_xmi(
    filepath,
    ignore_list=None,
    skip_duplicates=False
):
    """
    Takes an xmi file and returns a list of dictionaries.
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
                    Default is [].
        skip_duplicates: Protagonists are annotated several times if they
                        have several roles. If this param is set to
                        true, they are only counted once (Which of their
                        several roles is counted is effectively random).
                        Default is False.
    Returns:
        List of dictionaries as described above.
    """

    if ignore_list is None:
        ignore_list = []

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
