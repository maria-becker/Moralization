import numpy as np
import xlsxwriter
import os


def inside_of(coord_list, coord_tuple):
    """
    Checks whether the specific coordinates of coord_tuple
    are inside any of the coordinates on the list.
    Returns the first match, or None if there is no match.
    """

    for coord in coord_list:
        if coord_tuple[0] >= coord[0] and coord_tuple[1] <= coord[1]:
            return coord
    return None


def label_associations(moral_spans_list, label_spans_list):
    """
    Takes a list of moral spans and a list of annotation dicts
    to create a dictionary where the keys are 2-tuples of the
    beginning and end of a moralization, and the values are
    lists of 2-tuples of the beginnings and ends of the annotations
    inside the moralization.
    If an annotation is outside all moralizing spans, prints
    'KeyError' to the console. This means that something was
    falsely annotated, not that the function itself is
    experiencing an error!
    """

    dictionary = {}

    for moralization in moral_spans_list:
        dictionary[moralization] = []
    for label in label_spans_list:
        moral_span = inside_of(
            moral_spans_list, label["Coordinates"])
        try:
            dictionary[moral_span].append(label["Coordinates"])
        except KeyError:
            print("".join(("KeyError: ", str(label["Coordinates"]))))

    return dictionary


def label_associations_category(moral_spans_list, label_spans_list):
    """
    Takes a list of moral spans and a list of annotation dicts
    to create a dictionary where the keys are 2-tuples of the
    beginning and end of a moralization, and the values are
    lists of dictionaries that contain a 2-tuple and all
    annotation information.
    If an annotation is outside all moralizing spans, prints
    'KeyError' to the console. This means that something was
    falsely annotated, not that the function itself is
    experiencing an error!
    """

    dictionary = {}

    for moralization in moral_spans_list:
        dictionary[moralization] = []
    for label in label_spans_list:
        moral_span = inside_of(
            moral_spans_list, label["Coordinates"])
        try:
            dictionary[moral_span].append(label)
        except KeyError:
            print("".join(("KeyError: ",
                           str(label),
                           " -- Is the label inside a moralization?")))

    return dictionary


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


def special_upper(string):
    """Works like the upper() method, exept it does not turn 'ß' into 'SS'."""
    newstring = ''
    for i in range(len(string)):
        if (string[i]) != 'ß':
            newstring = ''.join((newstring, string[i].upper()))
        else:
            newstring = ''.join((newstring, string[i]))

    return newstring


def label_in_list(anno_list, category):
    """
    Takes a list of dicts; and if the category passed
    to this function is somewhere in the values of these
    dicts, returns True; else, False.
    """
    for element in anno_list:
        if category in element.values():
            return True
    return False


def possible_labels(category):
    """
    Returns lists of possible labels for any given
    category; for example, returns a list of MFT categories
    if a _moral category was passed.
    """
    cat_possibilities = ['obj_morals', 'subj_morals', 'all_morals',
                         'prot_roles', 'prot_groups', 'prot_ownother',
                         'com_functions',
                         'demands']
    if category in cat_possibilities[:3]:
        return [
            'Care',
            'Harm',
            'Fairness',
            'Cheating',
            'Loyalty',
            'Betrayal',
            'Authority',
            'Subversion',
            'Sanctity',
            'Degradation',
            'Liberty',
            'Oppression',
            'OTHER'
        ]
    if category == cat_possibilities[3]:
        return [
            'Adressat:in',
            'Benefizient:in',
            'Forderer:in',
            'Malefizient:in',
            'Kein Bezug',
            'Bezug unklar'
        ]
    if category == cat_possibilities[4]:
        return [
                "Individuum",
                "Institution",
                "Menschen",
                "soziale Gruppe",
                "Sonstige"
            ]
    if category == cat_possibilities[5]:
        return [
            'Own Group',
            'Other Group',
            'Neutral',
        ]
    if category == cat_possibilities[6]:
        return [
            'Appell',
            'Beziehung',
            'Darstellung',
            'Expression',
            'Appell+Beziehung',
            'Appell+Darstellung',
            'Appell+Expression'
        ]
    if category == cat_possibilities[7]:
        return [
            'implizit',
            'explizit'
        ]
    return None


