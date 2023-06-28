import ast

def law_news_extraction(filename):
    with open(filename, encoding='utf-8') as f:
        file_contents = [x.strip().split('\t') for x in f]
    law_news = [x for x in file_contents if ('«' or '»') in x[4]]
    print(law_news)
    print(len(law_news))

    return law_news


joined_list = (
    law_news_extraction('Ita_Newspapers_2012.txt')
    + law_news_extraction('Ita_Newspapers_2011.txt'))

with open('interviews_it.txt', 'w', encoding='utf-8') as f:
    f.write(str(joined_list))
