import xml.etree.ElementTree as ET
import corpus_extraction as ce
import xmi_analysis_util as xau
import regex as re


def list_moralizations_from_xmi(
    filepath,
    metadata_regex
):
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

        if test == "Keine Moralisierung":
                coordinates = (int(span.get("begin")), int(span.get("end")))

                # Test for duplicates, for there are some in the data
                if coordinates not in moral_spans_list:
                    moral_spans_list.append(coordinates)
                else:
                    pass
    
    corpus_list = []
    corpus_string = ce.text_from_xmi(filepath)
    for span in moral_spans_list:
        text = xau.get_span(corpus_string, span)
        text = re.sub(metadata_regex, '', text)
        corpus_list.append(text)

    return corpus_list
