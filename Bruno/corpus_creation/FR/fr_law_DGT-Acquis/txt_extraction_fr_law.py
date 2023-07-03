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


def extract_sentences_to_txt(path_to_file):
    print('Extracting ...')

    corpus_string = ''

    with open(path_to_file, 'r', encoding = 'utf-8') as file:
        data_string = file.read()

    decision_lib = data_string.split('Arrêt de la Cour')
    for decision in decision_lib:
        if 500 < len(decision) < 50000:
            paragraphs = decision.split('\n')
            text = ''
            for paragraph in paragraphs:
                if re.search('[!?.]$', paragraph) is not None:
                    text += (paragraph.replace('\n', ' ') + ' ')
            if text != '':
                print(f'Arrêt de la Cour {paragraphs[0]}')
                corpus_string += '###\n\nArrêt de la Cour'
                corpus_string = corpus_string + paragraphs[0]
                corpus_string += '\n' + text + '\n\n'


                #print('Arrêt de la Cour' + paragraphs[0])
                #print(text)

    corpus_string = corpus_string.replace('###', '', 1)

    while '\t' in corpus_string:
        corpus_string = corpus_string.replace('\t', ' ')
    while '  ' in corpus_string:
        corpus_string = corpus_string.replace('  ', ' ')

    with codecs.open("Decisions.txt", 'w', encoding="utf-8") as f:
        f.write(corpus_string)

    return None

##################################################
##################################################

path_to_Parsable_XMLs = r'C:\Users\Arbeit\Desktop\Arbeit\Moralisierungen\Teil 9 Französisch\Coli\DFG aqcuis\data.fr.txt\data.fr.txt'

#######################################

extract_sentences_to_txt(path_to_Parsable_XMLs)
