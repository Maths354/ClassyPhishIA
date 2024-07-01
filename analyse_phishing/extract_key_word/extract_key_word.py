import string
import requests
from bs4 import BeautifulSoup

class ExtractKeyWord:
    def __init__(self, url, official_sites):
        # Initialiser avec l'URL cible et une liste de sites officiels avec mots-clés
        self.url = url
        self.official_sites = official_sites

    def analyze_text(self):
        keywords = []  # Liste pour stocker les mots-clés
        company_match = []  # Liste pour stocker les correspondances de sociétés

        # Récupérer les mots-clés des sociétés
        for company in self.official_sites:
            keywords.append(company["key_word"])

        # Extraire le texte de l'URL donnée
        texte = self.extract_text_from_url()
        keyword_counts = {}  # Dictionnaire pour compter les occurrences des mots-clés
        if texte != None:
            # Enlever les ponctuations du texte et convertir en minuscules
            texte = texte.translate(str.maketrans('', '', string.punctuation)).lower()
        
            # Découper le texte en mots
            words = texte.split()
            
            # Compter les occurrences de chaque mot-clé dans le texte
            for word in words:
                if word in keywords:
                    if word in keyword_counts:
                        keyword_counts[word] += 1
                    else:
                        keyword_counts[word] = 1

        # Si des mots-clés ont été trouvés
        if keyword_counts:
            score = 1
            for company in self.official_sites:
                # Vérifier si le mot-clé de la société est présent dans le texte
                if company["key_word"] in list(keyword_counts.keys()):
                    # Ajouter l'URL de la société correspondante si elle n'est pas déjà dans la liste
                    if company["url"] not in company_match:
                        company_match.append(company["url"])
        else:
            # Aucun mot-clé trouvé
            score = 0

        # Retourner les comptes de mots-clés, le score et les correspondances de sociétés
        return keyword_counts, score, company_match
    
    def extract_text_from_url(self):
        try:
            # Faire une requête GET à l'URL pour récupérer le contenu
            response = requests.get(self.url)
            response.raise_for_status()  # Vérifier si la requête a réussi

            # Utiliser BeautifulSoup pour parser le contenu HTML
            soup = BeautifulSoup(response.content, 'html.parser')

            # Extraire tout le texte de la page en supprimant les espaces inutiles
            text = soup.get_text(separator=' ', strip=True)
            
            return text
        except requests.exceptions.RequestException as e:
            # Gérer les exceptions en cas d'erreur de requête
            print(f"Erreur lors de la récupération de l'URL : {e}")
            return None
