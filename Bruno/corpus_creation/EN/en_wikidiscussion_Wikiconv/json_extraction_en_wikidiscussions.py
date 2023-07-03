import json
import sys


def clean_json(file):
    dictionaries = []
    for line in open(file, encoding="UTF-8"):
        dictionaries.append(json.loads(line))

    print(dictionaries[0].keys())

    corpus_string = ""

    counter = 0
    for dictionary in dictionaries: 
        corpus_string = corpus_string + "ID: " + dictionary["id"] + "\nTitle:" + dictionary["page_title"] + "\nTime:" + dictionary["timestamp"] + "\n" + dictionary["cleaned_content"] + "\n\n###\n"
        counter += 1
        if counter == 10000:
        	break

    with open("Wikipedia_discussions.txt", 'wb') as f:
        f.write(corpus_string.encode("utf-8"))

    print("Done!")

    return None


clean_json("dataset_English_wikiconv_en_20180701_000000000000.json")
