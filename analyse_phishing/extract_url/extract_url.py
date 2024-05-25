import requests
import re
import difflib

class ExtractUrlBalises:
    def __init__(self, url):
        self.url = url

    def compute_similarity_score(self, urls_balises1, urls_balises2):
        # Calcul du ratio de similarité entre les deux structures de balises parsées
        similarity_ratio = difflib.SequenceMatcher(None, urls_balises1, urls_balises2).ratio()
        return similarity_ratio

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
        elif response.status_code == 403:
            print("Accès refusé. Veuillez vérifier vos permissions.")
            return []
        else:
            # Afficher un message d'erreur si la requête a échoué pour une autre raison
            print("La requête a échoué avec le code de statut:", response.status_code)
            return []

    def urls_balises_info(self, url_phishing):
        """Traite les URLs, extrait les balises HTML et les sauvegarde dans les fichiers Excel."""

        # Initialisation des variables pour les balises HTML extraites
        urls_balises1 = self.extract_urls()
        urls_balises2 = None

        # Vérification de l'URL de phishing
        url_pattern = re.compile(r'https?://(?:www\.)?[^\s<>"]+|www\.[^\s<>"]+')
        if url_pattern.match(url_phishing):
            # Traitement de l'URL de phishing
            phishing_extractor = ExtractUrlBalises(url_phishing)
            urls_balises2 = phishing_extractor.extract_urls()
        else:
            print(f"L'URL de phishing : {url_phishing} n'est pas une URL valide.")

        # Si les deux URLs sont valides, calculer le score de similarité des balises
        if urls_balises1 and urls_balises2:
            similarity_score = self.compute_similarity_score(urls_balises1, urls_balises2)
            print(f"\nScore de similarité des balises entre les deux URLs : {similarity_score:.2f}")

        # Retourner les balises HTML extraites
        return urls_balises1

# if __name__ == "__main__":
#     url_legitime = "https://www.orange.fr/portail"
#     url_phishing = "https://www.keraunos.org/"
#     extractor = ExtractUrlBalises(url_legitime)
#     extractor.urls_balises_info(url_phishing)
