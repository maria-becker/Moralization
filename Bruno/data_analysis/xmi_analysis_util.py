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
