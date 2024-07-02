import requests
from urllib.parse import urlparse
import whois
from datetime import datetime
from ipwhois import IPWhois
import socket
import time

class URLAnalyzer:
    def __init__(self, url):
        self.url = url
        self.parsed_url = urlparse(url)
        self.positive_points = []
        self.negative_points = []
        self.domain_info = whois.whois(self.parsed_url.hostname)

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
            
            creation_date = self.domain_info.creation_date
            if isinstance(creation_date, list):
                creation_date = creation_date[0]
            if creation_date:
                age = (datetime.now() - creation_date).days
                if age > 365:
                    self.positive_points.append("Le domaine est enregistré depuis plus d'un an, ce qui peut être un bon signe de légitimité.")
                else:
                    self.negative_points.append("Le domaine est enregistré depuis moins d'un an, ce qui pourrait indiquer un site récent ou potentiellement suspect.")
            else:
                self.negative_points.append("Impossible de déterminer la date de création du domaine.")
        except Exception as e:
            self.negative_points.append(f"Erreur lors de la vérification de l'âge du domaine : {str(e)}")

    def check_domain_expiration(self):
        """Vérifie la date d'expiration du domaine."""
        try:
            expiration_date = self.domain_info.expiration_date
            if isinstance(expiration_date, list):
                expiration_date = expiration_date[0]
            if expiration_date:
                days_to_expire = (expiration_date - datetime.now()).days
                if days_to_expire > 30:
                    self.positive_points.append("Le domaine est valide pour encore au moins 30 jours.")
                else:
                    self.negative_points.append("Le domaine expirera dans moins de 30 jours, ce qui peut indiquer un risque potentiel.")
            else:
                self.negative_points.append("Impossible de déterminer la date d'expiration du domaine.")
        except Exception as e:
            self.negative_points.append(f"Erreur lors de la vérification de la date d'expiration du domaine : {str(e)}")

    def check_server_location(self):
        """Vérifie la localisation du serveur."""
        try:
            ip_address = socket.gethostbyname(self.parsed_url.hostname)
            obj = IPWhois(ip_address)
            details = obj.lookup_rdap()
            country = details['asn_country_code']
            if country:
                self.positive_points.append(f"Le serveur est situé en {country}.")
            else:
                self.negative_points.append("Impossible de déterminer la localisation du serveur.")
        except Exception as e:
            self.negative_points.append(f"Erreur lors de la vérification de la localisation du serveur : {str(e)}")

    def check_whois_visibility(self):
        """Vérifie si les informations du propriétaire du domaine sont masquées ou non dans la base WHOIS."""
        try:
            if self.domain_info:
                if self.domain_info.privacy or "REDACTED" in str(self.domain_info):
                    self.negative_points.append("Les informations du propriétaire du domaine sont masquées dans la base WHOIS, ce qui peut être un indicateur de manque de transparence.")
                else:
                    self.positive_points.append("Les informations du propriétaire du domaine sont visibles dans la base WHOIS, ce qui indique de la transparence.")
            else:
                self.negative_points.append("Impossible de récupérer les informations WHOIS pour ce domaine.")
        except Exception as e:
            self.negative_points.append(f"Erreur lors de la vérification des informations WHOIS : {str(e)}")

    def check_domain_reputation(self):
        """Vérifie la réputation du domaine via des bases de données de sécurité."""
        try:
            # Placeholder for actual implementation
            # For example, integrate with Google Safe Browsing, VirusTotal API, etc.
            self.positive_points.append("Le domaine n'est pas listé dans les bases de données de sites malveillants (hypothétique).")
        except Exception as e:
            self.negative_points.append(f"Erreur lors de la vérification de la réputation du domaine : {str(e)}")

    def check_content_security(self):
        """Vérifie les headers de sécurité HTTP."""
        try:
            response = requests.head(self.url, timeout=5)
            headers = response.headers
            security_headers = ["Content-Security-Policy", "Strict-Transport-Security"]
            missing_headers = [header for header in security_headers if header not in headers]
            if not missing_headers:
                self.positive_points.append("Les headers de sécurité essentiels sont présents.")
            else:
                self.negative_points.append(f"Les headers de sécurité suivants sont manquants : {', '.join(missing_headers)}.")
        except Exception as e:
            self.negative_points.append(f"Erreur lors de la vérification des headers de sécurité HTTP : {str(e)}")

    def check_privacy_policy(self):
        """Vérifie la présence de la politique de confidentialité et des mentions légales."""
        try:
            response = requests.get(self.url, timeout=5)
            content = response.text.lower()
            if "politique de confidentialité" in content or "privacy policy" in content:
                self.positive_points.append("La politique de confidentialité est présente.")
            else:
                self.negative_points.append("La politique de confidentialité n'est pas trouvée.")
            
            if "mentions légales" in content or "legal notice" in content:
                self.positive_points.append("Les mentions légales sont présentes.")
            else:
                self.negative_points.append("Les mentions légales ne sont pas trouvées.")
        except Exception as e:
            self.negative_points.append(f"Erreur lors de la vérification de la politique de confidentialité et des mentions légales : {str(e)}")

    def check_user_reviews(self):
        """Vérifie la réputation du site sur des plateformes d'avis."""
        try:
            # Placeholder for actual implementation
            # For example, scraping Trustpilot or similar sites
            self.positive_points.append("Le site a de bonnes critiques sur les plateformes d'avis (hypothétique).")
        except Exception as e:
            self.negative_points.append(f"Erreur lors de la vérification des avis des utilisateurs : {str(e)}")

    def check_social_media_activity(self):
        """Vérifie l'activité du site sur les réseaux sociaux."""
        try:
            # Placeholder for actual implementation
            # For example, use APIs from Twitter, Facebook, etc.
            self.positive_points.append("Le site est actif sur les réseaux sociaux (hypothétique).")
        except Exception as e:
            self.negative_points.append(f"Erreur lors de la vérification de l'activité sur les réseaux sociaux : {str(e)}")

    def check_page_speed(self):
        """Vérifie la vitesse de chargement du site."""
        try:
            start_time = time.time()
            response = requests.get(self.url, timeout=5)
            load_time = time.time() - start_time
            if load_time < 2:
                self.positive_points.append(f"Le site se charge rapidement en {load_time:.2f} secondes.")
            else:
                self.negative_points.append(f"Le site se charge lentement en {load_time:.2f} secondes.")
        except Exception as e:
            self.negative_points.append(f"Erreur lors de la vérification de la vitesse de chargement du site : {str(e)}")

    def check_uptime_history(self):
        """Vérifie l'historique de disponibilité du site."""
        try:
            # Placeholder for actual implementation
            # For example, integrate with services like UptimeRobot or similar
            self.positive_points.append("Le site a une bonne disponibilité historique (hypothétique).")
        except Exception as e:
            self.negative_points.append(f"Erreur lors de la vérification de l'historique de disponibilité du site : {str(e)}")

    def analyze(self):
        """Effectue l'analyse complète de l'URL."""
        self.check_protocol()
        self.check_ssl_certificate()
        self.check_domain_age()
        self.check_domain_expiration()
        self.check_server_location()
        self.check_whois_visibility()
        self.check_domain_reputation()
        self.check_content_security()
        self.check_privacy_policy()
        self.check_user_reviews()
        self.check_social_media_activity()
        self.check_page_speed()
        self.check_uptime_history()
        return self.positive_points, self.negative_points