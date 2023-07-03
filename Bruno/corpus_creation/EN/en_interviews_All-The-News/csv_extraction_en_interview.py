import os
from collections import Counter
import pprint as pp
import pandas as pd
import nltk
from nltk.tokenize import word_tokenize, sent_tokenize
import xlsxwriter
import csv
import pandas
import sys


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
            article_string = ""
            try:
                article_string = "\n" + str(row[0]) + "," + str(row[5]) + "," + str(row[7]) + "," + str(row[9]) + "\n" + clean_text(row[6]) + "\n\n"

            except (ValueError, UnicodeDecodeError):
                print("error!")

            if "interview with" in str(row[5]).lower():
                if str(row[6]).count("?") > 4:
                    text_string = text_string + article_string
                    
                    counter += 1
                    print(str(row[5]))
                    if counter == 1000:
                        break

        with open(f"{path_to_source}.txt", "w", encoding="utf-8") as f:
            f.write(text_string)

    return None


maxInt = sys.maxsize
while True:
    # decrease the maxInt value by factor 10 
    # as long as the OverflowError occurs.

    try:
        csv.field_size_limit(maxInt)
        break
    except OverflowError:
        maxInt = int(maxInt/10)

path_to_source = "all-the-news-2-1.csv"
convert_to_text(path_to_source)
