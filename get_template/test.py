#! /usr/bin/env python3

def clean_html(input_file, output_file):
    with open(input_file, 'r') as f:
        lines = f.readlines()

    with open(output_file, 'w') as f:
        for line in lines:
            line = line.strip()
            if line.startswith("<") and line.endswith(">"):
                # Balise ouvrante et fermante
                tag = line.split()[0]
                f.write(tag + ">\n")
            elif line.startswith("<"):
                # Balise ouvrante
                tag = line.split()[0]
                f.write(tag + ">\n")
            elif line.endswith(">"):
                # Balise fermante
                tag = line.split()[0].replace("</", "<")
                f.write(tag + "\n")
            else:
                # Contenu texte
                f.write(line + "\n")

def fix_duplicates(output_file):
    with open(output_file, 'r') as f:
        lines = f.readlines()

    with open(output_file, 'w') as f:
        for line in lines:
            f.write(line.replace(">>", ">"))

input_file = "test.html"
output_file = "cleaned_output.html"
clean_html(input_file, output_file)
fix_duplicates(output_file)
