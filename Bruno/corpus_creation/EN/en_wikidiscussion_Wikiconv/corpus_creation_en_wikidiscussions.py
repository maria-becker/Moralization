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

    comments = file_contents.split("###\n\n")
    while "" in comments:
        comments.remove("")



    for comment in comments:

        lines = comment.split("\n")
        metadata = [lines[0], lines[1], lines[2]]

        for line in lines:
            paragraph_sentences = sent_tokenize(line)

            paragraph_lowered_sentences = [x.lower() for x in paragraph_sentences]

            for i, sentence in enumerate(paragraph_lowered_sentences):
                sentence_words = word_tokenize(sentence)
                orig_sentence_words = word_tokenize(paragraph_sentences[i])

                if len(sentence_words) != len(orig_sentence_words):
                    print("ERROR!")

                for loc, word in enumerate(sentence_words):
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

                        metadata_string = metadata[0] + ", " + metadata[1] + ", " + metadata[2]

                        word = orig_sentence_words[loc]

                        chunk = [
                            word,
                            precontext,
                            paragraph_sentences[i],
                            postcontext,
                            metadata_string,
                        ]

                        sentence_list.append(chunk)

                        break

    return sentence_list


def to_excel_bold(data, corpus, sheet_name):

    workbook = xlsxwriter.Workbook(f'{corpus}_{sheet_name}_2023.xlsx')
    worksheet = workbook.add_worksheet()

    row = 0
    for element in data:
        word = element[0]

        edited_sentence = element[2]

        edited_sentence = edited_sentence.replace(word, f"###{word}###")
        if "'''###" in edited_sentence:
            print(edited_sentence)
            continue

        worksheet.write(row, 0, element[4] + f", word: {word}")
        row += 1

        try:
            while element[1][0] == " ":
                element[1] = element[1][1:]
        except IndexError:
            val = 1

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


corpus = "Wikipedia_discussions"
sheet_name1 = "Positive Selection"
#sheet_name2 = "Negative Selection"

test1 = print_moral_sentences(f"{corpus}.txt", sheet_name1)
#test2 = print_moral_sentences(f"{corpus}.txt", sheet_name2)

to_excel_bold(test1, corpus, sheet_name1)
#to_excel_bold(test2, corpus, sheet_name2)
