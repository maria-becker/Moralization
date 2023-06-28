import os
from collections import Counter
import pprint as pp
import pandas as pd
import nltk
from nltk.tokenize import word_tokenize, sent_tokenize
import xlsxwriter
import regex as re
import json
import ast


def merge_excel(file_dict, value):
    excl_list = []
    for file in file_dict[value]:
        excl_list.append(pd.read_excel(file, header=None))

    # create a new dataframe to store the
    # merged excel file.
    excl_merged = pd.DataFrame()

    excl_merged = pd.concat(excl_list, axis=0, ignore_index=True, sort=False)

    # exports the dataframe into excel file with
    # specified name.
    excl_merged.to_excel(
        f'WikibooksNonfi_{value}.xlsx', header=None, index=False)
    return None


def print_moral_sentences(corpus_file_name, sheet_name):

    morallist = pd.read_excel(
        "Morallexikon_IT-überarbeitet.xlsx",
        sheet_name,
        header=None
    )

    # Sometimes you have to change the encoding type (utf-8, utf-16, ...)
    with open(corpus_file_name, 'r', errors='ignore') as f:
        file_contents = f.read()

    topic_list = ast.literal_eval(file_contents)

    morallexikon = morallist[0].tolist()
    sentence_list = []
    moral_library = {}

    for body in topic_list:
        metadata = corpus_file_name.replace('txt', '')
        metadata = metadata.replace('%', ':')
        metadata = metadata.replace('#', '')
        metadata = metadata.replace('.', '')

        if not re.match('\S{33,100}', body):
            # Finds all matches and their context
            try:
                paragraph_sentences = sent_tokenize(body)
                # if len(paragraph_sentences) > 1:
                paragraph_lowered_sentences = [x.lower() for x in paragraph_sentences]

                for i, sentence in enumerate(paragraph_lowered_sentences):
                    sentence_words = word_tokenize(sentence)

                    for word in sentence_words:
                        if word in morallexikon:
                            precontext = ""
                            postcontext = ""
                            if i > 1:
                                precontext = paragraph_sentences[i - 2] + " " + paragraph_sentences[i - 1]
                            elif i > 0:
                                precontext = paragraph_sentences[i - 1]
                            if i + 2 < len(paragraph_sentences):
                                postcontext = paragraph_sentences[i + 1] + " " + paragraph_sentences[i + 2]
                            elif i + 1 < len(paragraph_sentences):
                                postcontext = paragraph_sentences[i + 1]

                            metadata_string = metadata

                            chunk = [
                                word,
                                precontext,
                                paragraph_sentences[i],
                                postcontext,
                                metadata_string,
                            ]

                            sentence_list.append(chunk)

                            if word in moral_library.keys():
                                moral_library[word] += 1
                            else:
                                moral_library[word] = 1

                            break

            except IndexError:
                print('lol')

    print(moral_library)
    return sentence_list


def to_excel_bold(data, corpus, sheet_name):

    workbook = xlsxwriter.Workbook(f'{corpus}_{sheet_name}2.0.xlsx')
    worksheet = workbook.add_worksheet()
    bold = workbook.add_format({'bold': True})

    row = 0
    for element in data:
        word = element[0]
        list_sentence = element[2].split(word)

        edited_sentence = ""
        if list_sentence[0] != "" and len(list_sentence) >= 2:
            edited_sentence = ""
            for i in range(len(list_sentence) - 1):
                edited_sentence = edited_sentence \
                    + list_sentence[i] \
                    + "###" \
                    + f"{word}" \
                    + "###" \
                    + list_sentence[i + 1]
                edited_sentence.capitalize()
                edited_sentence.replace("  ", " ")

        else:
            word = word.capitalize()
            list_sentence = element[2].split(word)
            for i in range(len(list_sentence) - 1):
                edited_sentence = edited_sentence \
                    + list_sentence[i] \
                    + "###" \
                    + f"{word}" \
                    + "###" \
                    + list_sentence[i + 1]

        worksheet.write(row, 0, element[4] + f", word: {word}", bold)
        row += 1

        cleaned_str = ""

        if len(element[1]) > 0:
            cleaned_str = element[1] + " " + edited_sentence + " " + element[3]
        else:
            cleaned_str = edited_sentence + " " + element[3]

        cleaned_str = cleaned_str.replace('\n', ' ')
        while '  ' in cleaned_str:
            cleaned_str = cleaned_str.replace('  ', ' ')

        worksheet.write(row, 0, cleaned_str)

        row += 1

    workbook.close()
    print("\n\n\n\nDone!")

    return f'{corpus}_{sheet_name}2.0.xlsx'


corpus_list = [
        '#Wikibooks (2020)% Intelligenza artificiale',
        '#Mura, Roberto (2019)% Osservare il cielo',
        '#Wikibooks (2008)% Poesie (Palazzeschi)',
        '#Mencarelli, Stefano (2010)% Storia delle Forze armate tedesche dal 1945']


sheet_name_pos = "positiv - Auswahl"
sheet_name_neg = "negativ - Auswahl"
target_file_list_pos = []
target_file_list_neg = []

for corpus in corpus_list:
    pos = print_moral_sentences(f"{corpus}.txt", sheet_name_pos)
    target_file_list_pos.append(to_excel_bold(pos, corpus, sheet_name_pos))

    neg = print_moral_sentences(f"{corpus}.txt", sheet_name_neg)
    target_file_list_neg.append(to_excel_bold(neg, corpus, sheet_name_neg))

pos_dict = {'pos': target_file_list_pos}
neg_dict = {'neg': target_file_list_neg}
merge_excel(pos_dict, 'pos')
merge_excel(neg_dict, 'neg')
