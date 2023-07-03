import os
from collections import Counter
import pprint as pp
import pandas as pd
import nltk
from nltk.tokenize import word_tokenize, sent_tokenize
import xlsxwriter
import re
from nltk.stem import WordNetLemmatizer

lemmatizer = WordNetLemmatizer()


def clean_sentence(sentence):
    sentence = sentence.replace("â", "'")
    sentence = sentence.replace("", "")
    sentence = sentence.replace("", "")
    sentence = sentence.replace("", "")
    sentence = sentence.replace(" ", "")
    sentence = sentence.replace("Â", " ")
    sentence = sentence.replace("", "")
    sentence = sentence.replace("", "")
    sentence = sentence.replace("", "")
    sentence = sentence.replace("", "")
    sentence = sentence.replace("", "")
    sentence = sentence.replace("", "")
    sentence = sentence.replace("", "")
    sentence = sentence.replace("\\'", "'")

    return sentence


def print_moral_sentences(corpus_file_name, sheet_name):

    morallist = pd.read_excel(
        "Morallexikon FR_final_überarbeitet.xlsx",
        sheet_name,
        header=None
    )

    # Sometimes you have to change the encoding type (utf-8, utf-16, ...)
    with open(corpus_file_name, 'r', encoding='utf-8') as f:
        file_contents = f.read()

    morallexikon = morallist[0].tolist()
    sentence_list = []

    transcripts = file_contents.split("###")
    print(len(transcripts))
    while '' in transcripts:
        transcripts.remove('')

#    counter = 0

    for transcript in transcripts:
        transcript_lines = transcript.split("\n")
        copyright = " "
        for line in transcript_lines:
            if line.startswith("Copyright"):
                copyright = line
                break
            #except (AttributeError, TypeError):
             #   continue

        try:
            metadata = transcript_lines[3] + "; " + \
                transcript_lines[4] + "; " + \
                transcript_lines[5] + \
                f" ({copyright})"
        except IndexError:
            print(transcript)

        if transcript.count("?") > 3:

            for line in transcript_lines[6:]:
                paragraph_sentences = sent_tokenize(line)

                for paragraph in paragraph_sentences:
                    if paragraph.startswith("Copyright") or (" Copyright"):
                        paragraph_sentences.remove(paragraph)

                paragraph_sentences = sent_tokenize(" ".join(paragraph_sentences))
                paragraph_lowered_sentences = [
                    x.lower() for x in paragraph_sentences]
        #            counter += 1
        #            if counter > 30:
        #                break

                paragraph_lowered_sentences = [
                    x.lower() for x in paragraph_sentences]
        #            counter += 1
        #            if counter > 30:
        #                break

                for i, sentence in enumerate(paragraph_lowered_sentences):
                    sentence_words = word_tokenize(sentence)

                    for word in sentence_words:
                        if lemmatizer.lemmatize(word) in morallexikon:

                            precontext = ""
                            postcontext = ""
                            if i > 2:
                                precontext = paragraph_sentences[i - 2] + " " + \
                                    paragraph_sentences[i - 1]
                            elif i > 0:
                                precontext = paragraph_sentences[i - 1]
                            if i + 2 < len(paragraph_sentences):
                                postcontext = paragraph_sentences[i + 1] + " " + \
                                    paragraph_sentences[i + 2]
                            elif i + 1 < len(paragraph_sentences):
                                postcontext = paragraph_sentences[i + 1]

                            chunk = [
                                word,
                                precontext,
                                paragraph_sentences[i],
                                postcontext,
                                metadata,
                            ]

        #                        print(chunk)

        #                        for i,thing in enumerate(chunk):
        #                            chunk[i] = clean_sentence(thing)

        #                        print(chunk)

                            sentence_list.append(chunk)
        #                        print(chunk)

                            break

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
        if (element[1] or element[3]) != "":
            print(element[1], element[3])
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

            if len(element[1]) > 0:
                if element[1][0] == ' ':
                    element[1] = element[1][1:]
                worksheet.write(row, 0,
                    element[1]
                    + " "
                    + edited_sentence
                    + " "
                    + element[3]
                )

            else:
                #print(edited_sentence)
                if edited_sentence != '':
                    if edited_sentence[0] == ' ':
                        edited_sentence = edited_sentence[1:]
                    worksheet.write(row, 0,
                        edited_sentence
                        + " "
                        + element[3]
                    )

            row += 1

    workbook.close()
    print("\n\n\n\nDone!")

    return None


corpus = "French_Interviews"
sheet_name_pos = "Positive Selection"
sheet_name_neg = "Negative Selection"

pos = print_moral_sentences(f"{corpus}.txt", sheet_name_pos)
to_excel_bold(pos, corpus, sheet_name_pos)

neg = print_moral_sentences(f"{corpus}.txt", sheet_name_neg)
to_excel_bold(neg, corpus, sheet_name_neg)
