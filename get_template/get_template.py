#!/usr/bin/env python3

import requests
from bs4 import BeautifulSoup
import pandas as pd
import re
import difflib

def parse_html_string(html_string):
    #using re library to get all tags
    tags = re.findall(r'<[^>]+>', html_string)

    #String variable used to concatenate parsed tag
    parsed_tag=""

    #Check every tag
    for tag in tags:
        #condition used to get only the start of the tag, for example "span" from <span class="time">
        if " " in tag:
            tag = tag.replace(tag,tag.split(" ")[0])
        #condition used to get only start tag like <span>
        if "/" not in tag:
            tag=tag.split("<")[1].split(">")[0]
            parsed_tag+=f"{tag}+("
        #condition used to get only end tag like </span>
        else:
            parsed_tag+=")"
    return parsed_tag

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
            html_content = re.sub(r'<!DOCTYPE[^>]*>', '', html_content)
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
            
            # Fonction pour nettoyer le HTML
            def clean_html(html_content):
                # Utiliser BeautifulSoup pour analyser le HTML
                soup = BeautifulSoup(html_content, 'html.parser')

                # Parcourir toutes les balises <script>
                for script_tag in soup.find_all('script'):
                    # Supprimer le contenu des balises <script>, mais laisser les balises elles-mêmes
                    script_tag.clear()

                # Convertir l'objet soup en une chaîne de caractères (html nettoyé)
                cleaned_html = str(soup)

                # Supprimer les commentaires HTML
                cleaned_html = re.sub(r'<!--.*?-->', '', cleaned_html, flags=re.DOTALL)

                # Nettoyer les caractères indésirables (comme les crochets)
                cleaned_html = cleaned_html.replace("[", "").replace("]", "")

                # Nettoyage et réécriture des balises ouvrantes et fermantes
                lines = cleaned_html.splitlines()
                cleaned_lines = []

                for line in lines:
                    line = line.strip()

                    if line.startswith("<") and line.endswith(">"):
                        # Balise ouvrante et fermante
                        tag = line.split()[0]
                        cleaned_lines.append(tag + ">")
                    elif line.startswith("<"):
                        # Balise ouvrante
                        tag = line.split()[0]
                        cleaned_lines.append(tag + ">")
                    elif line.endswith(">"):
                        # Balise fermante
                        tag = line.split()[0].replace("</", "<")
                        cleaned_lines.append(tag)
                    else:
                        # Contenu texte
                        cleaned_lines.append(line)

                cleaned_html = '\n'.join(cleaned_lines)

                # Correction des balises en double
                cleaned_html = cleaned_html.replace(">>", ">")

                # Supprimer le texte entre les balises
                cleaned_html = re.sub(r'>[^<]+<', '><', cleaned_html)

                return cleaned_html

            
            # Nettoyage du HTML
            cleaned_html = clean_html(html_content)
            
            # Correction des balises en double
            cleaned_html = cleaned_html.replace(">>", ">")
            
            # Suppression du texte à l'intérieur des balises
            cleaned_html = re.sub(r'>[^<]+<', '><', cleaned_html)
            
            return cleaned_html
        elif response.status_code == 403:
            print("Accès refusé. Veuillez vérifier vos permissions.")
            return None
        else:
            print(f"La requête a échoué avec le code d'état : {response.status_code}")
            return None
    except Exception as e:
        print(f"Une erreur s'est produite lors du traitement du HTML : {e}")
        return None



def compute_similarity_score(parsed_tags1, parsed_tags2):
    # Calcul du ratio de similarité entre les deux structures de balises parsées
    similarity_ratio = difflib.SequenceMatcher(None, parsed_tags1, parsed_tags2).ratio()
    return similarity_ratio

def url_input(url1, url2):
    # Définition du pattern d'URL
    url_pattern = re.compile(r'https?://(?:www\.)?[^\s<>"]+|www\.[^\s<>"]+')

    # Vérification de la première URL
    is_url1 = url_pattern.match(url1)
    if is_url1:
        # Traitement de l'URL 1
        cleaned_html1 = process_html(url1)
        if cleaned_html1:
            print("URLs extraites de l'URL 1:")
            non_url_list1, regex_urls1 = extract_and_save_urls(url1)
            print(non_url_list1)
            print(regex_urls1)

            print("HTML nettoyé de l'URL 1:")
            print(cleaned_html1)

            print("\nTags parsés de l'URL 1:")
            parsed_tags1 = parse_html_string(cleaned_html1)
            print(parsed_tags1)
    else:
        print(f"L'URL 1 : {url1} n'est pas une URL valide.")

    # Vérification de la deuxième URL
    is_url2 = url_pattern.match(url2)
    if is_url2:
        # Traitement de l'URL 2
        cleaned_html2 = process_html(url2)
        if cleaned_html2:
            print("URLs extraites de l'URL 2:")
            non_url_list2, regex_urls2 = extract_and_save_urls(url2)
            print(non_url_list2)
            print(regex_urls2)

            print("HTML nettoyé de l'URL 2:")
            print(cleaned_html2)

            print("\nTags parsés de l'URL 2:")
            parsed_tags2 = parse_html_string(cleaned_html2)
            print(parsed_tags2)
    else:
        print(f"L'URL 2 : {url2} n'est pas une URL valide.")

    # Si les deux URLs sont valides, calculer le score de similarité
    if is_url1 and is_url2:
        similarity_score = compute_similarity_score(parsed_tags1, parsed_tags2)
        print(f"\nScore de similarité entre les deux URLs : {similarity_score:.2f}")
