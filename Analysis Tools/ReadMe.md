# Annotation Analysis Tools
Get examples of specific phenomena or perform statistical and linguistic analyses on the dataset.

## Contents
1. **annotation_statistics**: Code for generating statistics about the annotations. Includes simple-to-use jupyter notebooks for showcasing.
   + Uses XMI-Files as input.
   + Language-independend.
   + Documentation not fully finshed; in the process of updating.
2. **moral_indicators**: Perfom analyses on the linguistic surface. Find which words/POS are common for different annotation categories, and which are typical of moralizing speech. Includes a jupyter notebook for showcasing.
   + Uses XMI files and Excel files with specific formats as input.
   + Only German Hanta-tagging is supported. WIP!
   + Documentation not fully finshed; in the process of updating.
3. **search_moralizations**: Search for all moralizations that include a certain phenomenon, such as a certain lexeme. Useful for generating examples. Includes simple-to-use jupyter notebooks for showcasing.
   + Uses XMI-Files as input.
   + All four languages of the project (German, English, Italian, French) supported.
   + Documentation not fully finshed; in the process of updating.
4. **\_utils\_**
   + Used by other modules and toolsets. Not very useful by itself.


## Dependencies
The code was tested on Python3.12, though it might work with Python versions 3.7 and up.

Before running this code, make sure you have the following dependencies installed:
+ NLTK
+ HanTa
+ Spacy
+ xlsxwriter
+ pandas
+ matplotlib
+ scipy
+ numpy
