import os
import shutil
import pandas as pd
import pprint as pp
import re
import nltk
import codecs
import xml.etree.ElementTree as ET


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

    counter = 0
    description_list = []
    for area in os.listdir(os.fsencode(path_to_folder)):
        area_dec = os.fsdecode(area)
        path_to_area = os.path.join(path_to_folder, area_dec)

        for category in os.listdir(os.fsencode(path_to_area)):
            category_dec = os.fsdecode(category)
            if category_dec.endswith('reference_indexation'):
                path_to_category = os.path.join(path_to_area, category_dec)

                for file in os.listdir(os.fsencode(path_to_category)):
                    file_dec = os.fsdecode(file)
                    path_to_xml = os.path.join(path_to_category, file_dec)

                    counter += 1
                    if counter > 100:
                        counter = 0
                        break

                    if file_dec.endswith('.xml'):
                        print(path_to_xml)
                        tree = ET.parse(path_to_xml)
                        root = tree.getroot()

                        description = ''
                        for iterator in root.iter(
                            '{http://www.tei-c.org/ns/1.0}title'
                        ):
                            for desc_text in iterator.itertext():
                                description = description + desc_text
                            while '\n' in description:
                                description = description.replace('\n', ' ')
                            while '  ' in description:
                                description = description.replace('  ', ' ')
                            while description[0] == ' ':
                                description = description[1:]
                            description += (', Domaine: ' + area_dec)

                            print(description)
                            break

                        if description not in description_list:
                            try:
                                corpus_string += ('\n\n###\n\n'
                                    + description + '\n'
                                )
                                description_list.append(description)
                                
                                for word in root.iter(
                                    '{http://www.tei-c.org/ns/1.0}body'
                                    ):
                                    for text in word.itertext():
                                        corpus_string += (' ' + text.replace('\n', ''))

                            except IndexError:
                                print('error')

    corpus_string = corpus_string.replace('###', '', 1)

    while '  ' in corpus_string:
        corpus_string = corpus_string.replace('  ', ' ')

    with codecs.open("Research_Articles.txt", 'w', encoding="utf-8") as f:
        f.write(corpus_string)

    return None

##################################################
##################################################

path_to_Parsable_XMLs = r'C:\Users\Arbeit\Desktop\Arbeit\Moralisierungen\Teil 9 Französisch\Coli\termith\termith\3\donnees'

#######################################

extract_sentences_to_txt(path_to_Parsable_XMLs)
