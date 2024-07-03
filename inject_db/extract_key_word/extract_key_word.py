from urllib.parse import urlparse
import re

class ExtractKeyWord:

    def __init__(self, url):
        self.url = url

    def extract_domain(self):
        # Parse l'URL pour obtenir le netloc
        parsed_url = urlparse(self.url)
        netloc = parsed_url.netloc
        # Enlève le sous-domaine et le suffixe, ne garde que le domaine principal
        pattern = r"(?:www\.)?([^.]+)\.\w+$"
        match = re.search(pattern, netloc)
        if match:
            return match.group(1)
        return None