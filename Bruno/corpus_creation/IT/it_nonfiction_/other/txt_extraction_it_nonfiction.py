import regex as re

txt_dict = {
    'uc1-b4251166-1672731754':
        '#Di Bono, Mario (1990)% Le sfere omocentriche di Giovan Battista Amico nell\'astronomia del Cinquecento'}

for filename in txt_dict:
    with open(f'{filename}.txt', 'r', encoding='utf-8', errors='ignore') as orig_file:
        book_string = orig_file.read()

    book_string = re.sub('\n\n##.*######################\n', ' ', book_string)

    line_list = book_string.split('\n')
    new_line_list = []
    for line in line_list:
        if not line.isupper():
            print(line)
            new_line_list.append(line)

    line_list = new_line_list
    new_line_list = []
    print(line_list)
    for i, line in enumerate(line_list):
        if not line.isdigit():
            print(i)
            new_line_list.append(line)

    print(new_line_list)

    output_string = ' '.join(new_line_list)

    output_string = output_string.replace('', '')
    output_string = output_string.replace('\n', ' ')
    while '  ' in output_string:
        output_string = output_string.replace('  ', ' ')
    output_string = output_string.replace('- ', '')
    output_string = output_string.replace('¬ ', '')


    print(output_string)

    with open(f'{txt_dict[filename]}.txt', 'w', encoding='utf-8') as target_file:
        target_file.write(str(output_string))
