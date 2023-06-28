import regex as re

txt_dict = {
    'Bibliografia_Umbra_1_Reale_Curto_djvu':
        '#Reale, Luigi M. (2019)% Francesco Curto. Bibliografia ragionata 1968-2018',
    'Pillole-di-diritto-per-creativi-e-musicisti-Aliprandi':
        '#Aliprandi, Simone (2014)% Pillole di diritto per creativi e musicisti',
    'reddito-di-base-e-una-cosa-seria':
        '#Romano, Angelo e Zitelli, Andrea (2018)% Il reddito di base è una cosa seria',
    'Software_licencing':
        '#Aliprandi, Simone (2020)% Software licensing & data governance',
    'Un_ludista':
        '#Anonym (2020)% Un luddista si dondolava sopra un filo di ragnatela. Riflessioni su open source, creative commons e sul capitalismo della sorveglianza'}

for filename in txt_dict:
    with open(f'{filename}.txt', 'r', encoding='utf-8', errors='ignore') as orig_file:
        book_string = orig_file.read()

    book_string = re.sub('\n+( )*[0-9]+( )*\n+', ' ', book_string)
    book_string = book_string.replace('\n\n', '###')
    book_string = book_string.replace('\n', ' ')

    while '  ' in book_string:
        book_string = book_string.replace('  ', ' ')

    book_string = book_string.replace('###', '\n\n###\n\n')

    body_list = book_string.split('###')
    new_body_list = []
    for body in body_list:
        x = re.findall('[\.?!:"] ', body, flags=re.MULTILINE)
        if x:
            print('YES!!')
            print(x)
            new_body_list.append(body)
        else:
            print(body)
            print('#')

    new_book_string = ''
    for body in new_body_list:
        new_book_string += body
    new_book_string = new_book_string.replace('\n\n\n\n', ' ')
    new_book_string = new_book_string.replace('- ', '')
    new_book_string = new_book_string.replace('¬ ', '')

    with open(f'{txt_dict[filename]}.txt', 'w', encoding='utf-8') as target_file:
        target_file.write(str(new_book_string))
