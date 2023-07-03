import os
import shutil
import pandas as pd
import pprint as pp
import re
import nltk
import codecs
import xml.etree.ElementTree as ET


def iterate_folders(folder_path):
    folder_contents = ''
    for folder in os.listdir(os.fsencode(path_to_data)):
        folder_dec = os.fsdecode(folder)
        path_to_folder = os.path.join(path_to_data, folder_dec)


def merge_files(file_list, output_filename):
    filenames = file_list
    with open(output_filename, 'w') as outfile:
        for fname in filenames:
            with open(fname, errors="ignore") as infile:
                for line in infile:
                    outfile.write(line)


def test_for_article(tree_item):
    count = 0
    try:
        if tree_item.attrib == {'type': 'article'}:
            for sub in tree_item.iter():
                if sub.attrib == {'type': 'accroche'} or sub.attrib == {'type': 'legende'}:
                    return False
            test = str(tree_item.iter('{http://www.tei-c.org/ns/1.0}head'))
            if re.match(r'<_elementtree._element_iterator object at', test):
                return True
    except TypeError:
        return False
    return False


def extract_sentences_to_txt(path):
    print(path)

    counter = 0
    txt_nr = 0
    corpus_string = ''

    for dirpath, dirnames, filenames in os.walk(path):
        for filename in [f for f in filenames if f.endswith(".xml")]:
            path_to_xml = os.path.join(dirpath, filename)

            if path_to_xml.endswith('.xml'):
                if counter > 2000:
                    write_to_txt(corpus_string, txt_nr)
                    corpus_string = ''
                    txt_nr += 1
                    print(txt_nr - 1)
                    counter = 0
                    if txt_nr > 10:
                        return None
                tree = ET.parse(path_to_xml)
                root = tree.getroot()

                edition = ''
                for desc in root.iter('{http://www.tei-c.org/ns/1.0}title'):
                    for desc in desc.itertext():
                        edition += desc
                    break

                try:
                    for speech in root.iter('{http://www.tei-c.org/ns/1.0}div'):
                        description = (edition + ", ")
                        if test_for_article(speech):
                            for head in speech.iter('{http://www.tei-c.org/ns/1.0}head'):
                                for part in head.itertext():
                                    description += part
                                description = description.replace('\n', ' ')
                                description= description.replace('\t', ' ')
                                while '  ' in description:
                                    description = description.replace('  ', ' ')
                                break

                            post_string = ''
                            for post in speech.iter('{http://www.tei-c.org/ns/1.0}p'):
                                for text in post.itertext():
                                    post_string += text.replace('\n', '')

                            if "L'Est Républicain" not in post_string:
                                if "Secrétariat de mairie" not in post_string:
                                    if "tél." not in post_string:
                                        if '.' in post_string:
                                            corpus_string = corpus_string + '\n\n###\n\n' + \
                                                description + '\n'
                                            corpus_string += post_string.replace('\n', ' ')

                            counter += 1

                except IndexError:
                    print('error')

    return None


def write_to_txt(corpus_string, number):
    corpus_string = corpus_string.replace('###', '', 1)

    while '\t' in corpus_string:
        corpus_string = corpus_string.replace('\t', ' ')
    while '  ' in corpus_string:
        corpus_string = corpus_string.replace('  ', ' ')

    with codecs.open(f"Articles{str(number)}.txt", 'a', encoding="utf-8") as f:
        f.write(corpus_string)

    return None

##################################################
##################################################

path_to_Parsable_XMLs_list = [
    r"C:\Users\Arbeit\Desktop\Arbeit\Moralisierungen\Teil 9 Französisch\Coli\L'est Republican\est_republicain\est_republicain\4\Annee1999",
    r"C:\Users\Arbeit\Desktop\Arbeit\Moralisierungen\Teil 9 Französisch\Coli\L'est Republican\est_republicain\est_republicain\4\Annee2002",
    r"C:\Users\Arbeit\Desktop\Arbeit\Moralisierungen\Teil 9 Französisch\Coli\L'est Republican\est_republicain\est_republicain\4\Annee2003",
    r"C:\Users\Arbeit\Desktop\Arbeit\Moralisierungen\Teil 9 Französisch\Coli\L'est Republican\est_republicain\est_republicain\4\Annee2006",
    r"C:\Users\Arbeit\Desktop\Arbeit\Moralisierungen\Teil 9 Französisch\Coli\L'est Republican\est_republicain\est_republicain\4\Annee2007",
    r"C:\Users\Arbeit\Desktop\Arbeit\Moralisierungen\Teil 9 Französisch\Coli\L'est Republican\est_republicain\est_republicain\4\Annee2008",
    r"C:\Users\Arbeit\Desktop\Arbeit\Moralisierungen\Teil 9 Französisch\Coli\L'est Republican\est_republicain\est_republicain\4\Annee2009",
    r"C:\Users\Arbeit\Desktop\Arbeit\Moralisierungen\Teil 9 Französisch\Coli\L'est Republican\est_republicain\est_republicain\4\Annee2010",
    r"C:\Users\Arbeit\Desktop\Arbeit\Moralisierungen\Teil 9 Französisch\Coli\L'est Republican\est_republicain\est_republicain\4\Annee2011"]

file_list = [
    r"Articles0.txt",
    r"Articles1.txt",
    r"Articles3.txt",
    r"Articles4.txt",
    r"Articles5.txt",
    r"Articles6.txt",
    r"Articles7.txt",
    r"Articles8.txt",
    r"Articles9.txt",
    r"Articles10.txt"]

#######################################

for path in path_to_Parsable_XMLs_list:
    extract_sentences_to_txt(path)

merge_files(file_list, "Interviews_fr.txt")
