import requests
from bs4 import BeautifulSoup
import re

def extract_and_save_urls(url):
    # Définir un en-tête User-Agent
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
    }

    # Faire la requête HTTP avec l'en-tête User-Agent
    response = requests.get(url, headers=headers)

    # Vérifier si la requête a réussi
    if response.status_code == 200:
        # Utiliser BeautifulSoup pour analyser le contenu HTML
        soup = BeautifulSoup(response.text, 'html.parser')

        # Extraire les URL des attributs href et src
        non_url_list = [link.get('href') for link in soup.find_all('a', href=True)] + \
                        [img.get('src') for img in soup.find_all('img', src=True)]

        # Extraire les URL avec l'expression régulière
        regex_urls = re.findall(r'https?://(?:www\.)?[^\s<>"]+|www\.[^\s<>"]+|http://[^\s<>"]+', response.text)

        # Enregistrer les URL dans les fichiers
        with open('all_url.txt', 'w') as non_url_file:
            for non_url in non_url_list:
                non_url_file.write(str(non_url) + '\n')

        with open('url.txt', 'w') as url_file:
            for regex_url in regex_urls:
                url_file.write(str(regex_url) + '\n')

        return non_url_list, regex_urls
    elif response.status_code == 403:
        print("Accès refusé. Veuillez vérifier vos permissions.")
        return [], []
    else:
        # Afficher un message d'erreur si la requête a échoué pour une autre raison
        print("La requête a échoué avec le code de statut:", response.status_code)
        return [], []

# Exemple d'utilisation
url = input("Veuillez saisir une URL : ")
non_url_list, regex_urls = extract_and_save_urls(url)

print("URLs extraites des attributs href et src (all_url.txt) :")
for non_url in non_url_list:
    print(non_url)

print("\nURLs extraites avec l'expression régulière (url.txt) :")
for regex_url in regex_urls:
    print(regex_url)