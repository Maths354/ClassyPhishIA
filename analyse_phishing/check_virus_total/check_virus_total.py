
import requests
from urllib.parse import urlparse


class CheckVirusTotal:
    
    def __init__(self, url):
        self.url=url

    def reputation_score(self, reputation_score, malicious_scans, suspicious_scans):
        normalized_reputation = 0.00

        if reputation_score >= 10:
            normalized_reputation = 1.00
        elif reputation_score > 3 and reputation_score < 10:
            normalized_reputation = 0.95
        elif reputation_score > 1 and normalized_reputation <= 3:
            normalized_reputation = 0.90
        elif reputation_score == 1:
            normalized_reputation = 0.85
        elif reputation_score == 0:
            normalized_reputation = 0.50
        elif reputation_score < 0:
            normalized_reputation = 0.25

        if malicious_scans >= 5:
            normalized_reputation = normalized_reputation * 0.25
        elif malicious_scans > 1 and malicious_scans < 5:
            normalized_reputation = normalized_reputation * 0.50
        elif malicious_scans == 1:
            normalized_reputation = normalized_reputation * 0.75
        elif suspicious_scans > 1:
            normalized_reputation = normalized_reputation * 0.95
        
        return normalized_reputation

    def check_domain_reputation(self):

        #api_key = input("Enter your VirusTotal API key: ")
        api_key = ""
        if api_key != "":

            domain = urlparse(self.url).netloc

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
                
                # Calcul du score de confiance : harmless pour nombre de scan inofensif
                harmless_scans = stats['harmless']
                confidence_score = (harmless_scans / total_scans) if total_scans > 0 else 0
                
                normalized_reputation = self.reputation_score(reputation_score, malicious_scans, suspicious_scans)
                final_confidence_score = (confidence_score * 0.2 + normalized_reputation * 0.8)
                            
                # Assurez-vous que le score final est entre 0 et 1
                final_confidence_score = max(0, min(1, final_confidence_score))
                
                print(f"Scans totaux: {total_scans}, Malicieux: {malicious_scans}, Suspicieux: {suspicious_scans}, harmless: {harmless_scans}, Score de réputation: {reputation_score}")
                print(f"Score de confiance final: {final_confidence_score:.2f}")
                
                return {
                    "reputation_score": reputation_score,
                    "total_scans": total_scans,
                    "malicious_scans": malicious_scans,
                    "suspicious_scans": suspicious_scans,
                    "harmless_scans": harmless_scans,
                    "confidence_score": final_confidence_score
                }
            else:
                print(f"Erreur lors de la requête à VirusTotal: {response.status_code}")
                return None
        else:
            return {
                    "no_api": "No api",
                    "confidence_score": 0.00
                }
