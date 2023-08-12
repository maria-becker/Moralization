import pandas as pd
from HanTa import HanoverTagger as ht
import re
import nltk
import copy


pfad_cloud = r"C:\Users\Bruno\OneDrive\Hausarbeiten\Bachelorarbeit\Bachelorarbeit_Desktop\Data_Jypiter\Spans_and_instances.xlsx"
pfad_local = r"C:\Users\Arbeit\Desktop\Bachelorarbeit\Data\Data_Jypiter_no_bezuglos\Spans and Instances.xlsx"


textsorten_dict = {
    "Leserbriefe-neg-BB-neu-optimiert-RR": "Column10",
    "Interviews-pos-SH-neu-optimiert-AW": "Column6",
    "Gerichtsurteile-neg-AW-neu-optimiert-BB": "Column3",
    "Gerichtsurteile-pos-AW-neu-optimiert-BB": "Column5",
    "Kommentare-pos-RR-neu-optimiert-CK": "Column7",
    "Interviews-neg-SH-neu-optimiert-AW": "Column9",
    "Leserbriefe-pos-BB-neu-optimiert-RR": "Column4",
    "Kommentare-neg-RR-neu-optimiert-CK": "Column8"
}

relev_textsorten_dict = {
    "Leserbriefe-neg-BB-neu-optimiert-RR": "Column10",
    "Interviews-pos-SH-neu-optimiert-AW": "Column6",
    "Gerichtsurteile-neg-AW-neu-optimiert-BB": "Column3",
    "Gerichtsurteile-pos-AW-neu-optimiert-BB": "Column5",
    "Kommentare-pos-RR-neu-optimiert-CK": "Column7",
    "Interviews-neg-SH-neu-optimiert-AW": "Column9",
    "Leserbriefe-pos-BB-neu-optimiert-RR": "Column4",
    "Kommentare-neg-RR-neu-optimiert-CK": "Column8"
}


def add_protagonists_naive():

    # Open the Excel file
    excel_file = pd.ExcelFile(pfad_local)

    # Get the sheet you want to read
    sheet_name = 'spans_out'
    df = excel_file.parse(sheet_name)

    # Print the contents of the sheet

    # Read data
    full_dict = {}
    for column in relev_textsorten_dict:
        protagonisten_dict = {}
        for row in gruppe_list:
            data = df.loc[row, relev_textsorten_dict[column]].lower()
            protagonist_list = data.split(" ### ")
            for protagonist in protagonist_list:
                if protagonist in protagonisten_dict.keys():
                    protagonisten_dict[protagonist] += 1
                else:
                    protagonisten_dict[protagonist] = 1
        sorted_dict = {k: v for k, v in sorted(protagonisten_dict.items(), key=lambda item: item[1])}
        full_dict[column] = sorted_dict

    return full_dict


def add_protagonists_pro():

    tagger = ht.HanoverTagger('morphmodel_ger.pgz')


    # Open the Excel file
    excel_file = pd.ExcelFile(pfad_local)

    # Get the sheet you want to read
    sheet_name = 'spans_out'
    df = excel_file.parse(sheet_name)

    # Print the contents of the sheet

    # Read data
    full_dict = {}
    for column in relev_textsorten_dict:
        protagonisten_dict = {}
        for row in gruppe_list:
            data = df.loc[row, relev_textsorten_dict[column]].lower()
            protagonist_list = data.split(" ### ")
            for protagonist_term in protagonist_list:
                for protagonist in nltk.tokenize.word_tokenize(
                        protagonist_term, language="German"):
                    protagonist = tagger.analyze(protagonist)[0]
                    if protagonist in protagonisten_dict.keys():
                        protagonisten_dict[protagonist] += 1
                    else:
                        protagonisten_dict[protagonist] = 1
        sorted_dict = {k: v for k, v in sorted(
            protagonisten_dict.items(),
            key=lambda item: item[1])
        }
        full_dict[column] = sorted_dict

    return full_dict


