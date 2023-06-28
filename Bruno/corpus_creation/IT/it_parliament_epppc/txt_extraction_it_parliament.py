import os
import shutil
import pandas as pd
import xml.etree.ElementTree as ET
import pprint as pp
import re
import nltk
import codecs

########################################

# TODO: TAZ datei einlesen
# TODO: Moralwörter einlesen
# TODO: Wörter lemmatisieren
# TODO: lemmatisierte Wörter abspeichern
# TODO: Dataframe befüllen
# TODO: Dataframe als .xlsx (Excel-Datei) exportieren 
# TODO: .*woke.* Wörter beachten

#######################################


def extract_sentences_to_txt(parsable_txt_dir):
    print('Extracting ...')

    corpus_string = ""

    counter = 0

    for file in os.listdir(os.fsencode(parsable_txt_dir)):
        file_dec = os.fsdecode(file)
        path_to_single_txt = os.path.join(parsable_txt_dir, file_dec)

        print('File:', file_dec)

        if file_dec.endswith('.txt'):
            print(path_to_single_txt)
            with open(path_to_single_txt, "r+", encoding="utf-8") as temp_file:
                data = temp_file.read()

                # Collect Metadata
                data = re.sub(r'<SPEAKER .+NAME=', 'Speaker: ', data)
                #data = re.sub(r'<u who="#', '\n\n', data)
                #data = re.sub(r'<u who="#', '\n\n', data)
                #data = re.sub(r'<u who="#', '\n\n', data)
                #data = re.sub(r'<u who="#', '\n\n', data)
                #data = re.sub(r'<u who="#', '\n\n', data)
                #data = re.sub(r'<u who="#', '\n\n', data)
                data = re.sub(r'<.+>', '', data)
                data = re.sub(r'>', '', data)
                corpus_string = corpus_string + "### " + file_dec + "\n\n" + data + "\n\n\n"

        counter += 1
        print(counter)
        if counter >= 500:
            break


    with codecs.open("EU_Parlament.txt", 'w', encoding="utf-8") as f:
        f.write(corpus_string)

    return None

##################################################
##################################################

path_to_Parsable_XMLs = r'C:\Users\Arbeit\Desktop\Arbeit\Moralisierungen\Teil 8 Korpus Italienisch\Coli\Parlament (EU)\it'

#######################################

extract_sentences_to_txt(path_to_Parsable_XMLs)
