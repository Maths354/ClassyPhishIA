import string
import requests
from bs4 import BeautifulSoup
import re

class ExtractKeyWord:

    def __init__(self, url):
        self.url = url.split("/")[2]

    def extract_domain(self):
        # Utilise une expression régulière pour extraire le nom de domaine
        pattern = r"(?:www\.)?([^.]+(?:-[^.]+)*)\.\w+"
        match = re.search(pattern, self.url)
        if match:
            return match.group(1)
        return None