import ssl
import socket
import requests
from urllib.parse import urlparse
from datetime import datetime, timezone
from cryptography import x509
from cryptography.hazmat.backends import default_backend
from cryptography.x509.oid import NameOID, ExtensionOID

class SSLAnalyzer:

    def __init__(self, url):
        self.url = url
        self.parsed_url = urlparse(url)
        if not self.parsed_url.scheme:
            self.url = "https://" + url
            self.parsed_url = urlparse(self.url)
        self.hostname = self.parsed_url.netloc
        self.cert = None
        self.analysis = None
        self.legitimacy_score = 0
        self.reasons = []
        self.free_hosting_domain = None

    def analyze_cert(self):
        try:
            self.cert = self._get_certificate()
            self.analysis = self._analyze_certificate()
            self._assess_legitimacy()
            return self._get_results()
        except Exception as e:
            return {"error": str(e)}

    def _get_certificate(self):
        context = ssl.create_default_context()
        with socket.create_connection((self.hostname, 443)) as sock:
            with context.wrap_socket(sock, server_hostname=self.hostname) as secure_sock:
                der_cert = secure_sock.getpeercert(binary_form=True)
        return x509.load_der_x509_certificate(der_cert, default_backend())

    def _determine_cert_type(self):
        subject = self.cert.subject
        
        ev_oids = [NameOID.BUSINESS_CATEGORY, NameOID.JURISDICTION_COUNTRY_NAME, NameOID.SERIAL_NUMBER]
        is_ev = all(subject.get_attributes_for_oid(oid) for oid in ev_oids)
        
        is_ov = bool(subject.get_attributes_for_oid(NameOID.ORGANIZATION_NAME))
        
        if is_ev:
            return "EV (Validation Étendue)"
        elif is_ov:
            return "OV (Validation d'Organisation)"
        else:
            return "DV (Validation de Domaine)"

    def _analyze_certificate(self):
        cert_type = self._determine_cert_type()
        issuer = self.cert.issuer.get_attributes_for_oid(NameOID.COMMON_NAME)[0].value
        valid_from = self.cert.not_valid_before_utc
        valid_until = self.cert.not_valid_after_utc
        current_time = datetime.now(timezone.utc)
        
        return {
            "certificate_type": cert_type,
            "issuer": issuer,
            "valid_from": valid_from,
            "valid_until": valid_until,
            "is_expired": current_time > valid_until,
            "days_until_expiry": (valid_until - current_time).days
        }

    def _assess_legitimacy(self):
        self._check_certificate_type()
        self._check_expiration()
        self._check_issuer()
        self._check_free_hosting()
        
        max_score = 10
        self.legitimacy_score = max(0, min(100, (self.legitimacy_score / max_score) * 100))

    def _check_certificate_type(self):
        if self.analysis["certificate_type"] == "EV (Validation Étendue)":
            self.legitimacy_score += 3
            self.reasons.append("Certificat EV assure une haute assurance")
        elif self.analysis["certificate_type"] == "OV (Validation d'Organisation)":
            self.legitimacy_score += 2
            self.reasons.append("Certificat OV assure une assurance modérée")
        else:
            self.reasons.append("Certificat DV assure une assurance de base")

    def _check_expiration(self):
        if self.analysis["is_expired"]:
            self.legitimacy_score -= 3
            self.reasons.append("Le certificat est expiré")
        elif self.analysis["days_until_expiry"] < 30:
            self.legitimacy_score -= 1
            self.reasons.append("Le certificat expire bientôt")

    def _check_issuer(self):
        trusted_issuers = ["Let's Encrypt", "DigiCert", "Sectigo", "GlobalSign", "Amazon"]
        if any(issuer in self.analysis["issuer"] for issuer in trusted_issuers):
            self.legitimacy_score += 1
            self.reasons.append("Certificat émis par une CA bien connue")

    def _check_free_hosting(self):
        free_hosting_domains = ["github.io", "netlify.app", "herokuapp.com", "000webhostapp.com"]
        for domain in free_hosting_domains:
            if domain in self.hostname:
                self.free_hosting_domain = domain
                self.legitimacy_score -= 4
                self.reasons.append(f"Site hébergé sur un service d'hébergement gratuit ({domain})")
                break

    def _get_results(self):
        return {
            "url": self.url,
            "certificate_type": self.analysis["certificate_type"],
            "issuer": self.analysis["issuer"],
            "valid_from": self.analysis["valid_from"].isoformat(),
            "valid_until": self.analysis["valid_until"].isoformat(),
            "days_until_expiry": self.analysis["days_until_expiry"],
            "legitimacy_score": round(self.legitimacy_score, 2),
            "reasons": self.reasons,
            "free_hosting_domain": self.free_hosting_domain
        }