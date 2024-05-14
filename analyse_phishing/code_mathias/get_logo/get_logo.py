import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import os
import logging
import hashlib
import cv2
import numpy as np
from skimage.metrics import structural_similarity as ssim
from data_saver.sauvegarde import is_id_present, save_to_excel  # Importer les fonctions de sauvegarde.py

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
        return filename, sha256_hash.hexdigest()

    except requests.RequestException as e:
        logging.error(f"Erreur lors du téléchargement de l'image : {e}")
        return None, None

def process_url(url, filename):
    """Traiter l'URL et enregistrer les données dans le fichier Excel spécifié."""
    logo_url = extract_logo_url(url)
    
    if logo_url:
        logging.info(f"L'URL du logo du site est : {logo_url}")

        # Calculer l'ID basé sur l'URL
        data_id = hashlib.md5(url.encode()).hexdigest()

        # Télécharger le logo et calculer le SHA-256
        image_path, sha256_hash = download_image_and_compute_sha256(logo_url, data_id)

        if sha256_hash:
            logging.info(f"SHA-256 de l'image : {sha256_hash}")

            # Sauvegarder les données dans le fichier Excel, y compris les balises
            save_to_excel([data_id, url, sha256_hash, ''], filename)

        # Retourner le chemin du fichier image téléchargé
        return image_path

    else:
        logging.info("Aucun logo trouvé pour ce site.")
        return None

def load_image(file_path):
    """Charge une image et la convertit en niveau de gris."""
    image = cv2.imread(file_path)
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    return gray_image

def resize_image(image, size):
    """Redimensionne une image à la taille spécifiée."""
    resized_image = cv2.resize(image, size, interpolation=cv2.INTER_AREA)
    return resized_image

def compare_images(image1, image2):
    """Compare deux images et retourne un score de similarité entre 0 et 1."""
    size = (min(image1.shape[1], image2.shape[1]), min(image1.shape[0], image2.shape[0]))
    
    # Redimensionner les images à la même taille
    resized_image1 = resize_image(image1, size)
    resized_image2 = resize_image(image2, size)
    
    # Calcul de la similarité structurelle (SSIM)
    similarity, _ = ssim(resized_image1, resized_image2, full=True)
    
    return similarity

def logo_input(url1, url2):
    """Traitement principal avec deux URL d'entrée et les balises HTML des URL."""
    # Processus pour l'URL 1
    image_path1 = process_url(url1, 'logo_legitime.xlsx')
    
    # Processus pour l'URL 2
    image_path2 = process_url(url2, 'logo_phishing.xlsx')
    
    # Si les chemins d'image sont valides, comparez les images
    if image_path1 and image_path2:
        # Charger les images
        image1 = load_image(image_path1)
        image2 = load_image(image_path2)

        # Comparez les images et obtenez un score de similarité
        similarity_score = compare_images(image1, image2)
        
        # Afficher le score de similarité
        print(f"Score de ressemblance entre les images : {similarity_score:.2f}")
