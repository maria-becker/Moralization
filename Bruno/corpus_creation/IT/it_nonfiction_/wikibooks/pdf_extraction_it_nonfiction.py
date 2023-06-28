import PyPDF2
import regex as re


pdf_dict = {
    'Intelligenza_artificiale':
        '#Wikibooks (2020)% Intelligenza artificiale',
    'Osservare_il_cielo':
        '#Mura, Roberto (2019)% Osservare il cielo',
    'Poesie_(Palazzeschi)':
        '#Wikibooks (2008)% Poesie (Palazzeschi)',
    'Storia_delle_Forze_armate_tedesche_dal_1945':
        '#Mencarelli, Stefano (2010)% Storia delle Forze armate tedesche dal 1945'}


for filename in pdf_dict:

    # Create file object variable
    pdffileobj = open(f'{filename}.pdf', 'rb')

    # Create reader variable that will read the pdffileobj
    pdfreader = PyPDF2.PdfReader(pdffileobj)

    # Store the number of pages of this pdf file
    length = len(pdfreader.pages)

    # Loop over all pages and store the text
    text_string = ''
    for n in range(length):
        print(n)
        pageobj = pdfreader.pages[n]
        text = pageobj.extract_text()
        text_string += text + '\n\n### NEW PAGE ###\n\n'

    print(text_string)

    # Modify text string
    text_string = re.sub(
        '([0-9]+\n)*\n\n### NEW PAGE ###\n\n.*\n',
        '',
        text_string,
        flags=re.A)
    text_string = re.sub(
        '\n### NEW PAGE ###\n\n.*\n',
        '',
        text_string,
        flags=re.A)
    mainheader_list = re.findall(
        '\n[0-9]+.{5,40}[^\.!?;:]\n',
        text_string)
    header_list = re.findall(
        '\n[0-9]+\.[0-9]+.*[^\.!?;:]\n',
        text_string)
    subheader_list = re.findall(
        '\n[A-Z].{4,30}[^\.!?;:]\n',
        text_string)

    all_header_list = list(
        set(mainheader_list) | set(header_list) | set(subheader_list))

    all_header_list = [i for i in all_header_list if (')' or '(') not in i]

    for header in all_header_list:
        text_string = text_string.replace(
            header,
            '\n\n### HEADER' + header + '\n')

    body_list = re.split('\n\n### HEADER\n.*\n\n', text_string)
    new_body_list = []
    for body in body_list:
        body = body.replace('\n', ' ')
        body = body.replace('- ', '')
        while '  ' in body:
            body = body.replace('  ', ' ')
        new_body_list.append(body)

    print(new_body_list)

    with open(f"{pdf_dict[filename]}.txt", "w", errors='ignore') as file:
        file.write(str(new_body_list))

    print(len(new_body_list))
