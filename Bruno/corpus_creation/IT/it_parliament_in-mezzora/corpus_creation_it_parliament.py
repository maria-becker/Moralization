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
        "Morallexikon_IT-überarbeitet.xlsx",
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

    moral_library = {}
    counter = 0
    for transcript in transcripts:
        lines = transcript.split("\n")
        while "" in transcripts:
            transcripts.remove("")

        metadata = lines[0]
        metadata = metadata.replace(".txt", "")
        metadata = metadata[1:]
        speaker = ""


        for line in lines:
            counter += 1
            if counter >= 100000:
                break
            if line[0:7] == "Speaker":
                speaker = line
            
            else:
                paragraph_sentences = sent_tokenize(line)
                if len(paragraph_sentences) > 1:
                    paragraph_lowered_sentences = [x.lower() for x in paragraph_sentences]

                    for i, sentence in enumerate(paragraph_lowered_sentences):
                        sentence_words = word_tokenize(sentence)
                        if paragraph_sentences[0] == "Speaker":
                            speaker = sentence[:-1]


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
    print(moral_library)
    return sentence_list


def to_excel_bold(data, corpus, sheet_name):

    workbook = xlsxwriter.Workbook(f'{corpus}_{sheet_name}2.0.xlsx')
    worksheet = workbook.add_worksheet()
    moral_library = {}


    row = 0
    for element in data:
        word = element[0]
        list_sentence = element[2].split(word)

        edited_sentence = ""
        if list_sentence[0] != "" and len(list_sentence) >= 2:
            #print(list_sentence)
            edited_sentence = ""
            for i in range(len(list_sentence) - 1):
                edited_sentence = edited_sentence + list_sentence[i] + "###" + f"{word}" + "###" + list_sentence[i+1]
                edited_sentence.capitalize()
                edited_sentence.replace("  ", " ")
        else:
            #print(list_sentence)
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
            edited_sentence = edited_sentence[1:]

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


corpus = "Speeches"
sheet_name = "negativAuswahl"

test = print_moral_sentences(f"{corpus}.txt", sheet_name)


to_excel_bold(test, corpus, sheet_name)
