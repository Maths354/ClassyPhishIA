import requests
import re
import difflib
from time import sleep

class ExtractUrlBalises:
    def __init__(self, url):
        self.url = url
        self.urls_balises_phishing = list()

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

        # Retourner les balises HTML extraites
        return self.urls_balises_phishing