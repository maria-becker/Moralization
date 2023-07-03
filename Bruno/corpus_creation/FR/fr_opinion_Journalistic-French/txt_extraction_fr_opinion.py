import os
import shutil
import pandas as pd
import pprint as pp
import re
import nltk
import codecs


def add_string(corpus_string, string):

    if string is None:
        return corpus_string

    while '\n' in string:
        string = string.replace('\n', '')

    corpus_string += (string)
    return corpus_string


def extract_sentences_to_txt(path_to_folder):
    print('Extracting ...')

    corpus_string = ''

    #counter = 0
    category_dict = {'interview': 0, 'conversation': 0}

    for paper in os.listdir(os.fsencode(path_to_folder)):
        paper_dec = os.fsdecode(paper)
        path_to_paper = os.path.join(path_to_folder, paper_dec)
        print(path_to_paper)

        for year in os.listdir(os.fsencode(path_to_paper)):
            year_dec = os.fsdecode(year)
            path_to_year = os.path.join(path_to_paper, year_dec)
            print(path_to_year)

            for file in os.listdir(os.fsencode(path_to_year)):
                file_dec = os.fsdecode(file)
                path_to_txt = os.path.join(path_to_year, file_dec)

                #counter += 1
                #if counter > 100:
                #    counter = 0
                #    break

                if file_dec.endswith('.txt'):
                    with open(path_to_txt, encoding='latin') as f:
                        file = f.read()

                        lines = file.split('\n')
                        for key in category_dict.keys():
                            for line in lines[0:4]:
                                if key in line.lower():

                                    print(key)
                                    category_dict[key] += 1

                                    try:
                                        corpus_string += (
                                            '\n\n###\n\n'
                                            + paper_dec
                                            + ", "
                                            + year_dec
                                            + ": "
                                            + file
                                        )
                                    except IndexError:
                                        print('error')

    print(category_dict)

    corpus_string = corpus_string.replace('###', '', 1)

    while '  ' in corpus_string:
        corpus_string = corpus_string.replace('  ', ' ')

    with codecs.open("Interview_Articles.txt", 'w', encoding="utf-8") as f:
        f.write(corpus_string)

    return None

##################################################
##################################################

path_to_Parsable_txt = r'C:\Users\Arbeit\Desktop\Arbeit\Moralisierungen\Teil 9 Französisch\Coli\Journalistic French\ota_20.500.12024_2491\2491\Plain text'

#######################################

extract_sentences_to_txt(path_to_Parsable_txt)
