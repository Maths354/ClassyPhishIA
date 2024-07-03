import ssl
import socket
import requests
from urllib.parse import urlparse
from datetime import datetime
from cryptography import x509
from cryptography.hazmat.backends import default_backend
from cryptography.x509.oid import NameOID, ExtensionOID

# Fonction pour récupérer le certificat SSL d'un hostname donné
def get_certificate(hostname, port=443):
    context = ssl.create_default_context()
    with socket.create_connection((hostname, port)) as sock:
        with context.wrap_socket(sock, server_hostname=hostname) as secure_sock:
            der_cert = secure_sock.getpeercert(binary_form=True)
    return x509.load_der_x509_certificate(der_cert, default_backend())

# Fonction pour déterminer le type de certificat (DV, OV, EV)
def determine_cert_type(cert):
    subject = cert.subject
    
    ev_oids = [NameOID.BUSINESS_CATEGORY, NameOID.JURISDICTION_COUNTRY_NAME, NameOID.SERIAL_NUMBER]
    is_ev = all(subject.get_attributes_for_oid(oid) for oid in ev_oids)
    
    is_ov = bool(subject.get_attributes_for_oid(NameOID.ORGANIZATION_NAME))
    
    if is_ev:
        return "EV (Validation Étendue)"
    elif is_ov:
        return "OV (Validation d'Organisation)"
    else:
        return "DV (Validation de Domaine)"

# Fonction pour analyser les détails du certificat
def analyze_certificate(url, cert):
    cert_type = determine_cert_type(cert)
    issuer = cert.issuer.get_attributes_for_oid(NameOID.COMMON_NAME)[0].value
    valid_from = cert.not_valid_before
    valid_until = cert.not_valid_after
    current_time = datetime.utcnow()
    
    results = {
        "certificate_type": cert_type,
        "issuer": issuer,
        "valid_from": valid_from,
        "valid_until": valid_until,
        "is_expired": current_time > valid_until,
        "days_until_expiry": (valid_until - current_time).days
    }
    
    return results

# Fonction pour évaluer la légitimité du site basé sur l'analyse du certificat
def assess_legitimacy(analysis, url, api_key):
    score = 0
    reasons = []
    
    # Vérifier le type de certificat
    if analysis["certificate_type"] == "EV (Validation Étendue)":
        score += 3
        reasons.append("Certificat EV assure une haute assurance")
    elif analysis["certificate_type"] == "OV (Validation d'Organisation)":
        score += 2
        reasons.append("Certificat OV assure une assurance modérée")
    else:
        reasons.append("Certificat DV assure une assurance de base")
    
    # Vérifier l'expiration
    if analysis["is_expired"]:
        score -= 3
        reasons.append("Le certificat est expiré")
    elif analysis["days_until_expiry"] < 30:
        score -= 1
        reasons.append("Le certificat expire bientôt")
    
    # Vérifier l'émetteur
    trusted_issuers = ["Let's Encrypt", "DigiCert", "Sectigo", "GlobalSign", "Amazon"]
    if any(issuer in analysis["issuer"] for issuer in trusted_issuers):
        score += 1
        reasons.append("Certificat émis par une CA bien connue")
    
    # Vérifier les domaines d'hébergement gratuit
    free_hosting_domains = ["github.io", "netlify.app", "herokuapp.com", "000webhostapp.com"]
    domain = urlparse(url).netloc
    if any(hosting_domain in domain for hosting_domain in free_hosting_domains):
        score -= 4
        reasons.append("Site hébergé sur un service d'hébergement gratuit (risque élevé d'abus)")
    
    max_score = 10  # On peut ajuster le score maximal si nécessaire
    legitimacy_percentage = max(0, min(100, (score / max_score) * 100))
    
    return legitimacy_percentage, reasons, score
    
# Fonction principale
def main():
    url = input("Entrez l'URL complète à analyser (par exemple https://www.example.com) : ")
    parsed_url = urlparse(url)
    
    if not parsed_url.scheme:
        url = "https://" + url
        parsed_url = urlparse(url)
    
    hostname = parsed_url.hostname
    
    try:
        cert = get_certificate(hostname)
        analysis = analyze_certificate(url, cert)
        legitimacy_score, reasons, raw_score = assess_legitimacy(analysis, url)

        print(f"\nAnalyse pour {url}")
        print(f"Type de certificat: {analysis['certificate_type']}")
        print(f"Émis par: {analysis['issuer']}")
        print(f"Valide à partir de: {analysis['valid_from']}")
        print(f"Valide jusqu'à: {analysis['valid_until']}")
        print(f"Jours jusqu'à l'expiration: {analysis['days_until_expiry']}")
        
        print(f"\nScore de légitimité: {legitimacy_score:.2f}%")
        print("Raisons:")
        for reason in reasons:
            print(f"- {reason}")
        
        if legitimacy_score >= 80:
            print("\nConclusion : Ce site semble légitime.")
        elif legitimacy_score >= 60:
            print("\nConclusion : Ce site semble principalement légitime, mais faites attention.")
        else:
            print("\nConclusion : Ce site pourrait ne pas être légitime. Faites preuve d'une extrême prudence.")
        
    except Exception as e:
        print(f"Une erreur est survenue : {e}")

if __name__ == "__main__":
    main()
