import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import logging
from skimage.metrics import structural_similarity as ssim # type: ignore
import cv2 # type: ignore
import numpy as np
from io import BytesIO
from PIL import Image
import hashlib
import os

class ExtractLOGO:
    def __init__(self, url, official_sites):
        self.url = url
        self.official_sites = official_sites

    def extract_logo_url(self, url):
        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                              'AppleWebKit/537.36 (KHTML, like Gecko) '
                              'Chrome/58.0.3029.110 Safari/537.3'
            }
            # Envoie une requête HTTP GET à l'URL spécifiée avec les en-têtes spécifiés
            response = requests.get(url, headers=headers, timeout=10)
            # Vérifie si la requête a réussi
            response.raise_for_status()
            # Analyse le contenu HTML de la page
            soup = BeautifulSoup(response.text, 'html.parser')

            # Types d'icônes à rechercher dans la page HTML
            icon_types = [
                ('link', 'rel', 'icon'),
                ('link', 'rel', 'shortcut icon'),
                ('link', 'rel', 'apple-touch-icon'),
                ('link', 'rel', 'icon', 'image/x-icon'),
                ('link', 'rel', 'icon', 'image/png'),
                ('link', 'rel', 'icon', 'image/jpeg'),
                ('link', 'rel', 'icon', 'image/svg+xml'),
                ('link', 'rel', 'icon', 'image/webp'),
                ('img', 'class', 'logo'),
                ('img', 'id', 'logo')
            ]

            # Boucle sur les types d'icônes pour les rechercher dans le contenu HTML
            for tag, attribute, value, *optional_type in icon_types:
                if optional_type:
                    element = soup.find(tag, {attribute: value}, type=optional_type[0])
                else:
                    element = soup.find(tag, {attribute: value})
                if element:
                    logo_url = element.get('href') or element.get('src')
                    # Complète l'URL du logo si nécessaire
                    if logo_url and not logo_url.startswith('http'):
                        logo_url = urljoin(url, logo_url)
                    if logo_url.lower().endswith(('png', 'jpg', 'jpeg', 'ico', 'svg', 'webp')):
                        return logo_url

            # Tentative de récupération du favicon comme solution de secours
            favicon_url = urljoin(url, 'favicon.ico')
            response = requests.get(favicon_url, headers=headers, timeout=10)
            if response.status_code == 200:
                return favicon_url

            return None
        except requests.RequestException as e:
            logging.error(f"Erreur lors de l'extraction du logo: {e}")
            return None

    def download_image_and_compute_sha256(self, url):
        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                              'AppleWebKit/537.36 (KHTML, like Gecko) '
                              'Chrome/58.0.3029.110 Safari/537.3'
            }
            # Télécharge l'image à partir de l'URL spécifiée
            response = requests.get(url, headers=headers, timeout=10)
            # Vérifie si la requête a réussi
            response.raise_for_status()
            # Ouvre l'image et la convertit en format compatible avec OpenCV
            image = Image.open(BytesIO(response.content))
            return cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
        except requests.RequestException as e:
            logging.error(f"Erreur lors du téléchargement de l'image: {e}")
            return None

    def load_local_image_and_compute_sha256(self, file_path):
        try:
            # Ouvre et lit le fichier image local
            with open(file_path, 'rb') as f:
                image_data = f.read()
            # Charge l'image et la convertit en format compatible avec OpenCV
            image = Image.open(BytesIO(image_data))
            return cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
        except Exception as e:
            logging.error(f"Erreur lors du chargement de l'image: {e}")
            return None

    def resize_image(self, image, size):
        # Redimensionne l'image à la taille spécifiée
        return cv2.resize(image, size, interpolation=cv2.INTER_AREA)

    def compare_images(self, image_legitime, image_phishing):
        if image_legitime is None or image_phishing is None:
            logging.error("Une ou les deux images sont nulles.")
            return 0.0  # ou un score de similarité par défaut

        # Redimensionne les deux images à 32x32 pour la comparaison
        size = (32, 32)

        resized_image_legitime = self.resize_image(image_legitime, size)
        resized_image_phishing = self.resize_image(image_phishing, size)

        if resized_image_legitime is None or resized_image_phishing is None:
            logging.error("Erreur lors du redimensionnement d'une ou des deux images.")
            return 0.0  # ou un score de similarité par défaut

        # Continue avec la comparaison des images
        gray_image_legitime = cv2.cvtColor(resized_image_legitime, cv2.COLOR_BGR2GRAY)
        gray_image_phishing = cv2.cvtColor(resized_image_phishing, cv2.COLOR_BGR2GRAY)

        # Normalise et compare les images en utilisant SSIM ou d'autres méthodes
        similarity, _ = ssim(gray_image_legitime, gray_image_phishing, full=True)
        return similarity

    def logo_info(self):
        similarity_score = None
        top_score = -1
        url_phishing = self.url

        # Extrait l'URL du logo à partir du site de phishing
        logo_url_phishing = self.extract_logo_url(url_phishing)

        # Télécharge l'image du site de phishing
        try:
            image_phishing = self.download_image_and_compute_sha256(logo_url_phishing)
        except:
            image_phishing = None
        if image_phishing is not None:
            for company in self.official_sites:
                if "None" not in company["logo"]:
                    try:
                        # Charge l'image légitime depuis un fichier local
                        image_legitime = self.load_local_image_and_compute_sha256(f"analyse_phishing/extract_logo/images/{company['logo']}.png")

                        
                        # Compare les images et calcule un score de similarité
                        similarity_score = self.compare_images(image_legitime, image_phishing)

                        if similarity_score > top_score:
                            top_score = similarity_score
                            top_company = [company["id"], company["url"]]
                            
                    except:
                        pass
            # Extrait l'URL du logo de l'entreprise avec le score le plus élevé
            top_logo_url = self.extract_logo_url(top_company[1])
            return [top_logo_url, logo_url_phishing], top_score, top_company
        else:
            return ["Pas de correspondance", "Aucun logo trouvé sur le site de phishing"], 0.0, dict()
