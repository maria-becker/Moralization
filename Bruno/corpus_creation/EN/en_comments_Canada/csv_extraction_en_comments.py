import os
from collections import Counter
import pprint as pp
import pandas as pd
import nltk
from nltk.tokenize import word_tokenize, sent_tokenize
import xlsxwriter
import csv
import pandas


#article_id,
#comment_counter,
#comment_author,
#timestamp,
#post_time,
#comment_text,
#TotalVotes,
#posVotes,
#negVotes,
#vote,
#reactions,
#replies,
#comment_id,
#parentID,
#threadID,
#streamId,
#edited,
#isModerator,
#highlightGroups,
#moderatorEdit,
#descendantsCount,
#threadTimestamp,
#flagCount,
#sender_isSelf,
#sender_loginProvider,
#data_type,
#is_empty,
#status


def clean_text(text):
    text = text.replace("</p>", " ")
    text = text.replace("<p>", " ")
    text = text.replace("\n", " ")
    text = text.replace("  ", " ")
    return text


def convert_to_text(path_to_source):

    with open(path_to_source, encoding="utf-8") as csv_file:
        data = csv.reader(csv_file, delimiter=',')

        text_string = ""

        counter = 0
        
        for row in data:
            
            try:
                text_string = text_string + f"###\nID:{row[12]}, Article:{row[0]}\n" + clean_text(row[5]) + "\n\n"
                counter += 1
                print(counter)
                if counter == 10000:
                    break
            except (ValueError, UnicodeDecodeError):
                print("error!")


        with open(f"{path_to_source}.txt", "w") as f:
            f.write(text_string)

    return None


path_to_source = "gnm_comments.csv"
convert_to_text(path_to_source)
