import bz2

# Input .xml.bz2 file and output .xml file names
input_bz2_file = 'dewikibooks-20230901-pages-articles-multistream.xml.bz2'
output_xml_file = 'wikibooks_full.xml'

# Open the .xml.bz2 file and decompress it, then save it as a regular .xml file
with bz2.BZ2File(input_bz2_file, 'rb') as bz_file:
    with open(output_xml_file, 'wb') as xml_file:
        for data in bz_file:
            xml_file.write(data)

print(f"XML content extracted and saved as '{output_xml_file}'")
