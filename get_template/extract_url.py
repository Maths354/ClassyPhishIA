import requests
import re

def extract_urls(url):
    # Faire la requête HTTP pour obtenir le contenu de la page web
    response = requests.get(url)
    # Vérifier si la requête a réussi
    if response.status_code == 200:
        # Extraire toutes les URLs du contenu HTML brut
        urls = re.findall(r'https?://(?:www\.)?[^\s<>"]+|www\.[^\s<>"]+|http://[^\s<>"]+', response.text)
        return urls
    else:
        # Afficher un message d'erreur si la requête a échoué
        print("La requête a échoué avec le code de statut:", response.status_code)
        return []

# Exemple d'utilisation
url = input("Veuillez saisir une URL : ")
urls = extract_urls(url)
for u in urls:
    print(u)
