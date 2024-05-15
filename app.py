from flask import Flask, request, redirect, url_for, render_template, session # type: ignore
from flask_sqlalchemy import SQLAlchemy # type: ignore

from models import db, PhishingInfo
from analyse_phishing.main import Main
from graph.graph import Graph

from markupsafe import Markup # type: ignore
from os import path
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
    
def post_data(phishing_link):
    upload = PhishingInfo(url_phish=phishing_link, data_logo='data_logo', data_cert='data_cert',
        data_url='data_url')

    try:
        db.session.add(upload)
        db.session.commit()
        print("Upload success")
    except:
        print("Error Upload")

@app.route('/valid-url', methods=['GET', 'POST'])
def valid_url_page():
    phishing_link = session.pop('phishing_link', None)  # Récupérer l'URL depuis la session
    
    allData = Main(phishing_link)
    graph = Graph().grt()

    post_data(phishing_link)

    return render_template('valid_url.html', allData=allData.main(), phishing_link=phishing_link, graph=Markup(graph))

if __name__ == '__main__':
    app.run(debug=True)