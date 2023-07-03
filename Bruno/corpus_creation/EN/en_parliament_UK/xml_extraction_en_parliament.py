import os
import shutil
import pandas as pd
import xml.etree.ElementTree as ET
import pprint as pp
import re
import nltk

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

    for file in os.listdir(os.fsencode(parsable_txt_dir)):
        file_dec = os.fsdecode(file)
        path_to_single_txt = os.path.join(parsable_txt_dir, file_dec)

        print('File:', file_dec)

        if file_dec.endswith('.txt'):
            print(path_to_single_txt)
            with open(path_to_single_txt, "r+") as temp_file:
                data = temp_file.read()
                data = data.replace("\n", "")

                # Collect Metadata
                data = re.sub(r'<orgName>', '\nPlace: ', data)
                data = re.sub(r'<date>', '\nDate: ', data)
                data = re.sub(r'<activity>', '\nEvent: ', data)
                #data = re.sub(r'<u who="#', '\n\n', data)
                #data = re.sub(r'<u who="#', '\n\n', data)
                #data = re.sub(r'<u who="#', '\n\n', data)
                #data = re.sub(r'<u who="#', '\n\n', data)
                #data = re.sub(r'<u who="#', '\n\n', data)
                #data = re.sub(r'<u who="#', '\n\n', data)

                
                data = re.sub("  +", " ", data)
                data = re.sub(r'<u who="#', '\n\n', data)
                data = re.sub("<seg>", "\n", data)
                data = re.sub(r'">', ':', data)
                data = re.sub(r'<.*>', '', data)
                data = re.sub(r' </body> </text></TEI>', '', data)
                data = re.sub(r'\n ', '\n', data)
                data = re.sub(r"hon.", "honourable", data)
                data = re.sub(r"Hon.", "Honourable", data)
                corpus_string = corpus_string + "###\n\n" + data + "\n\n\n"

    with open("UK_Parlament.txt", 'w') as f:
        f.write(corpus_string)

    return None

##################################################
##################################################

path_to_Parsable_XMLs = r'C:\Users\Arbeit\Desktop\Arbeit\Moralisierungen\Teil 6 Corpus\Coli\XML\uk-parl\UK - TEI-XML Files'

#######################################

extract_sentences_to_txt(path_to_Parsable_XMLs)
