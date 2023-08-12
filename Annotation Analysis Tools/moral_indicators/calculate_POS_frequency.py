import pandas as pd
from HanTa import HanoverTagger as ht
import re
import nltk
import copy


pfad_cloud = r"C:\Users\Bruno\OneDrive\Hausarbeiten\Bachelorarbeit\Bachelorarbeit_Desktop\Data_Jypiter_no_bezugslos\Spans and instances.xlsx"
pfad_local = r"C:\Users\Arbeit\Desktop\Bachelorarbeit\Data\Data_Jypiter_no_bezuglos\Spans and instances.xlsx"

gruppe_list = [33, 34, 35, 36, 37]
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
    print(df)

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


def calculate_pos_freq(dict_of_dict_summed):

    tagger = ht.HanoverTagger('morphmodel_ger.pgz')

    for dictkey in dict_of_dict_summed:

        sum_nouns = 0
        sum_name = 0
        sum_pronouns = 0

        for key in dict_of_dict_summed[dictkey]:

            for word in nltk.tokenize.word_tokenize(
                key,
                language="German"
            ):
                pos = tagger.analyze(word)[1]
                if pos == "NN":
                    sum_nouns += dict_of_dict_summed[dictkey][key]
                    break
                elif pos == "NE":
                    sum_name += dict_of_dict_summed[dictkey][key]
                    break
            else:
                sum_pronouns += dict_of_dict_summed[dictkey][key]

        print(dictkey)
        print("NOMEN: ", str(sum_nouns))
        print("NAMEN: ", str(sum_name))
        print("PRONOMEN: ", str(sum_pronouns))

    return True


dicty = (combine_dictionaries(add_protagonists_naive()))
calculate_pos_freq(dicty)
