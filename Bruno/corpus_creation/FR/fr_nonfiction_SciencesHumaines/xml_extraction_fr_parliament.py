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
            iterator = root.iter('{http://www.tei-c.org/ns/1.0}title')
            description = next(iterator).text

            for date in root.iter('{http://www.tei-c.org/ns/1.0}date'):
                description += (', Date: ' + date.attrib['when'])
                while '\n' in description:
                    description = description.replace('\n', ' ')
                while '  ' in description:
                    description = description.replace('  ', ' ')
                while description[0] == ' ':
                    description = description[1:]

                print(description)
                break

            try:
                for speech in root.iter('{http://www.tei-c.org/ns/1.0}text'):
                    corpus_string = corpus_string + '\n\n###\n\n' + \
                        description + '\n'
                    for post in speech.iter('{http://www.tei-c.org/ns/1.0}p'):
                        for text in post.itertext():
                            corpus_string += text.replace('\n', '')

            except IndexError:
                print('error')

    corpus_string = corpus_string.replace('###', '', 1)

    while '\t' in corpus_string:
        corpus_string = corpus_string.replace('\t', ' ')
    while '  ' in corpus_string:
        corpus_string = corpus_string.replace('  ', ' ')

    with codecs.open("Articles.txt", 'w', encoding="utf-8") as f:
        f.write(corpus_string)

    return None

##################################################
##################################################

path_to_Parsable_XMLs = r'C:\Users\Arbeit\Desktop\Arbeit\Moralisierungen\Teil 9 Französisch\Coli\scienceshumaines\files\articles'

#######################################

extract_sentences_to_txt(path_to_Parsable_XMLs)
