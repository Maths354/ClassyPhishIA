import requests
from bs4 import BeautifulSoup

def get_html_structure(url):
    try:
        # Effectue une requête GET à l'URL fournie
        response = requests.get(url)
        
        # Vérifie si la requête a réussi (statut 200)
        if response.status_code == 200:
            # Récupère le contenu HTML de la page
            html_content = response.text
            
            # Utilise BeautifulSoup pour analyser le HTML
            soup = BeautifulSoup(html_content, 'html.parser')
            
            # Extrait toutes les balises sans leur contenu
            html_structure = '\n'.join(tag.prettify(formatter=None) for tag in soup.find_all(True, recursive=False))
            
            return html_structure
        else:
            print(f"La requête a échoué avec le code d'état : {response.status_code}")
    except Exception as e:
        print(f"Une erreur s'est produite : {e}")

# Demande à l'utilisateur de fournir l'URL
url = input("Entrez l'URL de la page dont vous souhaitez récupérer le code HTML : ")

# Appelle la fonction et affiche la structure HTML si disponible
html_structure = get_html_structure(url)
if html_structure:
    print(html_structure)
