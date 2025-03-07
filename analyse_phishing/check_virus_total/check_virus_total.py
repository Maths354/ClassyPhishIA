import requests
from urllib.parse import urlparse


class CheckVirusTotal:
    
    def __init__(self, url, apiKey):
        # Initialisation de l'instance avec l'URL et la clé API fournie
        self.url = url
        self.apiKey = apiKey

    def reputation_score(self, reputation_score, malicious_scans, suspicious_scans):
        # Fonction pour normaliser le score de réputation basé sur divers paramètres
        normalized_reputation = 0.00

        # Normalisation basée sur le score de réputation
        if reputation_score >= 10:
            normalized_reputation = 1.00
        elif reputation_score > 3 and reputation_score < 10:
            normalized_reputation = 0.95
        elif reputation_score > 1 and reputation_score <= 3:
            normalized_reputation = 0.90
        elif reputation_score == 1:
            normalized_reputation = 0.85
        elif reputation_score == 0:
            normalized_reputation = 0.50
        elif reputation_score < 0:
            normalized_reputation = 0.25

        # Ajustement basé sur le nombre de scans malveillants
        if malicious_scans >= 5:
            normalized_reputation = normalized_reputation * 0.25
        elif malicious_scans > 1 and malicious_scans < 5:
            normalized_reputation = normalized_reputation * 0.50
        elif malicious_scans == 1:
            normalized_reputation = normalized_reputation * 0.75
        # Ajustement basé sur le nombre de scans suspicieux
        elif suspicious_scans > 1:
            normalized_reputation = normalized_reputation * 0.95
        
        return normalized_reputation

    def check_domain_reputation(self):
        # Fonction pour vérifier la réputation d'un domaine via l'API VirusTotal
        api_key = self.apiKey

        if api_key != "":
            # Extraction du domaine à partir de l'URL fournie
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
                
                # Calcul des statistiques à partir des analyses
                total_scans = sum(stats.values())
                malicious_scans = stats['malicious']
                suspicious_scans = stats['suspicious']
                
                # Calcul du score de confiance basé sur les scans inoffensifs
                harmless_scans = stats['harmless']
                confidence_score = (harmless_scans / total_scans) if total_scans > 0 else 0
                
                # Calcul de la réputation normalisée
                normalized_reputation = self.reputation_score(reputation_score, malicious_scans, suspicious_scans)
                final_confidence_score = (confidence_score * 0.2 + normalized_reputation * 0.8)
                            
                # Assurez-vous que le score final est entre 0 et 1
                final_confidence_score = max(0, min(1, final_confidence_score))
                
                print(f"Scans totaux: {total_scans}, Malicieux: {malicious_scans}, Suspicieux: {suspicious_scans}, Inoffensifs: {harmless_scans}, Score de réputation: {reputation_score}")
                print(f"Score de confiance final: {final_confidence_score:.2f}")
                
                return {
                    "scan_total": total_scans,
                    "score_de_réputation": reputation_score,
                    "scan_malveillant": malicious_scans,
                    "scan_suspicieux": suspicious_scans,
                    "scan_inoffensif": harmless_scans,
                    "score_de_confiance": final_confidence_score
                }
            else:
                # Gestion des erreurs de requête
                print(f"Erreur lors de la requête à VirusTotal: {response.status_code}")
                return {
                    "Erreur": "Erreur clé API",
                    "score_de_confiance": 0.00
                }
        else:
            # Gestion du cas où la clé API n'est pas fournie
            return {
                "no_api": "Pas de clé API",
                "score_de_confiance": 0.00
            }
