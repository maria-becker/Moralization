import ast

def law_news_extraction(filename):
    with open(filename, encoding='utf-8') as f:
        file_contents = [x.strip().split('\t') for x in f]

    law_news = [x for x in file_contents if x[3] == '5']
    print(law_news)
    print(len(law_news))

    return law_news


joined_list = law_news_extraction("Eng_US_Newspapers.txt")


with open('law_news_ENG.txt', 'w', encoding='utf-8') as f:
    f.write(str(joined_list))
