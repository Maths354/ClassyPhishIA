import difflib

class CheckURL:
    
    def __init__(self, url, official_sites):
        self.url = url
        self.official_sites = official_sites

    def url_matching(self):
        top_ratio = 0  # Initialisation du ratio le plus élevé trouvé
        top_string = ""  # Initialisation de la sous-chaîne correspondante au meilleur ratio
        top_company = ""  # Initialisation de l'identifiant de la meilleure entreprise correspondante

        # Parcours de toutes les entreprises officielles fournies
        for company in self.official_sites:
            company_url = company["url"]
            company_str_len = len(company_url)
            
            # Parcours de toutes les sous-chaînes possibles de l'URL de l'entreprise
            for start_letter in range(company_str_len):
                for end_letter in range(start_letter, company_str_len):
                    # Calcul du ratio de similarité entre la sous-chaîne de l'URL de l'entreprise et l'URL fournie
                    ratio = difflib.SequenceMatcher(None, self.url, company_url[start_letter:end_letter+1]).ratio()
                    
                    # Mise à jour des meilleurs résultats si un nouveau meilleur ratio est trouvé
                    if ratio > top_ratio:
                        top_ratio = ratio
                        top_string = company_url[start_letter:end_letter+1]
                        top_company = [company["id"], company["url"]]

        # Retourne la sous-chaîne avec le meilleur ratio, le ratio lui-même (arrondi à trois décimales), et l'identifiant de l'entreprise correspondante
        return top_string, float("%.3f" % top_ratio), top_company
