import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import logging
from skimage.metrics import structural_similarity as ssim
import cv2
import numpy as np
from io import BytesIO
from PIL import Image
import hashlib

class ExtractLOGO:
    def __init__(self, url=None):
        self.url = url

    def extract_logo_url(self, url):
        try:
            headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}
            response = requests.get(url, headers=headers, timeout=10)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, 'html.parser')

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

            for tag, attribute, value, *optional_type in icon_types:
                if optional_type:
                    element = soup.find(tag, {attribute: value}, type=optional_type[0])
                else:
                    element = soup.find(tag, {attribute: value})
                if element:
                    logo_url = element.get('href') or element.get('src')
                    if logo_url and not logo_url.startswith('http'):
                        logo_url = urljoin(url, logo_url)
                    return logo_url

            favicon_url = urljoin(url, 'favicon.ico')
            response = requests.get(favicon_url, headers=headers, timeout=10)
            if response.status_code == 200:
                return favicon_url

            return None
        except requests.RequestException as e:
            logging.error(f"Erreur lors de l'extraction du logo : {e}")
            return None

    def download_image_and_compute_sha256(self, url):
        try:
            headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}
            response = requests.get(url, headers=headers, timeout=10)
            response.raise_for_status()
            image = Image.open(BytesIO(response.content))
            return cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR), hashlib.sha256(response.content).hexdigest()
        except requests.RequestException as e:
            logging.error(f"Erreur lors du téléchargement de l'image : {e}")
            return None, None

    def load_image(self, file_path):
        try:
            image = cv2.imread(file_path)
            if image is None:
                logging.error(f"Impossible de charger l'image à partir de {file_path}")
                return None
            gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            return gray_image, None
        except Exception as e:
            logging.error(f"Erreur lors du chargement de l'image : {e}")
            return None, None

    def resize_image(self, image, size):
        return cv2.resize(image, size, interpolation=cv2.INTER_AREA)

    def compare_images(self, image_legitime, image_phishing):
        size = (min(image_legitime.shape[1], image_phishing.shape[1]), min(image_legitime.shape[0], image_phishing.shape[0]))
        resized_image_legitime = self.resize_image(image_legitime, size)
        resized_image_phishing = self.resize_image(image_phishing, size)
        similarity, _ = ssim(resized_image_legitime, resized_image_phishing, full=True)
        return similarity

    def logo_info(self, url_legitime="https://www.orange.fr"):
        similarity_score = None
        url_phishing = self.url
        
        logo_url_legitime = self.extract_logo_url(url_legitime)
        logo_url_phishing = self.extract_logo_url(url_phishing)

        image_legitime, hash_legitime = self.download_image_and_compute_sha256(logo_url_legitime)
        image_phishing, hash_phishing = self.download_image_and_compute_sha256(logo_url_phishing)

        gray_image_legitime = cv2.cvtColor(image_legitime, cv2.COLOR_BGR2GRAY)
        gray_image_phishing = cv2.cvtColor(image_phishing, cv2.COLOR_BGR2GRAY)

        similarity_score = self.compare_images(gray_image_legitime, gray_image_phishing)
        return hash_phishing, similarity_score