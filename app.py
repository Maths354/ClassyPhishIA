from flask import Flask, request, redirect, url_for, render_template, session # type: ignore
# from analyse_phishing.check_url.check_url import CheckURL
# from analyse_phishing.extract_url.extract_url import ExtractURL
from analyse_phishing.main import Main

import requests

app = Flask(__name__)
app.secret_key = 'secret_key_test'

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
            #if response.status_code == 200 :
            session['phishing_link'] = phishing_link
            return redirect(url_for('valid_url_page'))
        except requests.ConnectionError:
            error_message = "URL non disponible."
            return render_template('home.html', error_message=error_message)           
            
    else:
        error_message = "URL n'est pas valide"
        return render_template('home.html', error_message=error_message)

@app.route('/valid-url')
def valid_url_page():
    phishing_link = session.pop('phishing_link', None)  # Récupérer l'URL depuis la session
    
    allData = Main(phishing_link)

    return render_template('valid_url.html', allData=allData.main(), phishing_link=phishing_link)

if __name__ == '__main__':
    app.run(debug=True)