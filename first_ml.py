import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Chargement du fichier CSV
data = pd.read_csv('templates.csv')

# Exemple de données (remplacez cela par vos propres données)
template1 = "<html>...</html>"
template2 = "<html>...</html>"

# Création d'une liste de templates
templates = [template1, template2]

# Parsage des templates HTML (c'est une étape simplifiée, vous devrez adapter cela selon vos besoins)
def parse_html(template):
    # Ici, vous devriez utiliser une bibliothèque comme BeautifulSoup
    # pour extraire des caractéristiques spécifiques du HTML.
    return template

# Extraction de caractéristiques
parsed_templates = [parse_html(template) for template in templates]

# Conversion des données parsées en texte pour le modèle TF-IDF
text_data = [" ".join(parsed_template) for parsed_template in parsed_templates]

# Vectorisation avec TF-IDF
vectorizer = TfidfVectorizer()
tfidf_matrix = vectorizer.fit_transform(text_data)

# Calcul de la similarité cosinus entre les templates
similarity_matrix = cosine_similarity(tfidf_matrix, tfidf_matrix)

# Affichage de la matrice de similarité
print("Matrice de Similarité :")
print(similarity_matrix)
