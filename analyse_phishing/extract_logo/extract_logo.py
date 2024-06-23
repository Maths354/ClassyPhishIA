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
        self.official_sites=official_sites

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

    def save_image_with_sha256_name(self, image, sha256, directory='images', size=(32, 32)):
        if not os.path.exists(directory):
            os.makedirs(directory)

        resized_image = self.resize_image(image, size)
        save_path = os.path.join(directory, f"{sha256}.png")
        cv2.imwrite(save_path, resized_image)
        logging.info(f"Saved image at: {save_path}")
        return save_path

    def resize_image(self, image, size):
        return cv2.resize(image, size, interpolation=cv2.INTER_AREA)

    def compare_images(self, image_legitime, image_phishing):
        if image_legitime is None or image_phishing is None:
            logging.error("One or both images are None.")
            return 0.0  # or some default similarity score

        # Resize both images to 32x32 for comparison
        size = (32, 32)

        resized_image_legitime = self.resize_image(image_legitime, size)
        resized_image_phishing = self.resize_image(image_phishing, size)

        if resized_image_legitime is None or resized_image_phishing is None:
            logging.error("Error resizing one or both images.")
            return 0.0  # or some default similarity score

        # Continue with image comparison
        gray_image_legitime = cv2.cvtColor(resized_image_legitime, cv2.COLOR_BGR2GRAY)
        gray_image_phishing = cv2.cvtColor(resized_image_phishing, cv2.COLOR_BGR2GRAY)

        # Normalize and compare images using SSIM or other methods
        similarity, _ = ssim(gray_image_legitime, gray_image_phishing, full=True)
        return similarity

    def logo_info(self):
        similarity_score = None
        top_score=-1
        top_company=""
        url_phishing = self.url

        logo_url_phishing = self.extract_logo_url(url_phishing)

        if logo_url_phishing != None:
            for company in self.official_sites:
                url_legitime=company["url"]
                logo_url_legitime = self.extract_logo_url(url_legitime)

                image_legitime, hash_legitime = self.download_image_and_compute_sha256(logo_url_legitime)
                image_phishing, hash_phishing = self.download_image_and_compute_sha256(logo_url_phishing)

                if image_legitime is not None and hash_legitime is not None:
                    self.save_image_with_sha256_name(image_legitime, hash_legitime, size=(32, 32))
                
                similarity_score = self.compare_images(image_legitime, image_phishing)

                if similarity_score>top_score:
                    top_score = similarity_score
                    top_company = [company["id"], company["url"]]
            return logo_url_legitime, top_score, top_company
        else:
            return dict(), dict(), dict()

