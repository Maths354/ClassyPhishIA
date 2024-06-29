import string
import requests
from bs4 import BeautifulSoup

class ExtractKeyWord:

    def __init__(self, url, official_sites):
        self.url = url
        self.official_sites = official_sites

    def analyze_text(self):

        keywords = list()

        for company in self.official_sites:
            keywords.append(company["key_word"])

        texte = self.extract_text_from_url()
        keyword_counts = {}
        if texte != None:
            # Enlever les ponctuations du texte et convertir en minuscules
            texte = texte.translate(str.maketrans('', '', string.punctuation)).lower()
        
            # Découper en mots
            words = texte.split()
            
            for word in words:
                if word in keywords:
                    if word in keyword_counts:
                        keyword_counts[word] += 1
                    else:
                        keyword_counts[word] = 1


        print("Mots-clés trouvés avec leurs occurrences :", keyword_counts)        
        return keyword_counts
    

    def extract_text_from_url(self):
        try:
            response = requests.get(self.url)
            response.raise_for_status()

            soup = BeautifulSoup(response.content, 'html.parser')

            # Extraire tout le texte de la page
            text = soup.get_text(separator=' ', strip=True)
            
            return text
        except requests.exceptions.RequestException as e:
            print(f"Erreur lors de la récupération de l'URL : {e}")
            return None

    
