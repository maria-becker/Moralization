def inside_of(coord_outer, coord_inner):
    """
    Checks whether the specific coordinates
    are inside any of the coordinates on the list
    Returns the first match, or None if there is no match.
    """

    if ((coord_outer[0] <= coord_inner[0])
            and (coord_inner[1] <= coord_outer[1])):
        return True
    return False


def protagonist_associations(moral_spans_list, protagonist_spans_list):
    """
    Some moralizing spans have no instance of a specific phenomenon
    (such as protagonists), others have many. It can be useful (when looking
    for specific examples) to have a way to find them. This function should
    make it easy to find all instances of a phenomenon.
    """

    protagonist_dict = {}

    for moralization in moral_spans_list:
        protagonist_dict[moralization] = []
    for protagonist in protagonist_spans_list:
        moral_span = inside_of(
            moral_spans_list, protagonist["Coordinates"])
        try:
            protagonist_dict[moral_span].append(protagonist["Coordinates"])
        except KeyError:
            print("".join(("KeyError: ", str(protagonist["Coordinates"]))))

    return protagonist_dict


def get_span(text, coordinates):
    try:
        span = text[coordinates[0]:(coordinates[1])]
        return span
    except TypeError:
        print("Error getting span.")
        return None
