import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import os

def extract_logo_url(url):
    try:
        # Obtenir le contenu HTML de l'URL
        response = requests.get(url)
        response.raise_for_status()  # Vérifier si la requête a été réussie

        # Analyser le contenu HTML avec BeautifulSoup
        soup = BeautifulSoup(response.text, 'html.parser')

        # Rechercher la balise <link> avec le type "image/x-icon" ou "image/png" ou "image/jpeg" pour le logo du site
        favicon_link = soup.find('link', rel='icon', type='image/x-icon')
        if not favicon_link:
            favicon_link = soup.find('link', rel='shortcut icon', type='image/x-icon')
        if not favicon_link:
            favicon_link = soup.find('link', rel='icon', type='image/png')
        if not favicon_link:
            favicon_link = soup.find('link', rel='icon', type='image/jpeg')

        if favicon_link:
            # Obtenir l'URL du logo
            favicon_url = favicon_link['href']
            # Si l'URL est relative, la convertir en URL absolue
            if not favicon_url.startswith('http'):
                favicon_url = urljoin(url, favicon_url)
            return favicon_url
        else:
            return None
    except Exception as e:
        print("Une erreur s'est produite lors de l'extraction du logo :", e)
        return None

def download_image(image_url, directory='./'):
    try:
        # Obtenir le nom du fichier à partir de l'URL de l'image
        filename = os.path.join(directory, os.path.basename(image_url))
        
        # Télécharger l'image
        with open(filename, 'wb') as file:
            response = requests.get(image_url)
            file.write(response.content)
        
        print(f"L'image a été téléchargée avec succès sous le nom : {filename}")
    except Exception as e:
        print("Une erreur s'est produite lors du téléchargement de l'image :", e)

def main():
    url = input("Entrez l'URL du site web : ")
    logo_url = extract_logo_url(url)
    if logo_url:
        print("L'URL du logo du site est :", logo_url)
        download_image(logo_url)
    else:
        print("Aucun logo trouvé pour ce site.")

if __name__ == "__main__":
    main()
