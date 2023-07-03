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

    text_dic = {
        "Abernathy": "Abernathy: A Stitch in Time",
        "Berk": "Berk: Awakening Children’s Minds: How Parents and Teachers Can Make a Difference",
        "Fletcher": "Fletcher: Our Secret Constitution : How Lincoln Redefined American Democracy",
        "Kauffman": "Kauffman: Investigations",
        "Rybczinski": "Rybczinski: The Look of Architecture",
        "Castro": "Castro: Chicano Folklore"
    }

    author_list = [
        "Abernathy",
        "Berk",
        "Fletcher",
        "Kauffman",
        "Rybczinski",
        "Castro"
    ]

    for file in os.listdir(os.fsencode(parsable_txt_dir)):
        file_dec = os.fsdecode(file)
        path_to_single_txt = os.path.join(parsable_txt_dir, file_dec)

        print('File:', file_dec)

        if file_dec.endswith('.txt'):
            print(path_to_single_txt)
            with open(path_to_single_txt, "r+", encoding="utf-8") as temp_file:
                data = temp_file.read()
                data = data.replace("\n", " ")
                #data = re.sub(r"\.[0-9]+", ".", data) # this is problematic
                #data = re.sub(r'”[0-9]+', "”", data) # this is problematic
                data = data.replace("    ", "")

                for author in author_list:
                    if author in file_dec:
                        chapter = file_dec.replace(".txt", "")
                        chapter = chapter.replace(author, "")
                        corpus_string = corpus_string + f"###\n{text_dic[author]}, {chapter}\n" + data + "\n\n\n"

    with codecs.open("ONAC_NonFiction.txt", 'w', encoding="utf-8") as f:
        f.write(corpus_string)

    return None

##################################################
##################################################

path_to_Parsable_XMLs = r'C:\Users\Arbeit\Desktop\Arbeit\Moralisierungen\Teil 6 Corpus\Coli\Sachbücher\ONAC\MAIN'

#######################################

extract_sentences_to_txt(path_to_Parsable_XMLs)
