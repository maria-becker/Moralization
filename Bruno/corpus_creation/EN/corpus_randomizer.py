import os
from collections import Counter
import pprint as pp
import pandas
import nltk
from nltk.tokenize import word_tokenize, sent_tokenize
import xlsxwriter
import random

def randomize_corpus(corpus_file, number, seed):
	"""
	Creates a random corpus with ´number´ entries from corpus_file.
	"""

	dataframe = pandas.read_excel(corpus_file, header=None)


	print(dataframe)
	print(dataframe[0][20])

	random.seed(seed)
	random_list = random.sample(range(0, dataframe.shape[0] // 2), number)
	random_list.sort()
	print(random_list)

	workbook = xlsxwriter.Workbook(f'#{corpus_file}{number}.xlsx')
	worksheet = workbook.add_worksheet()
	bold = workbook.add_format({'bold': True})

	row = 0

	for integer in random_list:
		worksheet.write(row, 0, dataframe[0][integer*2], bold)
		row += 1
		worksheet.write(row, 0, dataframe[0][integer*2+1])
		row +=1

	workbook.close()
	print("\n\n\n\nDone!")

	return None


corpus_file = "Sachtexte_IT_positiv"
seed = 1998   # Use 1998 for consistent results.


randomize_corpus(f"{corpus_file}.xlsx", 945, seed)
