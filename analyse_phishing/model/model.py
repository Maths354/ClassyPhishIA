import pandas as pd # type: ignore
from sklearn.linear_model import LogisticRegression # type: ignore
from sklearn.model_selection import train_test_split, GridSearchCV # type: ignore
from sklearn.preprocessing import StandardScaler # type: ignore
from sklearn.metrics import accuracy_score, classification_report # type: ignore

class Model:

    def __init__(self, score_url, score_logo, score_cert):
        self.score_url = score_url
        self.score_logo = score_logo
        self.score_cert = score_cert

    def prediction(self):
        logistic_model, scaler = self.training()

        new_site_features = {
            'url_score': [self.score_url],
            'logo_similarity': [self.score_logo],
            'cert_valid': [self.score_cert]
        }

        new_site_df = pd.DataFrame(new_site_features)
        new_site_df_scaled = scaler.transform(new_site_df)  # Standardisation

        predicted_site_proba = logistic_model.predict_proba(new_site_df_scaled)
        
        probability = float("%.3f" % predicted_site_proba[0][1])
        print(f"The predicted probability is: {probability}")
        return probability

    def training(self):
        data = {
            'url_score': [1.00, 0.80, 0.60, 0.35, 0.15, 0.90, 0.20, 0.00, 1.00, 0.80, 0.00, 1.00, 0.30, 1.00, 0.87],
            'logo_similarity': [1.00, 0.10, 0.50, 1.00, 1.00, 1.00, 0.33, 0.00, 1.00, 1.00, 1.00, 1.00, 1.00, 0.50, 0.10],
            'cert_valid': [0.80, 0.80, 0.85, 0.40, 0.30, 0.90, 0.05, 0.00, 1.00, 0.90, 0.50, 0.95, 0.90, 1.00, 1.00],
            'site_identity': [1, 1, 1, 0, 0, 1, 0, 0, 1, 1, 0, 1, 1, 1, 1]
        }

        df = pd.DataFrame(data)
        X = df[['url_score', 'logo_similarity', 'cert_valid']]
        y = df['site_identity']

        # Standardisation des données
        scaler = StandardScaler()
        X_scaled = scaler.fit_transform(X)

        X_train, X_test, y_train, y_test = train_test_split(X_scaled, y, test_size=0.2, random_state=42)

        # Recherche des meilleurs hyperparamètres
        param_grid = {'C': [0.01, 0.1, 1, 10, 100]}
        logistic_model = GridSearchCV(LogisticRegression(random_state=42), param_grid, cv=5)
        logistic_model.fit(X_train, y_train)

        logistic_predictions = logistic_model.predict(X_test)
        print(f'Predictions: {logistic_predictions}')
        print(f'Accuracy: {accuracy_score(y_test, logistic_predictions)}')
        print(classification_report(y_test, logistic_predictions))

        return logistic_model.best_estimator_, scaler


