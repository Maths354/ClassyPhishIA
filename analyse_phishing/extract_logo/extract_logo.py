import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import os
import logging
import hashlib
import cv2
import numpy as np
from skimage.metrics import structural_similarity as ssim

class ExtractLOGO:
    def __init__(self, url=None):
        self.url = url

    @staticmethod
    def extract_logo_url(url):
        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, 'html.parser')

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

            logo_img = soup.find('img', {'class': 'logo'}) or soup.find('img', {'id': 'logo'})
            if logo_img:
                logo_url = logo_img['src']
                if not logo_url.startswith('http'):
                    logo_url = urljoin(url, logo_url)
                return logo_url

            favicon_url = urljoin(url, 'favicon.ico')
            response = requests.get(favicon_url, timeout=10)
            if response.status_code == 200:
                return favicon_url

            return None
        except requests.RequestException as e:
            logging.error(f"Erreur lors de l'extraction du logo : {e}")
            return None

    @staticmethod
    def download_image_and_compute_sha256(image_url, data_id, directory='./'):
        try:
            if not os.path.exists(directory):
                os.makedirs(directory)

            filename = os.path.join(directory, f"{data_id}.png")

            response = requests.get(image_url)
            response.raise_for_status()

            with open(filename, 'wb') as file:
                file.write(response.content)

            sha256_hash = hashlib.sha256()

            with open(filename, 'rb') as file:
                while chunk := file.read(8192):
                    sha256_hash.update(chunk)

            return filename, sha256_hash.hexdigest()

        except requests.RequestException as e:
            logging.error(f"Erreur lors du téléchargement de l'image : {e}")
            return None, None

    @staticmethod
    def process_url(url):
        logo_url = ExtractLOGO.extract_logo_url(url)

        if logo_url:
            logging.info(f"L'URL du logo du site est : {logo_url}")
            data_id = hashlib.md5(url.encode()).hexdigest()
            image_path, sha256_hash = ExtractLOGO.download_image_and_compute_sha256(logo_url, data_id)

            if sha256_hash:
                logging.info(f"SHA-256 de l'image : {sha256_hash}")
            return image_path, sha256_hash
        else:
            logging.info("Aucun logo trouvé pour ce site.")
            return None, None

    @staticmethod
    def load_image(file_path):
        image = cv2.imread(file_path)
        gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        return gray_image

    @staticmethod
    def resize_image(image, size):
        resized_image = cv2.resize(image, size, interpolation=cv2.INTER_AREA)
        return resized_image

    @staticmethod
    def compare_images(image1, image2):
        size = (min(image1.shape[1], image2.shape[1]), min(image1.shape[0], image2.shape[0]))
        resized_image1 = ExtractLOGO.resize_image(image1, size)
        resized_image2 = ExtractLOGO.resize_image(image2, size)
        similarity, _ = ssim(resized_image1, resized_image2, full=True)
        return similarity

    @classmethod
    def logo_info(cls, url1, url2):
        image_path1, hash1 = cls.process_url(url1)
        image_path2, hash2 = cls.process_url(url2)

        if image_path1 and image_path2:
            image1 = cls.load_image(image_path1)
            image2 = cls.load_image(image_path2)
            similarity_score = cls.compare_images(image1, image2)
            logging.info(f"Score de ressemblance entre les images : {similarity_score:.2f}")
            logging.info(f"SHA-256 de l'image 1 : {hash1}")
            logging.info(f"SHA-256 de l'image 2 : {hash2}")

        return hash1

# if __name__ == "__main__":
#     url1 = "https://www.orange.fr/portail"
#     url2 = "https://www.keraunos.org/"
#     ExtractLOGO.logo_info(url1, url2)
