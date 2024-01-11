import requests

def get_html_content(url):
    try:
        # Effectue une requête GET à l'URL fournie
        response = requests.get(url)
        
        # Vérifie si la requête a réussi (statut 200)
        if response.status_code == 200:
            # Récupère le contenu HTML de la page
            html_content = response.text
            return html_content
        else:
            print(f"La requête a échoué avec le code d'état : {response.status_code}")
    except Exception as e:
        print(f"Une erreur s'est produite : {e}")

# Demande à l'utilisateur de fournir l'URL
url = input("Entrez l'URL de la page dont vous souhaitez récupérer le code HTML : ")

# Appelle la fonction et affiche le code HTML si disponible
html_content = get_html_content(url)
if html_content:
    print(html_content)
