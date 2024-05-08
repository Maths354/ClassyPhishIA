from flask import Flask, request, redirect, url_for, render_template, session # type: ignore
from analyse_phishing.check_url.check_url import CheckURL

app = Flask(__name__)
app.secret_key = 'secret_key_test'

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/', methods=['POST'])
def validate_url():
    phishing_link = request.form['phishing-link']
    if phishing_link.startswith('http://') or phishing_link.startswith('https://'):
        session['phishing_link'] = phishing_link
        return redirect(url_for('valid_url_page'))
    else:
        error_message = "L'URL n'est pas valide ou non disponible."
        return render_template('home.html', error_message=error_message)

@app.route('/valid-url')
def valid_url_page():
    phishing_link = session.pop('phishing_link', None)  # Récupérer l'URL depuis la session
    infoURL = CheckURL(phishing_link)
    return render_template('valid_url.html', infoURL=infoURL.url_matching(), phishing_link=phishing_link)

if __name__ == '__main__':
    app.run(debug=True)