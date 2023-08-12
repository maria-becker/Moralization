import nltk
import corpus_extraction as ce
import xmi_analysis_util as xau


def protagonists_in_context(
    word_list,
    filepath,
    protagonist_list=None
):
    """
    This function creates a list of moralizations in which
    one or more of the specified protagonist terms are found.

    Parameters:
        word_list: List of tokens to look for in the protagonist data.
                    These tokens should be lowercase.
        filepath: path to corpus file that is being searched.
        protagonist_list: Optionally, you can pass the function a
            list of protagonist dictionaries. Otherwise (if None), the
            function calls list_protagonists_from_xmi() with default params.
            Default: None
    Returns:
        A list of strings which are moralizing speechacts that include
        the specified term as part of a protagonist span.
    """

    text = ce.text_from_xmi(filepath)
    moralization_list = ce.list_moralizations_from_xmi(filepath)
    if not protagonist_list:
        protagonist_list = ce.list_protagonists_from_xmi(filepath)

    relevant_spans_list = []
    association = xau.protagonist_associations(
        moralization_list,
        protagonist_list
    )
    relevant_spans_list = []
    for moralization in association.keys():
        for protagonist in association[moralization]:
            tokenized = nltk.tokenize.word_tokenize(
                xau.get_span(text, protagonist), language='german')
            tokenized = [x.lower() for x in tokenized]
            for token in tokenized:
                if token in word_list:
                    relevant_spans_list.append(moralization)
                    break

    return_string_list = []
    for moralization in relevant_spans_list:
        return_string_list.append(xau.get_span(text, moralization))

    return return_string_list


def highlight_protagonists_count(
    filepath,
    count,
    protagonist_list=None
):
    """
    This function creates a list of moralizations in which
    the specified number of protagonist terms are found.
    The terms are highlighted.

    Parameters:
        filepath: path to corpus file that is being searched.
        count: The exact amount of protagonists that you want
            to have in moralizations that are returned.
        protagonist_list: Optionally, you can pass the function a
            list of protagonist dictionaries. Otherwise (if None), the
            function calls list_protagonists_from_xmi() with default params.
            Keep in mind that default does not skip duplicates.
            Default: None
    Returns:
        A list of moralizing speech acts with 'count' protagonists.
        The entries of the list are strings. Protagonist spans are capitalized
        as highlight.
    """

    text = ce.text_from_xmi(filepath)
    moralization_list = ce.list_moralizations_from_xmi(filepath)
    if not protagonist_list:
        protagonist_list = ce.list_protagonists_from_xmi(filepath)

    protagonist_association = xau.protagonist_associations(
        moralization_list,
        protagonist_list
    )

    relevant_spans_dict = {
        key: protagonist_association[key] for key
        in protagonist_association.keys()
        if len(protagonist_association[key]) == count
    }

    return_string_list = []
    for moralization_tuple in relevant_spans_dict:
        for protagonist in relevant_spans_dict[moralization_tuple]:
            if xau.get_span(text, protagonist):
                text = (
                    text[:(protagonist[0])]
                    + xau.special_upper(xau.get_span(text, protagonist))
                    + text[(protagonist[1]):]
                )
        output_string = xau.get_span(text, moralization_tuple)
        return_string_list.append(output_string)

    return return_string_list


def highlight_protagonists(
    filepath,
    condition_list=[],
    protagonist_list=None
):
    """
    This function creates a list of moralizations in which
    the specified protagonist terms are found.
    The terms are highlighted.

    Parameters:
        filepath: path to corpus file that is being searched.
        condition_list: The tags you that the protagonists must have
            so that they are counted and highlighted.
        protagonist_list: Optionally, you can pass the function a
            list of protagonist dictionaries. Otherwise (if None), the
            function calls list_protagonists_from_xmi() with default params.
            Default: None
    Returns:
        A list of moralizing speech acts with 'count' protagonists.
        The entries of the list are strings. Protagonist spans are capitalized
        as highlight.
    """

    text = ce.text_from_xmi(filepath)
    moralization_list = ce.list_moralizations_from_xmi(filepath)
    if not protagonist_list:
        protagonist_list = ce.list_protagonists_from_xmi(filepath)

    matched_protag_list = []
    for protagonist in protagonist_list:
        if all(item in protagonist.values() for item in condition_list):
            matched_protag_list.append(protagonist)

    # Create dictionary of relevant spans
    relevant_spans_dict = {}
    for matched_protag in matched_protag_list:
        span = xau.inside_of(
            moralization_list, matched_protag["Coordinates"]
        )
        if span in relevant_spans_dict.keys():
            relevant_spans_dict[span].append(matched_protag["Coordinates"])
        else:
            relevant_spans_dict[span] = [matched_protag["Coordinates"]]

    return_string_list = []
    for moralization_tuple in relevant_spans_dict:
        for protagonist in relevant_spans_dict[moralization_tuple]:
            if xau.get_span(text, protagonist):
                text = (
                    text[:(protagonist[0])]
                    + xau.special_upper(xau.get_span(text, protagonist))
                    + text[(protagonist[1]):]
                )
        output_string = xau.get_span(text, moralization_tuple)
        return_string_list.append(output_string)

    return return_string_list


