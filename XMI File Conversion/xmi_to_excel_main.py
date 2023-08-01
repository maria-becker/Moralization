import xmi_to_excel as xte


# Extract xmi annotations from zip directories inside an
# exported Inception project. Use 'annotation' directory as source
xte.extract_files(r"IÜD\Daten-IUED-180723\annotation", r"goalpath")

# Iterate over directories (created by above function)
# and create excel files in the goal directory for each xmi file

# Creates more detailed excel files
xte.xmi_iterate_count(r"extracted_files_path", r"goalpath")

# Creates more compact excel files
xte.xmi_iterate_minimal(r"extracted_files_path", r"goalpath")


# Iterate over files without a directory structure
# (In our project, these were the German files)
# and create excel files in the goal directory for each xmi file

# Creates more detailed excel files
xte.xmi_iterate_german_count(
    (r"C:\Users\Arbeit\Desktop\Bachelorarbeit\Data"
        r"\Moralisierungsdateien_DE_xmi\documents-export-2023-01-25"),
    r"C:\Users\Arbeit\Desktop\Output_neu_long")

# Creates more compact excel files
xte.xmi_iterate_german_minimal(
    (r"C:\Users\Arbeit\Desktop\Bachelorarbeit\Data"
        r"\Moralisierungsdateien_DE_xmi\documents-export-2023-01-25"),
    r"C:\Users\Arbeit\Desktop\Output_neu_short")


# For converting a single XMI file, if necessary
xte.write_excel_count(r"source", r"goal")  # Coprehensive
xte.write_excel_minimal(r"source", r"goal")  # Compact
