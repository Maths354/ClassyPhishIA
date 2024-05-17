from flask import Flask, request, redirect, url_for, render_template, session # type: ignore
from flask_sqlalchemy import SQLAlchemy # type: ignore

from models import db
from analyse_phishing.main import Main
from graph.graph import BarChart
from request_db import post_data

from markupsafe import Markup # type: ignore
import requests

app = Flask(__name__)
app.secret_key = 'secret_key_test'

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
db = SQLAlchemy(app)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/', methods=['POST'])
def validate_url():
    phishing_link = request.form['phishing-link']

    # Vérifier de l'URL
    if phishing_link.startswith('http://') or phishing_link.startswith('https://'):

        try:
            requests.get(phishing_link)
            session['phishing_link'] = phishing_link
            return redirect(url_for('valid_url_page'))
        except requests.ConnectionError:
            error_message = "URL non disponible."
            return render_template('home.html', error_message=error_message)           
            
    else:
        error_message = "URL n'est pas valide"
        return render_template('home.html', error_message=error_message)


@app.route('/valid-url', methods=['GET', 'POST'])
def valid_url_page():
    phishing_link = session.pop('phishing_link', None)  # Récupérer l'URL depuis la session
    
    allData = Main(phishing_link)
    barchart = BarChart().grt()

    post_data(phishing_link)

    return render_template('valid_url.html', allData=allData.main(), phishing_link=phishing_link, barchart=Markup(barchart))

if __name__ == '__main__':
    app.run(debug=True)