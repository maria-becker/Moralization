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
        string = string.replace('\n', ' ')
    while '  ' in string:
        string = string.replace('  ', ' ')
    if string[0] == " ":
        string = string[1:]

    corpus_string = corpus_string + string
    return corpus_string


def extract_sentences_to_txt(path_to_folder):
    print('Extracting ...')

    corpus_string = ''

    for file in os.listdir(os.fsencode(path_to_folder)):
        file_dec = os.fsdecode(file)
        path_to_xml = os.path.join(path_to_folder, file_dec)

        if file_dec.endswith('.xml') and not file_dec.endswith('(2).xml'):
            print(path_to_xml)
            tree = ET.parse(path_to_xml)
            root = tree.getroot()

            description = ''
            for iterator in root.iter('{http://www.tei-c.org/ns/1.0}setting'):
                for desc_text in iterator.itertext():
                    description = description + desc_text
                while '\n' in description:
                    description = description.replace('\n', ' ')
                while '  ' in description:
                    description = description.replace('  ', ' ')
                while description[0] == ' ':
                    description = description[1:]
                description = description.replace('TEI-CMC version of ', '')
                print(description)

            try:
                for post in root.iter('{http://www.tei-c.org/ns/1.0}u'):
                    corpus_string = corpus_string + '\n\n###\n\n' + \
                        description + '— ' + str(post.attrib) + '\n'
                    for text in post.itertext():
                        corpus_string = add_string(
                            corpus_string,
                            text)

            except IndexError:
                print('error')

    corpus_string = corpus_string.replace('###', '', 1)

    with codecs.open("French_Parliament.txt", 'w', encoding="utf-8") as f:
        f.write(corpus_string)

    return None

##################################################
##################################################

path_to_Parsable_XMLs = r'C:\Users\Arbeit\Desktop\Arbeit\Moralisierungen\Teil 9 Französisch\Coli\French Parliament\FR XML Files'

#######################################

extract_sentences_to_txt(path_to_Parsable_XMLs)
