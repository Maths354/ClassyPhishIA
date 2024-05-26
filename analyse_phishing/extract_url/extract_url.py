import requests
import re
import difflib

class ExtractUrlBalises:
    def __init__(self, url):
        self.url = url

    def compute_similarity_score(self,urls_balises_legitime, urls_balises_phishing):
        # Calcul du ratio de similarité entre les deux structures de balises parsées
        similarity_ratio = difflib.SequenceMatcher(None, urls_balises_legitime, urls_balises_phishing).ratio()
        return similarity_ratio

    def extract_urls(self,url):
        # Définir un en-tête User-Agent
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
        }

        # Faire la requête HTTP avec l'en-tête User-Agent
        response = requests.get(url, headers=headers)

        # Vérifier si la requête a réussi
        if response.status_code == 200:
            # Extraire les URL avec l'expression régulière
            regex_urls = re.findall(r'https?://(?:www\.)?[^\s<>"]+|www\.[^\s<>"]+|http://[^\s<>"]+', response.text)

            return regex_urls
        else:
            return []

    def urls_balises_info(self, url_legitime="https://www.orange.fr"):
        """Traite les URLs, extrait les balises HTML et les sauvegarde dans les fichiers Excel."""

        # Initialisation des variables pour les balises HTML extraites
        urls_balises_legitime = self.extract_urls(url_legitime)
        urls_balises_phishing = None

        # Vérification de l'URL de phishing si fournie
        if self.url:
            url_pattern = re.compile(r'https?://(?:www\.)?[^\s<>"]+|www\.[^\s<>"]+')
            if url_pattern.match(self.url):
                # Traitement de l'URL de phishing
                urls_balises_phishing = self.extract_urls(self.url)

        # Si les deux URLs sont valides, calculer le score de similarité des balises
        if urls_balises_legitime and urls_balises_phishing:
            similarity_score = self.compute_similarity_score(urls_balises_legitime, urls_balises_phishing)

        # Retourner les balises HTML extraites
        return urls_balises_phishing, similarity_score