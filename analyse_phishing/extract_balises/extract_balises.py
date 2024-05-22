#!/usr/bin/env python3

import requests
from bs4 import BeautifulSoup
import re
import difflib

class ExtractBALISES:
    
    def __init__(self, url):
        self.url = url

    @staticmethod
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

    @staticmethod
    def clean_text_tags(tag):
        # Supprime complètement le contenu de la balise
        tag.clear()

    def process_html(self):
        try:
            # Définir un en-tête User-Agent
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
            }
            
            # Effectue une requête GET à l'URL fournie avec l'en-tête User-Agent
            response = requests.get(self.url, headers=headers)
            
            # Vérifie si la requête a réussi (statut 200)
            if response.status_code == 200:
                # Récupère le contenu HTML de la page
                html_content = response.text
                html_content = re.sub(r'<!DOCTYPE[^>]*>', '', html_content)
                
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

    @staticmethod
    def compute_similarity_score(parsed_tags1, parsed_tags2):
        # Calcul du ratio de similarité entre les deux structures de balises parsées
        similarity_ratio = difflib.SequenceMatcher(None, parsed_tags1, parsed_tags2).ratio()
        return similarity_ratio

    @staticmethod
    def url_input(url_legitime, url_phishing):
        """Traite les URLs, extrait les balises HTML et les sauvegarde dans les fichiers Excel."""
        
        # Définition du pattern d'URL
        url_pattern = re.compile(r'https?://(?:www\.)?[^\s<>"]+|www\.[^\s<>"]+')
        
        # Initialisation des variables pour les balises HTML extraites
        parsed_tags1 = None
        parsed_tags2 = None
        
        # Vérification de l'URL légitime
        if url_pattern.match(url_legitime):
            # Traitement de l'URL légitime
            extract1 = ExtractBALISES(url_legitime)
            cleaned_html1 = extract1.process_html()
            
            if cleaned_html1:
                # Extraction et affichage des balises HTML parsées
                print("\nTags parsés de l'URL 1:")
                parsed_tags1 = extract1.parse_html_string(cleaned_html1)
                print(parsed_tags1)

        else:
            print(f"L'URL légitime : {url_legitime} n'est pas une URL valide.")
        
        # Vérification de l'URL de phishing
        if url_pattern.match(url_phishing):
            # Traitement de l'URL de phishing
            extract2 = ExtractBALISES(url_phishing)
            cleaned_html2 = extract2.process_html()
            
            if cleaned_html2:
                # Extraction et affichage des balises HTML parsées
                print("\nTags parsés de l'URL 2:")
                parsed_tags2 = extract2.parse_html_string(cleaned_html2)
                print(parsed_tags2)
        
        else:
            print(f"L'URL de phishing : {url_phishing} n'est pas une URL valide.")
        
        # Si les deux URLs sont valides, calculer le score de similarité des balises
        if parsed_tags1 and parsed_tags2:
            similarity_score = ExtractBALISES.compute_similarity_score(parsed_tags1, parsed_tags2)
            print(f"\nScore de similarité des balises entre les deux URLs : {similarity_score:.2f}")
        
        # Retourner les balises HTML extraites
        return parsed_tags1, parsed_tags2

if __name__ == "__main__":
    url_legitime = "https://www.keraunos.org/"
    url_phishing = "https://www.keraunos.org/"
    ExtractBALISES.url_input(url_legitime, url_phishing)
