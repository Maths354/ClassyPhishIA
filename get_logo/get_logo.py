import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import os
import logging
import hashlib
import openpyxl

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

def download_image_and_compute_sha256(image_url, data_id, directory='./'):
    """Télécharger une image, la renommer avec l'ID et retourner son SHA-256."""
    try:
        # Vérifier si le répertoire existe, sinon le créer
        if not os.path.exists(directory):
            os.makedirs(directory)
        
        # Utiliser l'ID pour renommer le fichier téléchargé
        filename = os.path.join(directory, f"{data_id}.png")

        # Télécharger l'image
        response = requests.get(image_url)
        response.raise_for_status()

        # Écrire le fichier téléchargé
        with open(filename, 'wb') as file:
            file.write(response.content)

        # Calculer l'empreinte SHA-256
        sha256_hash = hashlib.sha256()

        # Ouvrir le fichier téléchargé en mode lecture binaire
        with open(filename, 'rb') as file:
            while chunk := file.read(8192):
                sha256_hash.update(chunk)

        # Retourner le SHA-256 de l'image
        return sha256_hash.hexdigest()

    except requests.RequestException as e:
        logging.error(f"Erreur lors du téléchargement de l'image : {e}")
        return None

def save_to_excel(data, filename):
    """Sauvegarder les données dans un fichier Excel."""
    # Ouvrir le fichier Excel ou le créer s'il n'existe pas
    try:
        workbook = openpyxl.load_workbook(filename)
        sheet = workbook.active
    except FileNotFoundError:
        workbook = openpyxl.Workbook()
        sheet = workbook.active

        # Ajouter les en-têtes s'il s'agit d'un nouveau fichier
        sheet.append(['ID', 'URL', 'SHA-256'])

    # Ajouter les données à la feuille
    sheet.append(data)

    # Enregistrer le fichier Excel
    workbook.save(filename)
    logging.info(f"Les données ont été sauvegardées dans le fichier Excel : {filename}")

def process_url(url, filename):
    """Traiter l'URL et enregistrer les données dans le fichier Excel spécifié."""
    logo_url = extract_logo_url(url)
    
    if logo_url:
        logging.info(f"L'URL du logo du site est : {logo_url}")

        # Calculer l'ID basé sur l'URL
        data_id = hashlib.md5(url.encode()).hexdigest()

        # Télécharger le logo et calculer le SHA-256
        sha256_hash = download_image_and_compute_sha256(logo_url, data_id)

        if sha256_hash:
            logging.info(f"SHA-256 de l'image : {sha256_hash}")

            # Sauvegarder les données dans le fichier Excel
            data = [data_id, url, sha256_hash]
            save_to_excel(data, filename)

    else:
        logging.info("Aucun logo trouvé pour ce site.")

def logo_input(url1, url2):
    """Traitement principal avec deux URL d'entrée."""
    process_url(url1, 'logo_legitime.xlsx')
    process_url(url2, 'logo_phishing.xlsx')

