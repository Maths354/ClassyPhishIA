import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score, classification_report

class Model:

    def __init__(self, score_url, score_logo, score_cert, list_url):
        # Initialisation des attributs du modèle
        self.score_url = score_url
        self.score_logo = score_logo
        self.score_cert = score_cert
        self.list_url = list_url

    def prediction(self):
        # Prédiction basée sur les nouvelles données
        logistic_model, scaler = self.training() # Entraînement du modèle et récupération du scaler

        # Préparation des nouvelles données
        new_site_features = {
            'url_score': [self.score_url],
            'logo_similarity': [self.score_logo],
            'cert_valid': [self.score_cert],
            'list_url': [self.list_url]
        }

        new_site_df = pd.DataFrame(new_site_features)
        new_site_df_scaled = scaler.transform(new_site_df)  # Standardisation

        # Prédiction de la probabilité
        predicted_site_proba = logistic_model.predict_proba(new_site_df_scaled)
        probability = float("%.3f" % predicted_site_proba[0][1])
        print(f"La probabilité prédite est : {probability}")
        return probability

    def training(self):
        # Entraînement du modèle avec les données existantes
        data = {
            'url_score': [1.00, 0.80, 0.60, 0.35, 0.15, 0.90, 0.20, 0.00, 1.00, 0.80, 0.00, 1.00, 0.30, 1.00, 0.87, 0.12, 0.23, 1.00, 1.00, 1.00, 0.77, 0.75],
            'logo_similarity': [1.00, 0.10, 0.50, 1.00, 1.00, 1.00, 0.33, 0.00, 1.00, 1.00, 1.00, 1.00, 1.00, 0.50, 0.10, 0.00, 0.00, 0.33, 0.20, 0.80, 0.00, 0.30],
            'cert_valid': [0.80, 0.80, 0.85, 0.40, 0.30, 0.90, 0.05, 0.00, 1.00, 0.90, 0.50, 0.95, 0.90, 1.00, 1.00, 0.40, 0.50, 0.80, 0.74, 0.90, 0.80, 0.60],
            'list_url': [1.00, 1.00, 1.00, 0.10, 0.00, 0.60, 0.10, 0.00, 1.00, 0.80, 0.00, 0.88, 0.95, 0.50, 0.96, 0.20, 0.00, 1.00, 0.70, 0.90, 0.60, 0.50],
            'site_identity': [1, 1, 1, 0, 0, 1, 0, 0, 1, 1, 0, 1, 1, 1, 1, 0, 0, 1, 1, 1, 1, 1]
        }

        df = pd.DataFrame(data) # Création du DataFrame
        X = df[['url_score', 'logo_similarity', 'cert_valid', 'list_url']] # Sélection des caractéristiques
        y = df['site_identity'] # Sélection de la cible

        # Standardisation des données
        scaler = StandardScaler()
        X_scaled = scaler.fit_transform(X)

        # Division des données en ensemble d'entraînement et de test
        X_train, X_test, y_train, y_test = train_test_split(X_scaled, y, test_size=0.2, random_state=42)

        # Recherche des meilleurs hyperparamètres
        param_grid = {'C': [0.01, 0.1, 1, 10, 100]}
        logistic_model = GridSearchCV(LogisticRegression(random_state=42), param_grid, cv=5)
        logistic_model.fit(X_train, y_train)

        # Évaluation du modèle
        logistic_predictions = logistic_model.predict(X_test)
        print(f'Prédictions : {logistic_predictions}')
        print(f'Précision : {accuracy_score(y_test, logistic_predictions)}')
        print(classification_report(y_test, logistic_predictions))

        return logistic_model.best_estimator_, scaler # Retour du modèle et du scaler