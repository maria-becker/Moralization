import codecs
import striprtf.striprtf as strp
import re


def to_txt(filename):
# Sometimes you have to change the encoding type (utf-8, utf-16, ...)
    with open(f"{filename}.rtf", 'r') as f:
        file_contents = f.read()

    text = strp.rtf_to_text(file_contents, errors="ignore")

    text = text.replace(chr(160), " ")
    text = text.replace("End of Document", "###")
    text = text.replace("©", "")
    text = re.sub(r"Section:.*", "", text)
    text = re.sub(r"Length:.*", "", text)
    text = re.sub(r"Highlight:.*", "", text)
    text = re.sub(r"Byline:.*", "", text)
    text = re.sub(r"Load-Date:.*", "", text)
    #text = re.sub(r"Copyright.*", "", text)
    text = re.sub(r"Dateline.*", "", text)
    text = re.sub(r".*Edizione", "", text)
    text = text.replace("Body", "")
    while "\n\n\n" in text:
        text = text.replace("\n\n\n", "\n\n")

    text = text.replace("###\n\n", "###\n\n#METADATA:\n")

    # Be aware of the mode with which the file is opened
    # when you want to create (w)/append (a)
    with codecs.open("Italian_Comments.txt", 'a', encoding="utf-8") as f:
        f.write(text)
    print(filename)
    return None

file_list = []
for n in range(8):
    filename = f"Nexis_Comments_{n+1}"
    file_list.append(filename)

for file in file_list:
    to_txt(file)
