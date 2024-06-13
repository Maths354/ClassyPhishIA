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

class ExtractCert():

    def __init__(self, url, official_sites):
        assert isinstance(url, str)
        self.url=url.split("/")[2]
        self.official_sites=official_sites
        self._port=443
        self._score=0
        self._cert_info_raw=self.__get_cert()
        self._cert_info_clean=list()
        self._top_company=list()

    def __get_cert(self):
        try:
            context = ssl.create_default_context()
            with socket.create_connection((self.url, self._port)) as sock:
                with context.wrap_socket(sock, server_hostname=self.url) as ssock:
                    cert = ssock.getpeercert()
                    return cert
        except:
            return dict()
    
    def __compare_subjects(self,offical_subject, phishing_subject):
        fields = ['countryName', 'stateOrProvinceName', 'localityName', 'organizationName', 'commonName']
    
        similarity_score = 0
        comparison_result = {}
        
        dict1 = {field[0][0]: field[0][1] for field in offical_subject}
        dict2 = {field[0][0]: field[0][1] for field in phishing_subject}
        
        for field in fields:
            value1 = dict1.get(field)
            value2 = dict2.get(field)
            comparison_result[field] = (value1, value2, value1 == value2)
            if value1 == value2:
                similarity_score += 1
        
        return comparison_result, similarity_score

    def __manip_data(self):
        #check if there is data in phish cert
        if not self._cert_info_raw:
            self._score=0
            return "Pas de donnée à propos du certificat, cela peut être dû par différents phénomènes (Site en HTTP, Site n'utilisant pas le port 443)"
        
        #get phish cert creation
        cert_notBefore = datetime.strptime(self._cert_info_raw["notBefore"], "%b %d %H:%M:%S %Y GMT")
        now = datetime.now()
        diff = now - cert_notBefore
        self._cert_info_clean.append(f"Le certificat a été émis il y a {diff}")

        #compare certs
        best_score = -1

        for company in self.official_sites:
            company_cert = ast.literal_eval(company["certificate"])

            subject_comparison, subject_score = self.__compare_subjects(company_cert["subject"], self._cert_info_raw["subject"])
            if subject_score > best_score:
                best_score = subject_score/5
                best_comparison = subject_comparison
                if best_score > self._score:
                    self._score=best_score
                    self._top_company=[company["id"],company["url"]]

            if self._cert_info_raw["serialNumber"] == company_cert["serialNumber"]:
                self._score=1

        # Stocker les informations dans des variables
        official_details = ""
        phish_details = ""

        for field, (official, phish, is_same) in best_comparison.items():
            official_details += f"{field}: {official}\n"
            phish_details += f"{field}: {phish}\n"
        self._cert_info_clean.append(official_details)
        self._cert_info_clean.append(phish_details)



            

    def get_cert_info(self):
        """
        If the variable self._cert_info is empty {}, it can be due by two things : 
            - HTTP protocol (no cert available)
            - Website not hosted on port 443
        """
        self.__manip_data()
        return [self._cert_info_clean, self._cert_info_raw], self._score, self._top_company