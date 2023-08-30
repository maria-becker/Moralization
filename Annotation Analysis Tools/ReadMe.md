# Annotation Analysis Tools
Get examples of specific phenomena or perform statistical analysis on the dataset.

## Contents
1. **Stats_and_Search**: Code for example retrieval and statistics about the annotations. Includes simple-to-use jupyter notebooks for retrieving examples and calculating statistics, both for single corpus files and a collection of corpus files, respectively.
   + Uses XMI-Files as input.
   + Only German and English are currently fully supported; some search functions don't work with other languages and are work in progress.
   + Documentation is getting updated.
2. **moral_indicators**: Perfom analyses on the linguistic surface. Find which words/POS are common for different annotation categories, and which are typical of moralizing speech.
   + Work in progress!
   + Currently uses XMI files and Excel files with specific formats as input.
   + Currently does not include user-friendly notebooks, nor is the documentation updated.
3. **protagonist_analysis_GER**: Perform analyses on protagonists in the German dataset. Almost all tasks can also be achieved via Stats_and_Search, better use those modules.
   + Depricated, in the process of being integrated into Stats_and_Search.
   + Will be deleted at a later date.

## Dependencies
Before running this code, make sure you have the following dependencies installed:

+ NLTK
+ HanTa
+ xlsxwriter
+ pandas
+ matplotlib
+ scipy
+ numpy
