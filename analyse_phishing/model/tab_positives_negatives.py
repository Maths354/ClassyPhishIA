# url_analyzer.py

import requests
from urllib.parse import urlparse
import whois
from datetime import datetime, timedelta

class URLAnalyzer:
    def __init__(self, url):
        self.url = url
        self.parsed_url = urlparse(url)
        self.positive_points = []
        self.negative_points = []

    def check_protocol(self):
        """Vérifie si l'URL utilise HTTPS ou HTTP."""
        if self.parsed_url.scheme == "https":
            self.positive_points.append("Le site utilise HTTPS, ce qui est un bon indicateur de sécurité.")
        else:
            self.negative_points.append("Le site utilise HTTP, ce qui n'est pas sécurisé.")

    def check_ssl_certificate(self):
        """Vérifie la validité du certificat SSL de l'URL."""
        try:
            response = requests.get(self.url, timeout=5)
            if response.ok:
                self.positive_points.append("Le site répond avec succès et semble actif.")
            else:
                self.negative_points.append(f"Le site a répondu avec un statut non favorable : {response.status_code}.")
        except requests.exceptions.SSLError:
            self.negative_points.append("Le certificat SSL du site n'est pas valide.")
        except requests.exceptions.RequestException as e:
            self.negative_points.append(f"Le site n'a pas pu être atteint : {str(e)}.")

    def check_domain_age(self):
        """Vérifie l'âge du domaine."""
        try:
            domain_info = whois.whois(self.parsed_url.hostname)
            creation_date = domain_info.creation_date
            if isinstance(creation_date, list):
                creation_date = creation_date[0]
            if creation_date:
                age = (datetime.now() - creation_date).days
                if age > 365:  # Plus d'un an
                    self.positive_points.append("Le domaine est enregistré depuis plus d'un an, ce qui peut être un bon signe de légitimité.")
                else:
                    self.negative_points.append("Le domaine est enregistré depuis moins d'un an, ce qui pourrait indiquer un site récent ou potentiellement suspect.")
            else:
                self.negative_points.append("Impossible de déterminer la date de création du domaine.")
        except Exception as e:
            self.negative_points.append(f"Erreur lors de la vérification de l'âge du domaine : {str(e)}")

    def check_whois_visibility(self):
        """Vérifie si les informations du propriétaire du domaine sont masquées ou non dans la base WHOIS."""
        try:
            domain_info = whois.whois(self.parsed_url.hostname)
            if domain_info:
                if domain_info.privacy or "REDACTED" in str(domain_info):
                    self.negative_points.append("Les informations du propriétaire du domaine sont masquées dans la base WHOIS, ce qui peut être un indicateur de manque de transparence.")
                else:
                    self.positive_points.append("Les informations du propriétaire du domaine sont visibles dans la base WHOIS, ce qui indique de la transparence.")
            else:
                self.negative_points.append("Impossible de récupérer les informations WHOIS pour ce domaine.")
        except Exception as e:
            self.negative_points.append(f"Erreur lors de la vérification des informations WHOIS : {str(e)}")

    def analyze(self):
        """Effectue l'analyse complète de l'URL."""
        self.check_protocol()
        self.check_ssl_certificate()
        self.check_domain_age()
        self.check_whois_visibility()
        return self.positive_points, self.negative_points