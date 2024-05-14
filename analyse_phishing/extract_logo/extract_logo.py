

import logging
from urllib.parse import urljoin
from bs4 import BeautifulSoup
import requests


class ExtractLogo:
    
    def __init__(self, url):
        self.url = url

    def extract_logo_url(self):
        """Extraire l'URL du logo d'un site web."""
        try:
            # Obtenir le contenu HTML de l'URL
            response = requests.get(self.url, timeout=10)
            response.raise_for_status()

            # Analyser le contenu HTML avec BeautifulSoup
            soup = BeautifulSoup(response.text, 'html.parser')

            # Recherche de la balise <link> avec les types possibles d'images pour le logo
            favicon_link = (
                soup.find('link', rel='icon', type='image/x-icon') or
                soup.find('link', rel='shortcut icon', type='image/x-icon') or
                soup.find('link', rel='icon', type='image/png') or
                soup.find('link', rel='icon', type='image/jpeg') or
                soup.find('link', rel='icon', type='image/svg+xml') or
                soup.find('link', rel='icon', type='image/webp')
            )

            if favicon_link:
                favicon_url = favicon_link['href']
                if not favicon_url.startswith('http'):
                    favicon_url = urljoin(self.url, favicon_url)
                return favicon_url

            # Chercher dans les balises <img> avec les classes/id courants pour les logos
            logo_img = soup.find('img', {'class': 'logo'}) or soup.find('img', {'id': 'logo'})
            if logo_img:
                logo_url = logo_img['src']
                if not logo_url.startswith('http'):
                    logo_url = urljoin(self.url, logo_url)
                return logo_url

            # Chercher le fichier favicon.ico à la racine
            favicon_url = urljoin(self.url, 'favicon.ico')
            response = requests.get(favicon_url, timeout=10)
            if response.status_code == 200:
                return favicon_url

            return None
        
        except requests.RequestException as e:
            logging.error(f"Erreur lors de l'extraction du logo : {e}")
            return None