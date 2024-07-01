#!/usr/bin/env python3

import requests
from bs4 import BeautifulSoup
import re
import difflib

class ExtractBALISES:
    
    def __init__(self, url, official_sites):
        self.url = url
        self.official_sites = official_sites

    def parse_html_string(self, html_string, orientation):
        # Utilisation de la bibliothèque re pour récupérer toutes les balises
        balises = re.findall(r'<[^>]+>', html_string)

        # Variable chaîne de caractères utilisée pour concaténer les balises analysées
        balise_analysee = ""

        # Vérifier chaque balise
        for balise in balises:
            # Condition utilisée pour obtenir seulement le début de la balise, par exemple "span" de <span class="time">
            if " " in balise:
                balise = balise.replace(balise, balise.split(" ")[0])
            # Condition utilisée pour obtenir seulement la balise ouvrante comme <span>
            if "/" not in balise:
                balise = balise.split("<")[1].split(">")[0]
                balise_analysee += f"{balise}+("
            # Condition utilisée pour obtenir seulement la balise fermante comme </span>
            else:
                balise_analysee += ")"
        
        # Si les balises sont horizontales, modifier le format de balise_analysee
        if orientation == 'horizontal':
            balise_analysee = balise_analysee.replace("+(", " > ").replace(")", " <")
        
        return balise_analysee

    def clean_text_tags(self, tag):
        # Supprime complètement le contenu de la balise
        tag.clear()

    def detect_orientation(self, html_content):
        # Utiliser BeautifulSoup pour analyser le HTML
        soup = BeautifulSoup(html_content, 'html.parser')

        # Compter les balises directement imbriquées pour évaluer la disposition
        vertical_count = 0
        horizontal_count = 0

        for element in soup.descendants:
            if element.name:
                if element.parent and element.parent.name:
                    if element.parent.name in ['div', 'ul', 'ol', 'section', 'article']:
                        vertical_count += 1
                    elif element.parent.name in ['tr', 'td', 'th', 'table']:
                        horizontal_count += 1

        return 'vertical' if vertical_count >= horizontal_count else 'horizontal'

    def process_html(self, url):
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
                    lignes = cleaned_html.split(">")
                    lignes_nettoyees = []

                    for ligne in lignes:
                        ligne = ligne.strip()

                        if ligne:
                            if ligne.startswith("<"):
                                # Balise ouvrante et fermante
                                balise = ligne.split()[0]
                                lignes_nettoyees.append(balise + ">")
                            elif ligne.endswith("</"):
                                # Balise fermante
                                balise = ligne.split()[0].replace("</", "<")
                                lignes_nettoyees.append(balise)
                            else:
                                # Contenu texte
                                lignes_nettoyees.append(ligne)

                    cleaned_html = ">".join(lignes_nettoyees)

                    # Correction des balises en double
                    cleaned_html = cleaned_html.replace(">>", ">")

                    # Supprimer le texte à l'intérieur des balises
                    cleaned_html = re.sub(r'>[^<]+<', '><', cleaned_html)

                    return cleaned_html
                
                # Nettoyage du HTML
                cleaned_html = clean_html(html_content)
                
                # Correction des balises en double
                cleaned_html = cleaned_html.replace(">>", ">")
                
                # Suppression du texte à l'intérieur des balises
                cleaned_html = re.sub(r'>[^<]+<', '><', cleaned_html)
                
                return cleaned_html
            else:
                return None
        except Exception as e:
            return None

    def compute_similarity_score(parsed_tags_legitime, parsed_tags_phishing):
        # Calcul du ratio de similarité entre les deux structures de balises parsées
        similarity_ratio = difflib.SequenceMatcher(None, parsed_tags_legitime, parsed_tags_phishing).ratio()
        return similarity_ratio

    def balises_info(self):
        """Traite les URLs, extrait les balises HTML et les sauvegarde dans les fichiers Excel."""
        
        # Définition du pattern d'URL
        url_pattern = re.compile(r'https?://(?:www\.)?[^\s<>"]+|www\.[^\s<>"]+')
        
        # Initialisation des variables pour les balises HTML extraites
        parsed_tags_legitime = None
        parsed_tags_phishing = None
        top_score = -1
        
        # Vérification de l'URL de phishing
        if url_pattern.match(self.url):
            # Traitement de l'URL de phishing
            cleaned_html_phishing = self.process_html(self.url)
            
            if cleaned_html_phishing:
                # Détection de l'orientation des balises
                orientation = self.detect_orientation(cleaned_html_phishing)
                
                # Extraction et affichage des balises HTML parsées
                parsed_tags_phishing = self.parse_html_string(cleaned_html_phishing, orientation)
        
        for company in self.official_sites:
            parsed_tags_legitime = company["template"]
            # Si les deux URLs sont valides, calculer le score de similarité des balises
            if parsed_tags_legitime and parsed_tags_phishing:
                similarity_score = ExtractBALISES.compute_similarity_score(parsed_tags_legitime, parsed_tags_phishing)
                if similarity_score > top_score:
                    top_score = similarity_score
                    top_company = [company["id"], company["url"]]

        return parsed_tags_phishing, top_score, top_company
