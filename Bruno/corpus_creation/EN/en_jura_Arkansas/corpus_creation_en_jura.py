import os
from collections import Counter
import pprint as pp
import pandas as pd
import nltk
from nltk.tokenize import word_tokenize, sent_tokenize
import xlsxwriter


def clean_sentence(sentence):
    sentence = sentence.replace("<p> ", "")
    sentence = sentence.replace("<h> ", "")
    sentence = sentence.replace(' , "', ',"')
    sentence = sentence.replace(" .", ".")
    sentence = sentence.replace(" ? ", "? ")
    sentence = sentence.replace(" ! ", "! ")
    sentence = sentence.replace(" n't", "n't")
    sentence = sentence.replace(" '", "'")
    sentence = sentence.replace("\\", "")
    sentence = sentence.replace(" : ", ": ")
    sentence = sentence.replace(" ; ", "; ")
    sentence = sentence.replace(' , ', ', ')
    sentence = sentence.replace("( ", "(")
    sentence = sentence.replace(" )", ")")
    return sentence


def print_moral_sentences(corpus_file_name, sheet_name):

    morallist = pd.read_excel(
        "Morallexikon Englisch final 3.0.xlsx",
        sheet_name,
        header=None
    )

    # Sometimes you have to change the encoding type (utf-8, utf-16, ...)
    with open(corpus_file_name, 'r', encoding='utf-8') as f:
        file_contents = f.read()

    morallexikon = morallist[0].tolist()
    sentence_list = []

    transcripts = file_contents.split("###")
    while "" in transcripts:
        transcripts.remove("")

    counter = 0
    for transcript in transcripts:
        lines = transcript.split("\n")
        while "" in lines:
            lines.remove("")

        metadata = lines[0]

        for line in lines:
            counter += 1
            if counter >= 10000:
                break

            else:
                paragraph_sentences = sent_tokenize(line)
                paragraph_lowered_sentences = [x.lower() for x in paragraph_sentences]

                for i, sentence in enumerate(paragraph_lowered_sentences):
                    sentence_words = word_tokenize(sentence)


                    for word in sentence_words:
                        if word in morallexikon:

                            precontext = ""
                            postcontext = ""
                            if i > 2:
                                precontext = paragraph_sentences[i - 2] + " " + paragraph_sentences[i - 1]
                            elif i > 0:
                                precontext = paragraph_sentences[i - 1]
                            if i + 2 < len(paragraph_sentences):
                                postcontext = paragraph_sentences[i + 1] + " " + paragraph_sentences[i + 2]
                            elif i + 1 < len(paragraph_sentences):
                                postcontext = paragraph_sentences[i + 1]

                            chunk = [
                                word,
                                precontext,
                                paragraph_sentences[i],
                                postcontext,
                                metadata,
                            ]

                            sentence_list.append(chunk)
                            print(counter)

                            break

    return sentence_list


def to_excel_bold(data, corpus, sheet_name):

    workbook = xlsxwriter.Workbook(f'{corpus}_{sheet_name}2.0.xlsx')
    worksheet = workbook.add_worksheet()

    row = 0
    for element in data:
        word = element[0]
        list_sentence = element[2].split(word)

        edited_sentence = ""
        if list_sentence[0] != "" and len(list_sentence) >= 2:
            #print(list_sentence)
            edited_sentence = ""
            for i in range(len(list_sentence) - 1):
                edited_sentence = list_sentence[i] + "###" + f"{word}" + "###" + list_sentence[i+1]
                edited_sentence.capitalize()
        else:
            print(list_sentence)
            word = word.capitalize()
            list_sentence = element[2].split(word)
            if len(list_sentence) == 2:
                edited_sentence = "###" + f"{word}" + "###" + list_sentence[1]
        
        worksheet.write(row, 0, element[4] + f", word: {word}")
        row += 1

        try:
            while element[1][0] == " ":
                element[1] = element[1][1:]
                print(element[1])
        except IndexError:
            print("")

        if len(element[1]) > 0:
            worksheet.write(row, 0,
                element[1]
                + " "
                + edited_sentence
                + " "
                + element[3]
            )

        else:
            worksheet.write(row, 0,
                edited_sentence
                + " "
                + element[3]
            )

        row += 1

    workbook.close()
    print("\n\n\n\nDone!")

    return None


corpus = "DATA_Arkansas"
sheet_name = "Positive Selection"

test = print_moral_sentences(f"{corpus}.txt", sheet_name)


to_excel_bold(test, corpus, sheet_name)
