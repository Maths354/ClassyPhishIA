import pandas as pd # type: ignore
from sklearn.linear_model import LogisticRegression # type: ignore
from sklearn.model_selection import train_test_split # type: ignore
from sklearn.metrics import accuracy_score # type: ignore

class Model:
    
    def __init__(self, score_url, score_text, score_logo, score_cert):
        self.score_url = score_url
        self.score_text = score_text
        self.score_logo = score_logo
        self.score_cert = score_cert


    def prediction(self):

        logistic_model = self.training()

        # Site de phishing à tester
        new_site_features = {
            'url_score': [0.00],
            'text_score': [0.00],
            'logo_similarity': [0.90],
            # 'cert_valid': [1]
        }

        new_site_df = pd.DataFrame(new_site_features)

        # Faire une prédiction avec le modèle
        predicted_site_proba = logistic_model.predict_proba(new_site_df)
        #print(f'The proba is : {predicted_site_proba[0][1]}')

        return float("%.4f" % predicted_site_proba[0][1])
        # Récupérer le nom du site légitime à partir de l'ID (supposons que `site_id_to_name` est un dictionnaire que vous avez créé)
        # site_name = site_id_to_name[predicted_site_id[0]]
        # print(f'The site is impersonating: {site_name}')


    def training(self):

        # Données fictives d'entrainement à récupérer en BDD_SCORE.
        data = {
            'url_score':        [0.95, 0.80, 0.60, 0.40, 0.30, 0.35, 0.15, 0.05, 0.90, 0.20, 0.05, 0.00, 1.00, 0.00, 0.00, 1.00, 0.00],
            'text_score':       [0.90, 0.65, 0.55, 0.30, 0.25, 0.58, 0.20, 0.20, 0.62, 0.10, 0.20, 0.00, 1.00, 0.50, 0.00, 1.00, 1.00],
            'logo_similarity':  [0.98, 0.10, 0.50, 0.15, 0.20, 0.99, 0.99, 0.05, 0.10, 0.33, 0.10, 0.00, 1.00, 0.99, 1.00, 1.00, 1.00],
            # 'cert_valid':       [1, 0, 0, 1, 0],
            'site_identity':    [1, 1, 1, 0, 0, 1, 1, 0, 1, 0, 0, 0, 1, 1, 1, 1, 1]  # Identité réelle du site (label)
        }

        df = pd.DataFrame(data)

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
        
        return logistic_model