def get_protag_spans_condition(filepath, condition_list):
    """
    Allows you to get a list of protagonists where every
    protagonists has all annotation categories passed
    to this function as a list.

    Parameters:
        filepath: path to corpus file that is being searched.
        condition_list: list of conditions that protagonists
                        must fullfil.
                        Example: ['Forderer:in', 'Institution']
    Returns:
        List of protagonist dictionaries. See documentation of
        list_protagonists_from_xmi() for more info.
    """

    text = ce.text_from_xmi(filepath)
    protagonist_list = ce.list_protagonists_from_xmi(filepath)

    # Create dictionary of relevant spans
    matched_protag_list = []
    for protagonist in protagonist_list:
        if all(item in protagonist.values() for item in condition_list):
            matched_protag_list.append(protagonist)

    # Get the protagonist spans
    return_list = [
        xau.get_span(
            text,
            protagonist["Coordinates"]
        )
        for protagonist in matched_protag_list
    ]

    return return_list


def filenames(text_type=None):
    """
    Instead of typing filenames every time, this function
    can be used to get the filenames of one text genre or
    all filenames.
    NOTE: Includes only newspaper genres.

    Parameters:
        text_type: If you want only the filenames of a
                    specific genre, name that genre here.
                    default: None
    Returns:
        List of filenames either all or just the ones
        from the specified genre.
    """

    file_type_dict = {
        "Gerichtsurteile": [
            "Gerichtsurteile-neg-AW-neu-optimiert-BB.xmi",
            "Gerichtsurteile-pos-AW-neu-optimiert-BB.xmi"
        ],
        "Interviews": [
            "Interviews-neg-SH-neu-optimiert-AW.xmi",
            "Interviews-pos-SH-neu-optimiert-AW.xmi"
        ],
        "Kommentare": [
            "Kommentare-neg-RR-neu-optimiert-CK.xmi",
            "Kommentare-pos-RR-neu-optimiert-CK.xmi"
        ],
        "Leserbriefe": [
            "Leserbriefe-neg-BB-neu-optimiert-RR.xmi",
            "Leserbriefe-pos-BB-neu-optimiert-RR.xmi"
        ]
    }

    file_list = [
        "Gerichtsurteile-neg-AW-neu-optimiert-BB.xmi",
        "Gerichtsurteile-pos-AW-neu-optimiert-BB.xmi",
        "Interviews-neg-SH-neu-optimiert-AW.xmi",
        "Interviews-pos-SH-neu-optimiert-AW.xmi",
        "Kommentare-neg-RR-neu-optimiert-CK.xmi",
        "Kommentare-pos-RR-neu-optimiert-CK.xmi",
        "Leserbriefe-neg-BB-neu-optimiert-RR.xmi",
        "Leserbriefe-pos-BB-neu-optimiert-RR.xmi"
    ]

    if text_type:
        return file_type_dict[text_type]
    else:
        return file_list


def double_role_highlight(filepath, protagonist_list=None):
    """
    This function creates a list of moralizations in which
    a role is filled by several different protagonists.
    The terms are highlighted.

    Parameters:
        filepath: path to corpus file that is being searched.
        protagonist_list: Optionally, you can pass the function a
            list of protagonist dictionaries. Otherwise (if None), the
            function calls list_protagonists_from_xmi() with default params.
            Default: None
    Returns:
        This function creates a list of moralizations in which
        a role is filled by several different protagonists.
        The entries of the list are strings. Protagonist spans are capitalized
        as highlight.
    """

    text = ce.text_from_xmi(filepath)
    moralization_list = ce.list_moralizations_from_xmi(filepath)
    if not protagonist_list:
        protagonist_list = ce.list_protagonists_from_xmi(
            filepath, skip_duplicates=True,
        )

    dictionary_test = {}
    dictionary_main = {}
    for moralization in moralization_list:
        dictionary_test[moralization] = []
        dictionary_main[moralization] = []

    for new_protagonist in protagonist_list:
        moral_span = xau.inside_of(
            moralization_list, new_protagonist["Coordinates"])
        try:
            for old_protagonist in dictionary_test[moral_span]:
                if old_protagonist["Rolle"] == new_protagonist["Rolle"]:
                    try:
                        dictionary_main[moral_span].append(old_protagonist)
                        dictionary_main[moral_span].append(new_protagonist)
                    except KeyError:
                        continue
        except KeyError:
            continue
        dictionary_test[moral_span].append(new_protagonist)

    final_dict = {
        key: value for key, value in dictionary_main.items() if value != []}

    return_string_list = []
    for moralization_tuple in final_dict:
        for protagonist in final_dict[moralization_tuple]:
            if xau.get_span(text, protagonist["Coordinates"]):
                text = (
                    text[:(protagonist["Coordinates"][0])]
                    + xau.special_upper(
                        xau.get_span(text, protagonist["Coordinates"])
                    )
                    + text[(protagonist["Coordinates"][1]):]
                )
        output_string = xau.get_span(text, moralization_tuple)
        return_string_list.append(output_string)

    return return_string_list


