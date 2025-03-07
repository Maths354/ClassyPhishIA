"""
    Template of self._cert_info variable
    In the get_cert_info() function, you have to add in parameter one of the key below (subject, version, ...)

    {'subject': ((('commonName', 'domain.dns'),),), 
    'issuer': ((('countryName', 'FR'),), (('organizationName', 'GlobalSign nv-sa'),), (('commonName', 'GlobalSign Atlas R3 DV TLS CA 2023 Q3'),)), 
    'version': 3, 
    'serialNumber': 'XXXXXXXXXXXXXXXXXXX', 
    'notBefore': 'Sep  1 21:33:12 2023 GMT', 
    'notAfter': 'Oct  2 21:33:11 2024 GMT', 
    'subjectAltName': (('DNS', 'domain.dns'), ('DNS', '*.domain.dns')), 
    'OCSP': ('my_oscp_url',), 
    'caIssuers': ('my_crt_url',), 
    'crlDistributionPoints': ('my_crl_url',)}
"""


import ssl
import socket
import ast
from datetime import datetime
from urllib.parse import urlparse
from analyse_phishing.extract_certificat.sslAnalyzer import SSLAnalyzer

class ExtractCert():

    def __init__(self, url, official_sites):
        assert isinstance(url, str)
        self.full_url = url
        self.url = url.split("/")[2]  # Extraction de l'URL de base
        self.official_sites = official_sites  # Liste des sites officiels pour la comparaison
        self._port = int()  # Initialisation du port
        self._score = 0  # Score d'évaluation de la similarité
        self._cert_info_raw = self.__get_cert()  # Informations brutes du certificat
        self._cert_info_clean = list()  # Informations nettoyées du certificat
        self._top_company = list()  # Informations sur l'entreprise la mieux classée

    def __get_port_from_url(self):
        # Extraction du port à partir de l'URL
        parsed_url = urlparse(self.full_url)
        self._port = parsed_url.port

        if self._port is None:
            if parsed_url.scheme == 'http':
                self._port = 80
            elif parsed_url.scheme == 'https':
                self._port = 443

    def __get_cert(self):
        # Récupération du certificat SSL
        self.__get_port_from_url()
        try:
            context = ssl.create_default_context()
            with socket.create_connection((self.url, self._port)) as sock:
                with context.wrap_socket(sock, server_hostname=self.url) as ssock:
                    cert = ssock.getpeercert()
                    return cert
                    
        except:
            return dict()  # Retourne un dictionnaire vide en cas d'échec

    def __compare_subjects(self, official_subject, phishing_subject):
        # Comparaison des sujets des certificats
        fields = ['countryName', 'stateOrProvinceName', 'localityName', 'organizationName', 'commonName']
    
        similarity_score = 0
        comparison_result = {}
        
        dict_official = {field[0][0]: field[0][1] for field in official_subject}
        dict_phishing = {field[0][0]: field[0][1] for field in phishing_subject}
        
        for field in fields:
            value_official = dict_official.get(field)
            value_phishing = dict_phishing.get(field)
            comparison_result[field] = (value_official, value_phishing, value_official == value_phishing)
            if value_phishing is not None:
                if value_official == value_phishing:
                    similarity_score += 1
                    if field == "commonName":
                        similarity_score = 5  # Score maximal si le nom commun est identique
            
        return comparison_result, similarity_score

    def __manip_data(self):
        # Manipulation des données du certificat
        if not self._cert_info_raw:
            self._score = 0
            return "Pas de donnée à propos du certificat, cela peut être dû par différents phénomènes (Site en HTTP, Site n'utilisant pas le port 443)"
        
        # Calcul de la date de création du certificat phishing
        cert_notBefore = datetime.strptime(self._cert_info_raw["notBefore"], "%b %d %H:%M:%S %Y GMT")
        now = datetime.now()
        diff = now - cert_notBefore
        self._cert_info_clean.append(f"Le certificat a été émis il y a {diff}")

        # Comparaison avec les certificats officiels
        best_score = -1

        for company in self.official_sites:
            company_cert = ast.literal_eval(company["certificate"])
            
            if 'subject' in company_cert.keys():
                subject_comparison, subject_score = self.__compare_subjects(company_cert["subject"], self._cert_info_raw["subject"])
                if subject_score > best_score:
                    best_score = subject_score / 5
                    best_comparison = subject_comparison
                    if best_score > self._score:
                        self._score = best_score
                        self._top_company = [company["id"], company["url"]]
                        
            if 'serialNumber' in company_cert.keys():
                if self._cert_info_raw["serialNumber"] == company_cert["serialNumber"]:
                    self._score = 1

        # Stockage des détails de comparaison dans des variables
        official_details = ""
        phish_details = ""

        for field, (official, phish, is_same) in best_comparison.items():
            official_details += f"{field}: {official}\n"
            phish_details += f"{field}: {phish}\n"
        
        self._cert_info_clean.append(official_details)
        self._cert_info_clean.append(phish_details)

    def get_cert_info(self):
        """
        Si la variable self._cert_info est vide {}, cela peut être dû à deux raisons : 
            - Protocole HTTP (pas de certificat disponible)
            - Site non hébergé sur le port 443
        """
        if "https" in self.full_url:
            self.__manip_data()
        else:
            self._cert_info_clean = ""
            self._top_company = [99999999, ""]  # Valeur par défaut si le site n'est pas HTTPS
            
        analyseCert = SSLAnalyzer(self.full_url)
        dataCert = analyseCert.analyze_cert()

        print(dataCert)
        if dataCert["free_hosting_domain"] != None:
            self._score = 0.00
        
        return [self._cert_info_clean, self._cert_info_raw], self._score, self._top_company, dataCert
