# XMI File Conversion
Only the conversion from XMI to Excel is currently supported.

## Usage
1. In xmi_to_excel_main, comment out functions that you do not want to use
2. Change the filepaths to your directory structure
3. Run the xmi_to_excel_main script


The module has the following fuctionalities:
+ Extract XMI annotation files from ZIP files (this is based on the normal export format for Inception projects)
+ Convert XMI files inside subdirectories into Excel files (based on the output of the ZIP extraction)
+ Convert XMI files inside a directory into Excel files (if another method of extracting XMI files was used and they are not sorted)
+ Convert a single XMI file into a single Excel file

For all conversions, two options are available. The *minimal* functions create a more compact Excel file. The *count* functions create a bigger Excel file containing token counts for each category, making certain calculations easier.

See the comments in the xmi_to_excel_main module for more details.

## Dependencies
Before running this code, make sure you have the following dependencies installed:

+ ElementTree
+ xlsxwriter
+ zipfile
