import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import os
import logging

# Configurer le journal
logging.basicConfig(level=logging.INFO)

def extract_logo_url(url):
    """Extraire l'URL du logo d'un site web."""
    try:
        # Obtenir le contenu HTML de l'URL
        response = requests.get(url, timeout=10)
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
                favicon_url = urljoin(url, favicon_url)
            return favicon_url

        # Chercher dans les balises <img> avec les classes/id courants pour les logos
        logo_img = soup.find('img', {'class': 'logo'}) or soup.find('img', {'id': 'logo'})
        if logo_img:
            logo_url = logo_img['src']
            if not logo_url.startswith('http'):
                logo_url = urljoin(url, logo_url)
            return logo_url

        # Chercher le fichier favicon.ico à la racine
        favicon_url = urljoin(url, 'favicon.ico')
        response = requests.get(favicon_url, timeout=10)
        if response.status_code == 200:
            return favicon_url
        
        return None
    except requests.RequestException as e:
        logging.error(f"Erreur lors de l'extraction du logo : {e}")
        return None

def download_image(image_url, directory='./'):
    """Télécharger une image à partir de son URL."""
    try:
        # Vérifier si le répertoire existe, sinon le créer
        if not os.path.exists(directory):
            os.makedirs(directory)
        
        filename = os.path.join(directory, os.path.basename(image_url))

        # Télécharger l'image
        response = requests.get(image_url)
        response.raise_for_status()

        with open(filename, 'wb') as file:
            file.write(response.content)
        
        logging.info(f"L'image a été téléchargée avec succès sous le nom : {filename}")
    except requests.RequestException as e:
        logging.error(f"Erreur lors du téléchargement de l'image : {e}")

def main():
    url = input("Entrez l'URL du site web : ")
    logo_url = extract_logo_url(url)
    if logo_url:
        logging.info(f"L'URL du logo du site est : {logo_url}")
        download_image(logo_url)
    else:
        logging.info("Aucun logo trouvé pour ce site.")

if __name__ == "__main__":
    main()