def protagonist_combinations(filepath):
    """
    Protagonists in moralizations appear in different combinations,
    e.g. 'Adressat' + 'Forderer' but not 'Benefizient'. The following
    function creates a table for the frequency of these combinations.

    Parameters:
        filepath: Path to corpus file that is being analyzed.
    Returns:
        Dictionary. Keys are the possible combinations, where
        -A stands for 'Adressat'
        -B stands for 'Benefizient'
        -F stands for 'Forderer'
        The values are the absolute frequencies of the combinations.
    """

    distribution_dict = {
        "A": 0, "B": 0, "F": 0,
        "A+B": 0, "A+F": 0, "B+F": 0, "A+B+F": 0, "none": 0
    }

    protagonists = ce.list_protagonists_from_xmi(
        filepath, ignore_list=["Kein_Bezug"])
    moralizations = ce.list_moralizations_from_xmi(filepath)
    associations = xau.protagonist_associations(moralizations, protagonists)

    infos = {}
    for moralization_span in associations.keys():
        info = []
        for protagonist_span in associations[moralization_span]:
            for protagonist_dict in protagonists:
                if protagonist_span == protagonist_dict["Coordinates"]:
                    info.append(protagonist_dict["Rolle"])
        infos[moralization_span] = info

    for info in infos.values():
        if "Adresassat:in" in info:
            if "Benefizient:in" in info:
                if "Forderer:in" in info:
                    distribution_dict["A+B+F"] += 1
                    continue
                distribution_dict["A+B"] += 1
                continue
            if "Forderer:in" in info:
                distribution_dict["A+F"] += 1
                continue
            distribution_dict["A"] += 1
            continue
        elif "Benefizient:in" in info:
            if "Forderer:in" in info:
                distribution_dict["B+F"] += 1
                continue
            distribution_dict["B"] += 1
            continue
        elif "Forderer:in" in info:
            distribution_dict["F"] += 1
            continue
        else:
            distribution_dict["none"] += 1

    return distribution_dict


def multi_role_protagonists(file):
    """
    Some protagonists have several roles at once.
    This function returns moralizing speech acts where this is the case,
    alongside which roles are being filled by the same protagonist.

    Parameters:
        file: Path to corpus file that is being analyzed.
    Returns:
        Dictionary. The keys are the coordinates for the moralizing instances
        that the protagonist is part of. The values are lists of the roles
        that are being filled by the same protagonist.
    """

    protagonists = ce.list_protagonists_from_xmi(file)
    moralizations = ce.list_moralizations_from_xmi(file)
    text = ce.text_from_xmi(file)

    associations = xau.label_associations(moralizations, protagonists)
    double_role_dict = {}

    for morali in associations.keys():
        singles_list = []
        duplicate_list = []
        for protagonist in associations[morali]:
            if protagonist not in singles_list:
                singles_list.append(protagonist)
            else:
                duplicate_list.append(protagonist)
        if duplicate_list:
            double_role_dict[morali] = duplicate_list

    double_role_output = {}
    for morali in double_role_dict.keys():
        span = xau.get_span(text, morali)
        info = []
        for protagonist in double_role_dict[morali]:
            info.append(xau.get_span(text, protagonist))
            for entry in protagonists:
                if protagonist == entry["Coordinates"]:
                    info.append(entry["Rolle"])
        double_role_output[span] = info

    return double_role_output


def multi_role_combinations(double_role_output):
    """
    This function returns the distribution of the different possible
    combinations where one protagonist has multiple roles.

    Parameters:
        double_role_output: dictionary as created by multi_role_protagonists()
    Returns:
    Returns:
        Dictionary. Keys are the possible combinations, where
        -A stands for 'Adressat'
        -B stands for 'Benefizient'
        -F stands for 'Forderer'
        The values are the absolute frequencies of the combinations.
    """

    distribution_dict = {"A+B": 0, "A+F": 0, "B+F": 0, "A+B+F": 0, "error": 0}
    for info in double_role_output.values():
        if "Adresassat:in" in info:
            if "Benefizient:in" in info:
                if "Forderer:in" in info:
                    distribution_dict["A+B+F"] += 1
                    continue
                distribution_dict["A+B"] += 1
                continue
            if "Forderer:in" in info:
                distribution_dict["A+F"] += 1
                continue
        elif "Benefizient:in" in info:
            if "Forderer:in" in info:
                distribution_dict["B+F"] += 1
                continue
            else:
                distribution_dict["error"] += 1
        else:
            distribution_dict["error"] += 1

    return distribution_dict
