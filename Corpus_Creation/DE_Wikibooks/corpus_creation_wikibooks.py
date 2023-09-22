from HanTa import HanoverTagger as ht
import nltk
import xlsxwriter
import json
import nltk.data


def print_moral_sentences(corpus_file_name):

    with open(r"Morallexika\neg-selection-of-selection.txt",
              "r", encoding="utf-8") as f:
        morallexikon = f.read().split()

    with open(corpus_file_name, 'r', encoding='utf-8') as f:
        file_contents = json.load(f)

    tagger = ht.HanoverTagger(f'morphmodel_ger.pgz')

    sentence_list = []

    for paragraph in file_contents:
        paragraph_sentences = nltk.sent_tokenize(paragraph["text"], language="german")

        # # For testing
        # if len(sentence_list) > 20:
        #     break

        for i, sentence in enumerate(paragraph_sentences):
            sentence_words = nltk.word_tokenize(sentence, language="german")
            sentence_tagged = tagger.tag_sent(sentence_words)

            for loc, word in enumerate(sentence_tagged):
                if word[1] in morallexikon:
                    precontext = ""
                    postcontext = ""
                    if i > 2:
                        precontext = (paragraph_sentences[i - 2]
                                      + " "
                                      + paragraph_sentences[i - 1])
                    elif i > 0:
                        precontext = paragraph_sentences[i - 1]
                    if i + 2 < len(paragraph_sentences):
                        postcontext = (paragraph_sentences[i + 1]
                                       + " "
                                       + paragraph_sentences[i + 2])
                    elif i + 1 < len(paragraph_sentences):
                        postcontext = paragraph_sentences[i + 1]

                    chunk = [
                        word[0],
                        precontext,
                        paragraph_sentences[i],
                        postcontext,
                        paragraph["source"]
                    ]

                    sentence_list.append(chunk)
                    print(chunk)
                    break

    return sentence_list


def to_excel_bold(data, corpus, sheet_name):

    workbook = xlsxwriter.Workbook(f'{corpus}_{sheet_name}.xlsx')
    worksheet = workbook.add_worksheet()
    bold = workbook.add_format({'bold': True})

    row = 0
    for element in data:
        word = element[0]

        combined_str = "".join([
            element[4],
            f"; Wort: {word}",
            " ### ",
            element[1],
            " ",
            element[2],
            " ",
            element[3]
            ])

        worksheet.write(row, 0, combined_str)
        row += 1

    workbook.close()
    print("\n\n\n\nDone!")

    return None


corpus = r"wikibooks\wikibooks_dwds.json"
sheet_name = "Negative Selection"

test = print_moral_sentences(corpus)

to_excel_bold(test, corpus, sheet_name)
