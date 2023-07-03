import json
import codecs


def create_txt(filename):
    data = [json.loads(line) for line in open(filename, 'r', encoding='utf-8')]

    print(data[1].keys())
    corpus_string = ""

    counter = 0
    for dictionary in data:
        try:
            corpus_string = corpus_string + f'###\nID: {dictionary["id"]}, {dictionary["name_abbreviation"]}\n{dictionary["casebody"]["data"]["opinions"][0]["text"]}\n\n'
            counter += 1
            if counter == 50000:
                break

        except IndexError:
            print("Error")

    with codecs.open("ONAC_NonFiction.txt", 'w', encoding="utf-8") as f:
        f.write(corpus_string)

    return None


create_txt("data.jsonl")
