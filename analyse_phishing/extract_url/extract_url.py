import requests
import re
import difflib
from time import sleep

class ExtractUrlBalises:
    def __init__(self, url, official_sites):
        self.url = url
        self.official_sites = official_sites
        self.urls_balises_phishing = list()

    def compute_similarity_score(self):
        # Calcul du ratio de similarité entre les deux structures de balises parsées
        similarity_ratio = 0
        top_company = ""
        for company in self.official_sites:
            urls_official_site= company["list_url"]
            #eval is used to convert str to list
            ratio = difflib.SequenceMatcher(None, eval(urls_official_site), self.urls_balises_phishing).ratio()
            if ratio >= similarity_ratio:
                similarity_ratio = ratio
                top_company=[company["id"],company["url"]]
        return similarity_ratio, top_company

    def extract_urls(self):
        # Définir un en-tête User-Agent
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
        }

        # Faire la requête HTTP avec l'en-tête User-Agent
        response = requests.get(self.url, headers=headers)

        # Vérifier si la requête a réussi
        if response.status_code == 200:
            # Extraire les URL avec l'expression régulière
            regex_urls = re.findall(r'https?://(?:www\.)?[^\s<>"]+|www\.[^\s<>"]+|http://[^\s<>"]+', response.text)

            return regex_urls
        else:
            return []

    def urls_balises_info(self):
        """Traite les URLs, extrait les balises HTML et les sauvegarde dans les fichiers Excel."""

        # Vérification de l'URL de phishing si fournie
        url_pattern = re.compile(r'https?://(?:www\.)?[^\s<>"]+|www\.[^\s<>"]+')
        if url_pattern.match(self.url):
            # Traitement de l'URL de phishing
            self.urls_balises_phishing = self.extract_urls()

        # Si les deux URLs sont valides, calculer le score de similarité des balises
        if self.urls_balises_phishing:
            similarity_score, top_company = self.compute_similarity_score()

        # Retourner les balises HTML extraites
        return self.urls_balises_phishing, similarity_score, top_company