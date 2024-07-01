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

    def __init__(self, url):
        assert isinstance(url, str)
        self.url=url.split("/")[2]
        self._port=443
        self._score=0
        self._cert_info_raw=self.__get_cert()

    def __get_cert(self):
        try:
            context = ssl.create_default_context()
            with socket.create_connection((self.url, self._port)) as sock:
                with context.wrap_socket(sock, server_hostname=self.url) as ssock:
                    cert = ssock.getpeercert()
                    return cert
        except:
            return dict()
            

    def get_cert_info(self):
        """
        If the variable self._cert_info is empty {}, it can be due by two things : 
            - HTTP protocol (no cert available)
            - Website not hosted on port 443
        """
        return self._cert_info_raw