def calculate_normalized_pmi(contingency_table):
    """
    Calculate PMI (Pointwise Mutual Information)
    from a given contingency table.

    Parameters:
        - contingency_table: A 2x2 contingency table with counts.

    Returns:
        - PMI value.
    """
    counter_12, counter_1 = contingency_table[0]
    counter_2, counter_none = contingency_table[1]

    total_segments = counter_12 + counter_1 + counter_2 + counter_none

    p_x_and_y = counter_12
    p_x = (counter_12 + counter_1)
    p_y = (counter_12 + counter_2)

    if p_x_and_y == 0.0 or p_x == 0.0 or p_y == 0.0:
        return float('-inf')  # Avoid log(0)

    pmi = np.log2(p_x_and_y / ((p_x * p_y) / total_segments))
    jsi = -1 * np.log2(p_x_and_y / total_segments)
    return (pmi / jsi)


def freq_table(corpus, associations1, associations2, label1, label2):
    """
    Creates a contigency table for two annotation labels. Looks whether
    the one, both or none of the lables are present at least once
    for each moralizing segment in the corpus.

    Parameters:
        - corpus: CorpusData object
        - associations1: dict as created by label_associatins_category()
        - associations2: dict as created by label_associatins_category()
        - label1: str of a label (such as 'Care', 'Harm')
        - label2: str of a label (such as 'Care', 'Harm')

    Returns:
        - two-dimensional array (the contigency table as described above).
    """
    counter_1 = 0
    counter_2 = 0
    counter_12 = 0
    counter_none = 0

    for moralization in corpus.concat_coords("moralizations"):
        if label_in_list(associations1[moralization], label1):
            if label_in_list(associations2[moralization], label2):
                counter_12 += 1
            else:
                counter_1 += 1
        elif label_in_list(associations2[moralization], label2):
            counter_2 += 1
        else:
            counter_none += 1

    contingency_table = [
        [counter_12, counter_1],
        [counter_2, counter_none]
    ]

    return contingency_table


def list_to_excel(source_list, filepath):
    """
    Takes a list and writes it into the first column
    of an excel file.
    """

    workbook = xlsxwriter.Workbook(filepath)
    worksheet = workbook.add_worksheet("list")

    row = 0
    col = 0
    for item in source_list:
        worksheet.write(row, col, item)
        row += 1

    workbook.close()
    return None


def dict_to_excel(source_dict, filepath):
    """
    Takes a dictionary with lists as values and
    writes the list contents into the first row of an excel
    file; the values are divided into sections
    based on the key the are associated with.
    """
    workbook = xlsxwriter.Workbook(filepath)
    worksheet = workbook.add_worksheet("dict")

    row = 0
    col = 0
    bold = workbook.add_format({'bold': True})

    keys_list = list(source_dict.keys())

    for key in keys_list:
        worksheet.write(row, col, key, bold)
        row += 1
        for item in source_dict[key]:
            worksheet.write(row, col, item)
            row += 1
        if key != keys_list[-1]:
            worksheet.write(row, col, "", bold)
            row += 1

    workbook.close()
    return None


def valid_category(category):
    """
    Checks whether a string conforms with one of the attributes
    of a CorpusData object; if not, prints a list of strings
    that do.
    """
    possible_categories = ['obj_morals', 'subj_morals', 'all_morals',
                           'protagonists', 'protagonists_doubles',
                           'com_functions',
                           'expl_demands', 'impl_demands', 'all_demands']

    if category not in possible_categories:
        print("Error: label_type must be one of:\n" +
              "\n".join(possible_categories))
        return False

    return True


def list_xmis_in_directory(directory):
    """Creates a list of absolute filepaths to all xmis in a directory.

    Args:
        directory (str): path to directory
    """

    filepaths = []
    for filename in os.listdir(directory):
        filepath = os.path.join(directory, filename)

        if os.path.isfile(filepath) and filepath.endswith('.xmi'):
            filepaths.append(filepath)

    return filepaths
