import xml.etree.ElementTree as ET
import os
import xmi_conversion_util as util
import xlsxwriter
import zipfile


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
        category = span.get('KAT1MoralisierendesSegment')

        if category:
            if category != "Keine Moralisierung":
                data_dict = {
                    "Coordinates":
                        (int(span.get("begin")), int(span.get("end"))),
                    "Category":
                        category
                }
                moral_spans_list.append(data_dict)

    return moral_spans_list


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


def list_protagonists_from_xmi(
    filepath,
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


def list_communication_from_xmi(filepath):
    tree = ET.parse(filepath)
    root = tree.getroot()

    span_list = root.findall("{http:///custom.ecore}Span")

    # Get all moralizing instances
    morals_list = []
    for span in span_list:
        category = span.get('KommunikativeFunktion')

        if category:
            data_dict = {
                "Coordinates":
                    (int(span.get("begin")), int(span.get("end"))),
                "Category":
                    category
            }
            morals_list.append(data_dict)

    return morals_list


def list_demand_from_xmi(filepath):
    tree = ET.parse(filepath)
    root = tree.getroot()

    span_list = root.findall("{http:///custom.ecore}Span")

    # Get all moralizing instances
    morals_list = []
    for span in span_list:
        category = span.get('KAT5Ausformulierung')

        if category:
            data_dict = {
                "Coordinates":
                    (int(span.get("begin")), int(span.get("end"))),
                "Category":
                    category
            }
            morals_list.append(data_dict)

    return morals_list


def list_explicit_from_xmi(filepath):
    tree = ET.parse(filepath)
    root = tree.getroot()

    span_list = root.findall("{http:///custom.ecore}Span")

    # Get all moralizing instances
    morals_list = []
    for span in span_list:
        category = span.get('Forderung')

        if category:
            data_dict = {
                "Coordinates":
                    (int(span.get("begin")), int(span.get("end"))),
                "Category":
                    category
            }
            morals_list.append(data_dict)

    return morals_list


def get_example_string(listy):
    str_to_write = ""
    for item in listy:
        if str_to_write != "":
            str_to_write = str_to_write + "; "
        str_to_write = str_to_write + item[0] + ": " + item[1]
    return str_to_write


def get_example_string_impl(listy):
    str_to_write = ""
    for item in listy:
        if str_to_write != "":
            str_to_write = str_to_write + "; "
        str_to_write = str_to_write + item[0]
    return str_to_write


def get_category_string(listy):
    category_dict = {}

    for item in listy:
        if item[0] in category_dict.keys():
            category_dict[item[0]] += 1
        else:
            category_dict[item[0]] = 1
    str_to_write = ""

    for category in category_dict.keys():
        if str_to_write != "":
            str_to_write = (
                str_to_write
                + "; "
            )
        str_to_write = (
            str_to_write
            + category
            + ": "
            + str(category_dict[category])
        )

    return str_to_write


def category_list(anno_list, moralization, text):
    listy = []
    for moral in anno_list:
        if util.inside_of(
            moralization["Coordinates"],
            moral["Coordinates"]

        ):
            listy.append(
                (
                    moral["Category"],
                    util.get_span(text, moral["Coordinates"]),
                    moral["Coordinates"]
                )
            )
    return listy


def get_protag_example_string(listy):
    str_to_write = ""
    for item in listy:
        cat_str = "".join(["(", ", ".join(filter(None, item[0:3])), ")"])
        if str_to_write != "":
            str_to_write = str_to_write + "; "
        str_to_write = str_to_write + cat_str + ": " + item[3]
    return str_to_write


def get_protagonist_string(listy):
    category_dict = {}

    for item in listy:
        cat_str = "".join(["(", ", ".join(filter(None, item[0:3])), ")"])
        if cat_str in category_dict.keys():
            category_dict[cat_str] += 1
        else:
            category_dict[cat_str] = 1
    str_to_write = ""

    for category in category_dict.keys():
        if str_to_write != "":
            str_to_write = (
                str_to_write
                + "; "
            )
        str_to_write = (
            str_to_write
            + category
            + ": "
            + str(category_dict[category])
        )

    return str_to_write


def protagonist_list(anno_list, moralization, text):
    listy = []
    for protagonist in anno_list:
        if util.inside_of(
            moralization["Coordinates"],
            protagonist["Coordinates"]

        ):
            listy.append(
                (
                    protagonist["Rolle"],
                    protagonist["Gruppe"],
                    protagonist["own/other"],
                    util.get_span(text, protagonist["Coordinates"]),
                    protagonist["Coordinates"]
                )
            )
    return listy


def write_excel_count(sourcepath, goalpath):
    text = text_from_xmi(sourcepath)
    moralizations = list_moralizations_from_xmi(sourcepath)
    obj_morals = list_obj_moral_from_xmi(sourcepath)
    subj_morals = list_subj_moral_from_xmi(sourcepath)
    protagonists = list_protagonists_from_xmi(sourcepath)
    communications = list_communication_from_xmi(sourcepath)
    demands = list_demand_from_xmi(sourcepath)
    explicits = list_explicit_from_xmi(sourcepath)

    workbook = xlsxwriter.Workbook(goalpath)
    worksheet = workbook.add_worksheet()

    header_format = workbook.add_format({'bold': True})
    worksheet.freeze_panes(1, 0)

    worksheet.write(0, 0, "Text", header_format)
    worksheet.write(0, 1, "Typ", header_format)
    worksheet.write(0, 2, "# Explizite Moralwerte", header_format)
    worksheet.write(0, 3, "Label Explizite Moralwerte", header_format)
    worksheet.write(0, 4, "Spans Explizite Moralwerte", header_format)
    worksheet.write(0, 5, "# Subjektive Ausdrücke", header_format)
    worksheet.write(0, 6, "Label Subjektive Ausdrücke", header_format)
    worksheet.write(0, 7, "Spans Subjektive Ausdrücke", header_format)
    worksheet.write(0, 8, "# Kommunikative Funktionen", header_format)
    worksheet.write(0, 9, "Label Kommunikative Funktionen", header_format)
    worksheet.write(0, 10, "Spans Kommunikative Funktionen", header_format)
    worksheet.write(0, 11, "# Protagonist:innen", header_format)
    worksheet.write(0, 12, "Label Protagonist:innen", header_format)
    worksheet.write(0, 13, "Spans Protagonist:innen", header_format)
    worksheet.write(0, 14, "# Explizite Forderungen", header_format)
    worksheet.write(0, 15, "Label Explizite Forderung", header_format)
    worksheet.write(0, 16, "Spans Explizite Forderung", header_format)
    worksheet.write(0, 17, "# Implizite Forderungen", header_format)
    worksheet.write(0, 18, "Label Implizite Forderung", header_format)
    worksheet.write(0, 19, "Spans Implizite Forderung", header_format)

    row = 1

    for moralization in moralizations:
        worksheet.write(
            row, 0, util.get_span(text, moralization["Coordinates"]))
        worksheet.write(
            row, 1, moralization["Category"])

        # Moralisierung und Typ
        anno_list = category_list(obj_morals, moralization, text)
        cat_str = get_category_string(anno_list)
        expl_str = get_example_string(anno_list)
        worksheet.write(row, 2, len(set([x[-1:] for x in anno_list])))
        worksheet.write(row, 3, cat_str)
        worksheet.write(row, 4, expl_str)

        # Moralwerte ('objektiv')
        anno_list = category_list(subj_morals, moralization, text)
        cat_str = get_category_string(anno_list)
        expl_str = get_example_string(anno_list)
        worksheet.write(row, 5, len(set([x[-1:] for x in anno_list])))
        worksheet.write(row, 6, cat_str)
        worksheet.write(row, 7, expl_str)

        # MoraLwerte ('subjektiv')
        anno_list = category_list(communications, moralization, text)
        cat_str = get_category_string(anno_list)
        expl_str = get_example_string(anno_list)
        worksheet.write(row, 8, len(set([x[-1:] for x in anno_list])))
        worksheet.write(row, 9, cat_str)
        worksheet.write(row, 10, expl_str)

        # Protagonisten
        anno_list = protagonist_list(protagonists, moralization, text)
        cat_str = get_protagonist_string(anno_list)
        expl_str = get_protag_example_string(anno_list)
        worksheet.write(row, 11, len(set([x[-1:] for x in anno_list])))
        worksheet.write(row, 12, cat_str)
        worksheet.write(row, 13, expl_str)

        # Forderungen explizit
        anno_list = category_list(explicits, moralization, text)
        cat_str = get_category_string(anno_list)
        expl_str = get_example_string(anno_list)
        worksheet.write(row, 14, len(set([x[-1:] for x in anno_list])))
        worksheet.write(row, 15, cat_str)
        worksheet.write(row, 16, expl_str)

        # Forderungen implizit
        anno_list = category_list(demands, moralization, text)
        expl_str = get_example_string_impl(anno_list)
        worksheet.write(row, 17, len(set([x[-1:] for x in anno_list])))
        if len(anno_list) > 0:
            worksheet.write(row, 18, ("implizit: " + str(len(anno_list))))
        worksheet.write(row, 19, expl_str)

        row += 1

    workbook.close()


def write_excel_minimal(sourcepath, goalpath):
    text = text_from_xmi(sourcepath)
    moralizations = list_moralizations_from_xmi(sourcepath)
    obj_morals = list_obj_moral_from_xmi(sourcepath)
    subj_morals = list_subj_moral_from_xmi(sourcepath)
    protagonists = list_protagonists_from_xmi(sourcepath)
    communications = list_communication_from_xmi(sourcepath)
    demands = list_demand_from_xmi(sourcepath)
    explicits = list_explicit_from_xmi(sourcepath)

    workbook = xlsxwriter.Workbook(goalpath)
    worksheet = workbook.add_worksheet()

    header_format = workbook.add_format({'bold': True})
    worksheet.freeze_panes(1, 0)

    worksheet.write(0, 0, "Text", header_format)
    worksheet.write(0, 1, "Typ", header_format)
    worksheet.write(0, 2, "Label Explizite Moralwerte", header_format)
    worksheet.write(0, 3, "Spans Explizite Moralwerte", header_format)
    worksheet.write(0, 4, "Label Subjektive Ausdrücke", header_format)
    worksheet.write(0, 5, "Spans Subjektive Ausdrücke", header_format)
    worksheet.write(0, 6, "Label Kommunikative Funktionen", header_format)
    worksheet.write(0, 7, "Spans Kommunikative Funktionen", header_format)
    worksheet.write(0, 8, "Label Protagonist:innen", header_format)
    worksheet.write(0, 9, "Spans Protagonist:innen", header_format)
    worksheet.write(0, 10, "Label Explizite Forderungen", header_format)
    worksheet.write(0, 11, "Spans Explizite Forderung", header_format)
    worksheet.write(0, 12, "Label Implizite Forderungen", header_format)
    worksheet.write(0, 13, "Spans Implizite Forderung", header_format)

    row = 1

    for moralization in moralizations:
        worksheet.write(
            row, 0, util.get_span(text, moralization["Coordinates"]))
        worksheet.write(
            row, 1, moralization["Category"])

        # Moralisierung und Typ
        anno_list = category_list(obj_morals, moralization, text)
        cat_str = get_category_string(anno_list)
        expl_str = get_example_string(anno_list)
        worksheet.write(row, 2, cat_str)
        worksheet.write(row, 3, expl_str)

        # Moralwerte ('objektiv')
        anno_list = category_list(subj_morals, moralization, text)
        cat_str = get_category_string(anno_list)
        expl_str = get_example_string(anno_list)
        worksheet.write(row, 4, cat_str)
        worksheet.write(row, 5, expl_str)

        # MoraLwerte ('subjektiv')
        anno_list = category_list(communications, moralization, text)
        cat_str = get_category_string(anno_list)
        expl_str = get_example_string(anno_list)
        worksheet.write(row, 6, cat_str)
        worksheet.write(row, 7, expl_str)

        # Protagonisten
        anno_list = protagonist_list(protagonists, moralization, text)
        cat_str = get_protagonist_string(anno_list)
        expl_str = get_protag_example_string(anno_list)
        worksheet.write(row, 8, cat_str)
        worksheet.write(row, 9, expl_str)

        # Forderungen explizit
        anno_list = category_list(explicits, moralization, text)
        cat_str = get_category_string(anno_list)
        expl_str = get_example_string(anno_list)
        worksheet.write(row, 10, cat_str)
        worksheet.write(row, 11, expl_str)

        # Forderungen implizit
        anno_list = category_list(demands, moralization, text)
        cat_str = get_category_string(anno_list)
        expl_str = get_example_string_impl(anno_list)
        if len(anno_list) > 0:
            worksheet.write(row, 12, ("implizit: " + str(len(anno_list))))
        worksheet.write(row, 13, expl_str)

        row += 1

    workbook.close()


def extract_files(root_folder, goal_folder):

    for root, dirs, _ in os.walk(root_folder):
        for directory in dirs:
            subdir = os.path.join(root, directory)
            print(subdir)
            extracted = False
            for file in os.listdir(subdir):
                if (file.endswith('.zip') and file[:-3] in directory):
                    zip_path = os.path.join(subdir, file)
                    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                        for zip_file in zip_ref.namelist():
                            if (zip_file.endswith('.xmi')
                                    and zip_file[:-3] in zip_file):
                                destination_folder = os.path.join(
                                    goal_folder,
                                    directory)
                                os.makedirs(
                                    destination_folder,
                                    exist_ok=True)
                                zip_ref.extractall(destination_folder)
                                extracted = True

            if not extracted:
                for file in os.listdir(subdir):
                    if not (file.startswith('INITIAL_CAS')):
                        zip_path = os.path.join(subdir, file)
                        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                            for zip_file in zip_ref.namelist():
                                if (zip_file.endswith('.xmi')
                                        and zip_file[:-3] in zip_path):
                                    destination_folder = os.path.join(
                                        goal_folder,
                                        directory)
                                    os.makedirs(
                                        destination_folder,
                                        exist_ok=True)
                                    zip_ref.extractall(destination_folder)
                                    extracted = True


def xmi_iterate_count(root_folder, goal_folder):
    for root, _, files in os.walk(root_folder):
        for file in files:
            if file.endswith('.xmi'):
                filename = os.path.splitext(os.path.basename(root))[0]
                filename = filename + '.xlsx'
                goalpath = os.path.join(goal_folder, filename)
                sourcepath = os.path.join(root, file)
                print(goalpath)
                write_excel_count(sourcepath, goalpath)


def xmi_iterate_minimal(root_folder, goal_folder):
    for root, _, files in os.walk(root_folder):
        for file in files:
            if file.endswith('.xmi'):
                filename = os.path.splitext(os.path.basename(root))[0]
                filename = filename + '.xlsx'
                goalpath = os.path.join(goal_folder, filename)
                sourcepath = os.path.join(root, file)
                print(goalpath)
                write_excel_minimal(sourcepath, goalpath)


def xmi_iterate_german_count(root_folder, goal_folder):
    for root, _, files in os.walk(root_folder):
        for file in files:
            if file.endswith('.xmi'):
                filename = os.path.splitext(os.path.basename(file))[0]
                filename = filename + '.xlsx'
                goalpath = os.path.join(goal_folder, filename)
                sourcepath = os.path.join(root, file)
                print(goalpath)
                write_excel_count(sourcepath, goalpath)


def xmi_iterate_german_minimal(root_folder, goal_folder):
    for root, _, files in os.walk(root_folder):
        for file in files:
            if file.endswith('.xmi'):
                filename = os.path.splitext(os.path.basename(file))[0]
                filename = filename + '.xlsx'
                goalpath = os.path.join(goal_folder, filename)
                sourcepath = os.path.join(root, file)
                print(goalpath)
                write_excel_minimal(sourcepath, goalpath)
