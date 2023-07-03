import os
from collections import Counter
import pprint as pp
import pandas as pd
import nltk
from nltk.tokenize import word_tokenize, sent_tokenize
import xlsxwriter
import csv
import pandas


def clean_text(text):
    text = text.replace("</p>", " ")
    text = text.replace("<p>", " ")
    text = text.replace("\n", " ")
    text = text.replace("  ", " ")
    return text


def convert_to_text(path_to_source):
    with open(path_to_source, encoding="utf-8") as csv_file:
        data = csv.reader(csv_file, delimiter=',')

        text_string = ""

        counter = 0
        for row in data:
            try:
                text_string = text_string + "\n" + str(row[0:4]) + "\n" + clean_text(row[7]) + "\n\n"
                counter += 1
                print(counter)
                # if counter == 30:
                #    break

            except (ValueError, UnicodeDecodeError):
                print("error!")


        with open(f"{path_to_source}.txt", "w") as f:
            f.write(text_string)

    return None


path_to_source = "gnm_articles.csv"
convert_to_text(path_to_source)
