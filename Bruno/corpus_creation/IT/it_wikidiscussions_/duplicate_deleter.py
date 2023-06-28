with open('article_list.txt', 'r', encoding='utf-8') as f:
    article_list = f.read().splitlines()
print(article_list)

article_list = list(dict.fromkeys(article_list))
print(article_list)

string = ''
for article in article_list:
    string += f'{article}\n'

with open('article_list_clean.txt', 'w', encoding='utf-8') as f:
    f.write(string)
