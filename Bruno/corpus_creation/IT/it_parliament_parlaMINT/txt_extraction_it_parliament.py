import os
import shutil
import pandas as pd
import pprint as pp
import re
import nltk
import codecs
import xml.etree.ElementTree as ET


def extract_sentences_to_txt(path_list):
    corpus_string = ''

    for path in path_list:
        print(path)
        for dirpath, dirnames, filenames in os.walk(path):
            counter = 0
            for filename in [f for f in filenames if f.endswith(".txt")]:
                path_to_txt = os.path.join(dirpath, filename)
                path_to_tsv = path_to_txt.replace('.txt', '-meta.tsv')

                with open(path_to_txt, encoding='utf-8') as f:
                    file_string = f.read()

                with open(path_to_tsv) as f:
                    meta = [x.strip().split('\t') for x in f]

                for array in meta:
                    file_string = file_string.replace(
                        str(array[0]) + '\t',
                        str(array[0]) + ': '
                        + str(array[1]) + ', '
                        + 'Speaker: ' + str(array[16]) + '\t')

                corpus_string += file_string
                counter += 1
                if counter > 30:
                    break

    # corpus_string = corpus_string.replace('ParlaMint-', '\nParlaMint-')
    corpus_string = corpus_string.replace('\n', '\n\n')
    corpus_string = re.sub(r'\[\[.*\]\]', '', corpus_string)
    while '  ' in corpus_string:
        corpus_string = corpus_string.replace('  ', ' ')
    with open("Parlament_discussions_IT.txt", 'w', encoding="utf-8") as f:
        f.write(corpus_string)

    return None


##################################################
##################################################

path_to_Parsable_TXTs_list = [
    r"C:\Users\Arbeit\Desktop\Arbeit\Moralisierungen\Teil 8 Korpus Italienisch\Coli\parlaMINT\extracted_files\ParlaMint-IT-txt\2013",
    r"C:\Users\Arbeit\Desktop\Arbeit\Moralisierungen\Teil 8 Korpus Italienisch\Coli\parlaMINT\extracted_files\ParlaMint-IT-txt\2014",
    r"C:\Users\Arbeit\Desktop\Arbeit\Moralisierungen\Teil 8 Korpus Italienisch\Coli\parlaMINT\extracted_files\ParlaMint-IT-txt\2015",
    r"C:\Users\Arbeit\Desktop\Arbeit\Moralisierungen\Teil 8 Korpus Italienisch\Coli\parlaMINT\extracted_files\ParlaMint-IT-txt\2016",
    r"C:\Users\Arbeit\Desktop\Arbeit\Moralisierungen\Teil 8 Korpus Italienisch\Coli\parlaMINT\extracted_files\ParlaMint-IT-txt\2017",
    r"C:\Users\Arbeit\Desktop\Arbeit\Moralisierungen\Teil 8 Korpus Italienisch\Coli\parlaMINT\extracted_files\ParlaMint-IT-txt\2018",
    r"C:\Users\Arbeit\Desktop\Arbeit\Moralisierungen\Teil 8 Korpus Italienisch\Coli\parlaMINT\extracted_files\ParlaMint-IT-txt\2019",
    r"C:\Users\Arbeit\Desktop\Arbeit\Moralisierungen\Teil 8 Korpus Italienisch\Coli\parlaMINT\extracted_files\ParlaMint-IT-txt\2020"]

#######################################

extract_sentences_to_txt(path_to_Parsable_TXTs_list)
