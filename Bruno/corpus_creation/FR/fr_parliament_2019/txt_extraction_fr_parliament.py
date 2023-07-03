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

    for file in os.listdir(os.fsencode(path_to_folder)):
        file_dec = os.fsdecode(file)
        path_to_xml = os.path.join(path_to_folder, file_dec)

        if file_dec.endswith('.xml'):
            print(path_to_xml)
            tree = ET.parse(path_to_xml)
            root = tree.getroot()

            description = ''
            for iterator in root.iter('{http://www.tei-c.org/ns/1.0}title'):
                for desc_text in iterator.itertext():
                    description = description + desc_text
                while '\n' in description:
                    description = description.replace('\n', ' ')
                while '  ' in description:
                    description = description.replace('  ', ' ')
                while description[0] == ' ':
                    description = description[1:]
                description = description.replace(
                    ' Fichier étiqueté POS d\'un compte rendu de d', ' D'
                )
                print(description)
                break

            try:
                for speech in root.iter('{http://www.tei-c.org/ns/1.0}sp'):
                    corpus_string = corpus_string + '\n\n###\n\n' + \
                    description + ' — ' + str(speech.attrib) + '\n'
                    for post in speech.iter('{http://www.tei-c.org/ns/1.0}s'):
                        for text in post.itertext():
                            corpus_string += (' ' + text.replace('\n', ''))

            except IndexError:
                print('error')

    corpus_string = corpus_string.replace('###', '', 1)

    while '  ' in corpus_string:
        corpus_string = corpus_string.replace('  ', ' ')

    with codecs.open("French_Parliament.txt", 'w', encoding="utf-8") as f:
        f.write(corpus_string)

    return None

##################################################
##################################################

path_to_Parsable_XMLs = r'C:\Users\Arbeit\Desktop\Arbeit\Moralisierungen\Teil 9 Französisch\Coli\French Parliament 2.0\xml-protocols'

#######################################

extract_sentences_to_txt(path_to_Parsable_XMLs)
