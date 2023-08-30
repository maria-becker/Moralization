import numpy as np
import xlsxwriter


def inside_of(coord_list, coord_tuple):
    """
    Checks whether the specific coordinates
    are inside any of the coordinates on the list
    Returns the first match, or None if there is no match.
    """

    for coord in coord_list:
        if coord_tuple[0] >= coord[0] and coord_tuple[1] <= coord[1]:
            return coord
    return None


def label_associations(moral_spans_list, label_spans_list):
    """
    Some moralizing spans have no instance of a specific phenomenon
    (such as protagonists), others have many. It can be useful (when looking
    for specific examples) to have a way to find them. This function should
    make it easy to find all instances of a phenomenon.
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
    Some moralizing spans have no instance of a specific phenomenon
    (such as protagonists), others have many. It can be useful (when looking
    for specific examples) to have a way to find them. This function should
    make it easy to find all instances of a phenomenon.
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


def label_in_list(list, category):
    for element in list:
        if category in element.values():
            return True
    return False


def possible_labels(category):
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
            'Adresassat:in',
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
    jsi = np.log2(p_x_and_y / total_segments)
    return (pmi / (-1 * jsi))


def freq_table(corpus, associations1, associations2, label1, label2):
    counter_1 = 0
    counter_2 = 0
    counter_12 = 0
    counter_none = 0

    for moralization in corpus.moralizations:
        if label_in_list(associations1[moralization], label1):
            if label_in_list(associations2[moralization], label2):
                counter_12 += 1
            else:
                counter_1 += 1
        elif label_in_list(associations2[moralization], label2):
            counter_2 += 1
        else:
            counter_none += 1

    try:
        contingency_table = [
            [counter_12, counter_1],
            [counter_2, counter_none]
        ]
    except ZeroDivisionError:
        print("Error: Division by zero.")

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
    workbook = xlsxwriter.Workbook(filepath)
    worksheet = workbook.add_worksheet("list")

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
