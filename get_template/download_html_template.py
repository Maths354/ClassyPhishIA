import requests
from bs4 import BeautifulSoup
import pandas as pd

def clean_text_tags(tag):
    # Supprime complètement le contenu de la balise
    tag.clear()

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
            html_structure = [tag.prettify(formatter=None) for tag in soup.find_all(True, recursive=False)]
            
            # Nettoie le contenu texte des balises spécifiques
            tags_to_clean = ['h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'p', 'a']
            for tag_name in tags_to_clean:
                for tag in soup.find_all(tag_name):
                    clean_text_tags(tag)
            
            # Recrée la structure HTML mise à jour
            html_structure = [tag.prettify(formatter=None) for tag in soup.find_all(True, recursive=False)]
            
            return html_structure
        else:
            print(f"La requête a échoué avec le code d'état : {response.status_code}")
    except Exception as e:
        print(f"Une erreur s'est produite : {e}")

# Demande à l'utilisateur de fournir l'URL
url = input("Entrez l'URL de la page dont vous souhaitez récupérer le code HTML : ")

# Appelle la fonction et récupère la structure HTML si disponible
html_structure = get_html_structure(url)

if html_structure:
    # Affiche la structure HTML
    print("\n".join(html_structure))
    
    # Crée un DataFrame pandas avec une colonne 'Balise HTML'
    df = pd.DataFrame({'Balise HTML': html_structure})
    
    # Enregistre le DataFrame dans un fichier Excel
    excel_filename = 'output_html_structure.xlsx'
    df.to_excel(excel_filename, index=False)
    
    print(f"\nL'extraction a été enregistrée dans le fichier Excel : {excel_filename}")
else:
    print("La structure HTML n'a pas pu être récupérée.")
