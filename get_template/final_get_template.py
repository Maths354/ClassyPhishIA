#!/usr/bin/env python3

import requests
from bs4 import BeautifulSoup
import pandas as pd
import re

def clean_text_tags(tag):
    # Supprime complètement le contenu de la balise
    tag.clear()

def extract_and_save_urls(url):
    # Définir un en-tête User-Agent
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
    }

    try:
        # Faire la requête HTTP avec l'en-tête User-Agent
        response = requests.get(url, headers=headers)
        
        # Vérifier si la requête a réussi
        if response.status_code == 200:
            # Utiliser BeautifulSoup pour analyser le contenu HTML
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Extraire les URL des attributs href et src
            non_url_list = [link.get('href') for link in soup.find_all('a', href=True)] + \
                            [img.get('src') for img in soup.find_all('img', src=True)]

            # Extraire les URL avec l'expression régulière
            regex_urls = re.findall(r'https?://(?:www\.)?[^\s<>"]+|www\.[^\s<>"]+|http://[^\s<>"]+', response.text)

            # Enregistrer les URL dans les fichiers
            with open('all_url.txt', 'w') as non_url_file:
                for non_url in non_url_list:
                    non_url_file.write(str(non_url) + '\n')

            with open('url.txt', 'w') as url_file:
                for regex_url in regex_urls:
                    url_file.write(str(regex_url) + '\n')

            return non_url_list, regex_urls
        elif response.status_code == 403:
            print("Accès refusé. Veuillez vérifier vos permissions.")
            return [], []
        else:
            # Afficher un message d'erreur si la requête a échoué pour une autre raison
            print("La requête a échoué avec le code de statut:", response.status_code)
            return [], []
    except Exception as e:
        print(f"Une erreur s'est produite lors de l'extraction des URLs : {e}")
        return [], []

def process_html(url):
    try:
        # Définir un en-tête User-Agent
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
        }
        
        # Effectue une requête GET à l'URL fournie avec l'en-tête User-Agent
        response = requests.get(url, headers=headers)
        
        # Vérifie si la requête a réussi (statut 200)
        if response.status_code == 200:
            # Récupère le contenu HTML de la page
            html_content = response.text
            
            # Utilise BeautifulSoup pour analyser le HTML
            soup = BeautifulSoup(html_content, 'html.parser')
            
            # Extrait toutes les balises sans leur contenu
            html_structure = [tag.prettify(formatter=None) for tag in soup.find_all(True, recursive=False)]
            
            # Nettoie le contenu texte des balises spécifiques
            tags_to_clean = ['h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'a', 'script']
            for tag_name in tags_to_clean:
                for tag in soup.find_all(tag_name):
                    clean_text_tags(tag)
            
            # Recrée la structure HTML mise à jour
            html_structure = [tag.prettify(formatter=None) for tag in soup.find_all(True, recursive=False)]
            
            # Écriture de la structure HTML dans un fichier temporaire
            temp_file = "temp_html_structure.html"
            with open(temp_file, 'w') as f:
                f.write("\n".join(html_structure))
            
            # Fonction pour nettoyer le HTML
            def clean_html(input_file, output_file):
                with open(input_file, 'r') as f:
                    lines = f.readlines()

                with open(output_file, 'w') as f:
                    for line in lines:
                        # Supprimer les lignes de commentaire HTML
                        if not re.match(r'^\s*<!--.*?-->\s*$', line):
                            # Réécrire la ligne si elle n'est pas un commentaire
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
            
            # Nettoyage du HTML
            clean_html(temp_file, "cleaned_output.html")
            
            # Correction des balises en double
            with open("cleaned_output.html", 'r') as f:
                lines = f.readlines()
            with open("cleaned_output.html", 'w') as f:
                for line in lines:
                    f.write(line.replace(">>", ">"))
            
            # Suppression du texte à l'intérieur des balises
            with open("cleaned_output.html", 'r') as f:
                content = f.read()
            content = re.sub(r'>[^<]+<', '><', content)
            with open("final_output.html", 'w') as f:
                f.write(content)
            
            print("Le fichier HTML final a été créé avec succès : final_output.html")
            return True
        elif response.status_code == 403:
            print("Accès refusé. Veuillez vérifier vos permissions.")
            return False
        else:
            print(f"La requête a échoué avec le code d'état : {response.status_code}")
            return False
    except Exception as e:
        print(f"Une erreur s'est produite lors du traitement du HTML : {e}")
        return False

def main():
    # Demande à l'utilisateur de fournir l'URL
    url = input("Entrez l'URL de la page dont vous souhaitez récupérer le code HTML : ")

    # Appelle la fonction et récupère la structure HTML si disponible
    if process_html(url):
        # Exemple d'utilisation de la fonction extract_and_save_urls
        print("\nExtraction des URLs...")
        non_url_list, regex_urls = extract_and_save_urls(url)

        print("URLs extraites des attributs href et src (all_url.txt) :")

main()