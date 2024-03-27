import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

# Données fictives
data = {
    'url_score':        [0.95, 0.80, 0.60, 0.40, 0.30, 0.35, 0.15, 0.05, 0.90, 0.20, 0.05],
    'text_score':       [0.90, 0.65, 0.55, 0.30, 0.25, 0.58, 0.20, 0.20, 0.62, 0.10, 0.20],
    'logo_similarity':  [0.98, 0.10, 0.50, 0.15, 0.20, 0.99, 0.99, 0.05, 0.10, 0.33, 0.10],
    # 'has_https':        [1, 0, 1, 1, 0],
    # 'cert_valid':       [1, 0, 0, 1, 0],
    'site_identity':    [1, 1, 1, 0, 0, 1, 1, 0, 1, 0, 0]  # Identité réelle du site (label)
}

# Création d'un DataFrame
df = pd.DataFrame(data)

# Séparation des caractéristiques et des labels
#X = df[['url_score', 'text_score', 'logo_similarity', 'has_https', 'cert_valid']]

X = df[['url_score', 'text_score', 'logo_similarity']]
y = df['site_identity']

# Séparation des données en ensembles d'entraînement et de test
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Création et entraînement du modèle de régression logistique
logistic_model = LogisticRegression(random_state=42)
logistic_model.fit(X_train, y_train)

# Prédiction sur l'ensemble de test
logistic_predictions = logistic_model.predict(X_test)
print(logistic_predictions)

# Évaluation du modèle de régression logistique
logistic_accuracy = accuracy_score(y_test, logistic_predictions)
print(f'Logistic Regression Accuracy: {logistic_accuracy}')

# "scaler" = Ojet StandardScaler utilisé pour mettre à l'échelle les données d'entraînement, si nécessaire.

# Nouvelles caractéristiques extraites du site à tester
new_site_features = {
    'url_score': [0.1],
    'text_score': [0.2],
    'logo_similarity': [0.99],
    # 'has_https': [1],
    # 'cert_valid': [1]
}

# DataFrame pour les nouvelles caractéristiques
new_site_df = pd.DataFrame(new_site_features)

# Prétraitement des caractéristiques si nécessaire (par exemple, mise à l'échelle)
# new_site_scaled = scaler.transform(new_site_df)

# Faire une prédiction avec le modèle
predicted_site_id = logistic_model.predict(new_site_df)

# Afficher l'identité du site légitime prédite
print(f'The model predicts that the site is impersonating the legitimate site with ID: {predicted_site_id[0]}')

# Récupérer le nom du site légitime à partir de l'ID (supposons que `site_id_to_name` est un dictionnaire que vous avez créé)
# site_name = site_id_to_name[predicted_site_id[0]]
# print(f'The site is impersonating: {site_name}')