def combine_dictionaries(dict_of_dict):
    dict_list = [x for x in dict_of_dict]
    new_dict_of_dict = {}

    while len(dict_list) > 0:
        removed_dict = dict_list[0]
        dict_list.remove(removed_dict)
        match = re.findall("^.*?-", removed_dict)[0]
        for twin in dict_list:
            if match in twin:

                dict1 = dict_of_dict[removed_dict]
                dict2 = dict_of_dict[twin]

                for key in dict2:
                    if key in dict1:
                        dict1[key] += dict2.get(key)
                    else:
                        dict1[key] = dict2.get(key)

                sorted_dict = {k: v for k, v in sorted(
                    dict1.items(), key=lambda item: item[1])
                }

                new_dict_of_dict[match] = sorted_dict

    return new_dict_of_dict


def create_exel_top_hits(meta_dict, n_max=0, pos_list=0, bonus_name=''):
    """
    This function takes a dictionary of dictionaries and creates and excel
    spreadsheet that includes the top n keys.

    Args:
        meta_dict: The dictionary of dictionaries
        n:  The number of results that should be written into the excel file.
            If n=0, all values are written into the file.
        pos_list: The parts of speech that will be considered. If 0, it creates
            four sheets using four different lists.

    Returns:
        Nothing, this writes to a file.

    """

    tagger = ht.HanoverTagger('morphmodel_ger.pgz')

    test_for_n = False
    if n_max == 0:
        test_for_n = True

    for name in meta_dict:
        with pd.ExcelWriter(f'{name}{bonus_name}.xlsx') as writer:
            df = pd.DataFrame()
            df.to_excel(writer, index=False)

    def write_to_excel(meta_dict, n_max, pos_list):

        for name in meta_dict:
            dicty = copy.deepcopy(meta_dict[name])

            if test_for_n:
                n_max = len(dicty)

            # Highlight the words that are not part of the POS list
            for key in dicty:
                relevant = False
                for pos in pos_list:
                    if pos in tagger.analyze(key)[1]:
                        relevant = True
                        break
                if not relevant:
                    dicty[key] = -1

            # Remove the non-relevant words
            for key in list(dicty):
                if dicty[key] == -1:
                    del dicty[key]

            # Sort the dictionary by values in descending order
            sorted_dict = dict(
                sorted(dicty.items(), key=lambda x: x[1], reverse=True))

            # Get the top x items and convert to a DataFrame
            print(list(sorted_dict.items()))
            df = pd.DataFrame(
                list(sorted_dict.items())[:n_max], columns=['key', 'value'])

            # Write the DataFrame to an Excel file
            with pd.ExcelWriter(f'{name}{bonus_name}.xlsx', mode="a", engine="openpyxl",) as writer:
                df.to_excel(writer, sheet_name=pos_list[0], index=False)

    if pos_list == 0:
        copy_dict = meta_dict
        for pos_list in pos_list_list:
            write_to_excel(copy_dict, n_max, pos_list)
    else:
        write_to_excel(meta_dict, n_max, pos_list)

    return True


tag_list_voll = [
    "all",
    "NN", "NE", "PPER", "PRF", "PPOSAT", "PPOSS", "PDAT", "PDS",
    "PIAT", "PIDAT", "PIS", "PWS", "PWAT"]
tag_list_low = [
    "best",
    "NN", "NE", "PPER", "PRF", "PPOSAT", "PPOSS",
    "PIAT", "PIDAT", "PIS", "PWS", "PWAT"]
tag_list_nomen = [
    "nouns",
    "NN", "NE"]
tag_list_names = [
    "names",
    "NE"
]
tag_list_prnomen = [
    "pronouns",
    "PPER", "PRF", "PPOSAT", "PPOSS", "PDAT", "PDS",
    "PIAT", "PIDAT", "PIS", "PWS", "PWAT"]

# Enthält PIDAT (mit Determiner) nicht
tag_list_indef_pron = [
    "indefinitivpronomen",
    "PIAT", "PIS"]

pos_list_list = [
    tag_list_voll,
    tag_list_low,
    tag_list_nomen,
    tag_list_names,
    tag_list_prnomen,
    tag_list_indef_pron
]

gruppe_list = [40]

testy = add_protagonists_pro()
testy2 = combine_dictionaries(testy)
create_exel_top_hits(testy2, bonus_name="Forderer")
