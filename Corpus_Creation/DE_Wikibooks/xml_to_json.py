import xml.etree.ElementTree as ET
import json
from nltk.tokenize import sent_tokenize


def check_relevance(text, metadata):
    irrelevant_titles = [
        "Traktorenlexikon",
        "Mathe",
        "Grammatik",
        "Spanisch",
        "Latein",
        "Russisch",
        "Schaltungen",
        "Wikijunior",
        "Programmierung",
        "GIMP",
        "Websiteentwicklung",
        "Gitarre",
        "Staatsexamen",
        "Linux",
        "Gambas",
        "Programmierkurs",
        "Türkisch",
        "Portugiesisch",
        "Französisch",
        "Japanisch",
        "Esperanto",
        "spiele",
        "Englisch",
        "Statistik",
        "Cocktails",
        "Diffgeo",
        "Klettern",
        "Kochbuch",
        "SDL",
        "Blender",
        "Java",
        "Vektoranalysis",
        "OpenOffice.org",
        "Mac-OS-Kompendium",
        "Funktionentheorie",
        "Hebräisch",
        "LaTeX",
        "Netzwerktechnik",
        "Procmail",
        "Elektrotechnik",
        "Programmieren",
        "Programmierung",
        "Datenkompression",
        "GNU",
        "CPU",
        "Kroatisch",
        "Chinesisch",
        "Adventskalender",
        "Spiele",
        "Dienstvorschriften",
        "Liederbuch",
        "GnuPG",
        "Motoren aus technischer Sicht",
        "Bauelemente",
        "A Poem a Day",
        "OpenRewi",
        "Ido-Kompaktkurs",
        "Till Eulenspiegels",
        "Inkscape",
        "Quadriviale Kuriositäten",
        "Webdesign",
        ".NET",
        "ISDN-Technik",
        "Öffentliches Recht",
        "Arabisch",
        "Geschichte",
        "Go/",
        "bildgebende Verfahren",
        "Algorithmen und Datenstrukturen",
        "Einbürgerungstest",
        "Examensrepetitorium",
        "Learning the vi editor",
        "Gnutella",
        "Poker",
        "Medizinische Mikrobiologie",
        "Schach:",
        "Physikalische Grundlagen der Nuklearmedizin",
        "Studienführer Hans Albert: Liste der wissenschaftlichen Artikel",
        "Pathologie:",
        "Anorganische Chemie für Schüler/ Atombau ",
        "Wikipedia-Lehrbuch: ",
        "Teilchenphysik: "
    ]
    if text.count(" ") < 5 or text.count(" - ") > 20:
        return False
    if text.count("•") > 1 or '\n' in text:
        return False
    for element in irrelevant_titles:
        if element in metadata:
            return False
    if len(sent_tokenize(text)) < 3:
        return False

    return True


# Define a namespace dictionary to associate the prefix with the namespace URI
ns = {"tei": "http://www.tei-c.org/ns/1.0"}

# Parse the XML file
tree = ET.parse(r"wikibooks\wikibooks_dwds.xml")
root = tree.getroot()

# Initialize a dictionary to store text passages with source strings
passages_with_sources = []

# Iterate through each book in the XML using the namespace prefix
for book in root.findall('.//tei:TEI', namespaces=ns):
    # Initialize a dictionary to store text passages with source strings
    book_passages_with_sources = {}

    # Extract book information from the TEI header for this book
    title_elem = book.find('.//tei:titleStmt/tei:title[@type="main"]', namespaces=ns)
    if title_elem is not None:
        title = title_elem.text
    else:
        title = 'Unbekannter Titel'

    # Extract all text content from <p> elements for this book and create source strings
    book_passages = []
    for p in book.findall('.//tei:body/tei:p', namespaces=ns):
        text = p.text
        # Heuristically heck whether paragraph contains longer text
        if text:
            if check_relevance(text, title):
                source_string = f"Wikibooks: {title}"
                book_passages.append({'source': source_string, 'text': text})

    # Append the passages for this book to the list for all books
    passages_with_sources.extend(book_passages)

# Save passages with source strings for all books to a JSON file
with open('wikibooks_dwds.json', 'w', encoding='utf-8') as json_file:
    json.dump(passages_with_sources, json_file, ensure_ascii=False, indent=4)

print("Text passages with source strings saved to 'wikibooks_dwds.json'")
