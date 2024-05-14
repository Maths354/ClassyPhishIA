
import requests
from bs4 import BeautifulSoup
import re

class ExtractURL:
    
    def __init__(self, url):
        self.url = url

    def extract_and_save_urls(self):

        # Définir un en-tête User-Agent
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
        }

        # Faire la requête HTTP avec l'en-tête User-Agent
        response = requests.get(self.url, headers=headers)

        # Utiliser BeautifulSoup pour analyser le contenu HTML
        soup = BeautifulSoup(response.text, 'html.parser')

        # Extraire les URL avec l'expression régulière
        regex_urls = re.findall(r'https?://(?:www\.)?[^\s<>"]+|www\.[^\s<>"]+|http://[^\s<>"]+', response.text)

        print("regex : ", regex_urls)
        return regex_urls