import ssl
import socket
import requests
from urllib.parse import urlparse
from datetime import datetime
from cryptography import x509
from cryptography.hazmat.backends import default_backend
from cryptography.x509.oid import NameOID, ExtensionOID

def check_domain_reputation(domain, api_key):
    base_url = "https://www.virustotal.com/api/v3/"
    headers = {
        "accept": "application/json",
        "x-apikey": api_key
    }
    
    url = f"{base_url}domains/{domain}"
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        data = response.json()
        stats = data['data']['attributes']['last_analysis_stats']
        reputation_score = data['data']['attributes']['reputation']
        
        total_scans = sum(stats.values())
        malicious_scans = stats['malicious']
        suspicious_scans = stats['suspicious']
        
        print("test : ", total_scans, malicious_scans, suspicious_scans, reputation_score)
        
        return {
            "reputation_score": reputation_score,
            "total_scans": total_scans,
            "malicious_scans": malicious_scans,
            "suspicious_scans": suspicious_scans
        }
    else:
        return None
    

def get_certificate(hostname, port=443):
    context = ssl.create_default_context()
    with socket.create_connection((hostname, port)) as sock:
        with context.wrap_socket(sock, server_hostname=hostname) as secure_sock:
            der_cert = secure_sock.getpeercert(binary_form=True)
    return x509.load_der_x509_certificate(der_cert, default_backend())

def determine_cert_type(cert):
    subject = cert.subject
    
    ev_oids = [NameOID.BUSINESS_CATEGORY, NameOID.JURISDICTION_COUNTRY_NAME, NameOID.SERIAL_NUMBER]
    is_ev = all(subject.get_attributes_for_oid(oid) for oid in ev_oids)
    
    is_ov = bool(subject.get_attributes_for_oid(NameOID.ORGANIZATION_NAME))
    
    if is_ev:
        return "EV (Extended Validation)"
    elif is_ov:
        return "OV (Organization Validation)"
    else:
        return "DV (Domain Validation)"

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


def assess_legitimacy(analysis, url, api_key):
    score = 0
    reasons = []
    
    # Check certificate type
    if analysis["certificate_type"] == "EV (Extended Validation)":
        score += 3
        reasons.append("EV certificate provides high assurance")
    elif analysis["certificate_type"] == "OV (Organization Validation)":
        score += 2
        reasons.append("OV certificate provides moderate assurance")
    else:
        reasons.append("DV certificate provides basic assurance")
    
    # Check expiration
    if analysis["is_expired"]:
        score -= 3
        reasons.append("Certificate is expired")
    elif analysis["days_until_expiry"] < 30:
        score -= 1
        reasons.append("Certificate is nearing expiration")
    
    # Check issuer
    trusted_issuers = ["Let's Encrypt", "DigiCert", "Sectigo", "GlobalSign", "Amazon"]
    if any(issuer in analysis["issuer"] for issuer in trusted_issuers):
        score += 1
        reasons.append("Certificate issued by a well-known CA")
    
    # Check for free hosting domains
    free_hosting_domains = ["github.io", "netlify.app", "herokuapp.com", "000webhostapp.com"]
    domain = urlparse(url).netloc
    if any(hosting_domain in domain for hosting_domain in free_hosting_domains):
        score -= 4
        reasons.append("Site hosted on a free hosting service (higher risk of abuse)")

    # Analyse virus total
    reputation_data = check_domain_reputation(domain, api_key)
    
    if reputation_data:
        if reputation_data["reputation_score"] > 0:
            score += 4
            reasons.append(f"Domain has positive VirusTotal reputation score: {reputation_data['reputation_score']}")
        elif reputation_data["reputation_score"] == 0:
            score += 2
            reasons.append(f"Le domaine est neutre, le score de réputation de VirusTotal : {reputation_data['reputation_score']}")
        elif reputation_data["reputation_score"] < 0:
            score -= 3
            reasons.append(f"Domain has negative VirusTotal reputation score: {reputation_data['reputation_score']}")

        if reputation_data["malicious_scans"] > 1:
            score -=5
            reasons.append(f"Le domain est flag par VirusTotal {reputation_data['malicious_scans']}")
        elif reputation_data["malicious_scans"] == 0:
            score +=4
            reasons.append(f"Le domain n'est pas flag par VirusTotal {reputation_data['malicious_scans']}")
    else:
        reasons.append("Unable to check domain reputation")
    
    max_score = 12  # On peux ajuster le score max si besoin
    legitimacy_percentage = max(0, min(100, (score / max_score) * 100))
    
    return legitimacy_percentage, reasons, score
    
def main():
    url = input("Enter the full URL to analyze (e.g., https://www.example.com): ")
    api_key = input("Enter your VirusTotal API key: ")
    parsed_url = urlparse(url)
    
    if not parsed_url.scheme:
        url = "https://" + url
        parsed_url = urlparse(url)
    
    hostname = parsed_url.hostname
    
    try:
        cert = get_certificate(hostname)
        analysis = analyze_certificate(url, cert)
        legitimacy_score, reasons, raw_score = assess_legitimacy(analysis, url, api_key)

        print(f"\nAnalysis for {url}")
        print(f"Certificate Type: {analysis['certificate_type']}")
        print(f"Issuer: {analysis['issuer']}")
        print(f"Valid From: {analysis['valid_from']}")
        print(f"Valid Until: {analysis['valid_until']}")
        print(f"Days Until Expiry: {analysis['days_until_expiry']}")
        
        print(f"\nLegitimacy Score: {legitimacy_score:.2f}%")
        print("Reasons:")
        for reason in reasons:
            print(f"- {reason}")
        
        if legitimacy_score >= 80:
            print("\nConclusion: This site appears to be legitimate.")
        elif legitimacy_score >= 60:
            print("\nConclusion: This site seems mostly legitimate, but exercise caution.")
        else:
            print("\nConclusion: This site may not be legitimate. Exercise extreme caution.")
        
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()