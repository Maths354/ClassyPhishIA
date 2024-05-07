from flask import Flask, request, redirect, url_for, render_template # type: ignore

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/validate_url', methods=['POST'])
def validate_url():
    phishing_link = request.form['phishing-link']
    if phishing_link.startswith('http://') or phishing_link.startswith('https://'):
        return redirect(url_for('valid_url_page'))
    else:
        error_message = "L'URL n'est pas valide ou non disponible."
        return render_template('home.html', error_message=error_message)

@app.route('/valid-url')
def valid_url_page():
    return render_template('valid_url.html')

if __name__ == '__main__':
    app.run(debug=True)