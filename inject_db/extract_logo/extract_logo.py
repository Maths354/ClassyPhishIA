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
    def __init__(self, url):
        self.url = url

    def extract_logo_url(self, url):
        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                              'AppleWebKit/537.36 (KHTML, like Gecko) '
                              'Chrome/58.0.3029.110 Safari/537.3'
            }
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
                    if logo_url.lower().endswith(('png', 'jpg', 'jpeg', 'ico', 'svg', 'webp')):
                        return logo_url

            # Attempt to retrieve favicon as a fallback
            favicon_url = urljoin(url, 'favicon.ico')
            response = requests.get(favicon_url, headers=headers, timeout=10)
            if response.status_code == 200:
                return favicon_url

            return None
        except requests.RequestException as e:
            logging.error(f"Error while extracting the logo: {e}")
            return None

    def download_image_and_compute_sha256(self, url):
        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                              'AppleWebKit/537.36 (KHTML, like Gecko) '
                              'Chrome/58.0.3029.110 Safari/537.3'
            }
            response = requests.get(url, headers=headers, timeout=10)
            response.raise_for_status()
            image = Image.open(BytesIO(response.content))
            return cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR), hashlib.sha256(response.content).hexdigest()
        except requests.RequestException as e:
            logging.error(f"Error while downloading the image: {e}")
            return None, None

    def save_image_with_sha256_name(self, image, sha256, directory='analyse_phishing/extract_logo/images', size=(32, 32)):
        if not os.path.exists(directory):
            os.makedirs(directory)

        resized_image = self.resize_image(image, size)
        save_path = os.path.join(directory, f"{sha256}.png")
        cv2.imwrite(save_path, resized_image)
        return save_path

    def resize_image(self, image, size):
        return cv2.resize(image, size, interpolation=cv2.INTER_AREA)

    def logo_info(self):
        logo_url = self.extract_logo_url(self.url)

        if logo_url != None:
            image_legitime, hash_legitime = self.download_image_and_compute_sha256(logo_url)

            if image_legitime is not None and hash_legitime is not None:
                self.save_image_with_sha256_name(image_legitime, hash_legitime, size=(32, 32))
                
            return hash_legitime
        else:
            return None
