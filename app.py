from flask import Flask, request, redirect, url_for, render_template, session # type: ignore
from flask_sqlalchemy import SQLAlchemy # type: ignore
from analyse_phishing.model.tab_positives_negatives import URLAnalyzer
from analyse_phishing.main import Main

#Import DB things
from apps.models.models import OfficalSite, PhishingSite, Score, ReccurentDomain
from apps.models.questions import Questions
from apps.models.post import Post

import requests
import json

app = Flask(__name__, template_folder="apps/templates", static_folder="apps/static")
app.secret_key = 'secret_key_test'

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
db = SQLAlchemy(app)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/stats')
def stats():
    domaines=Questions().get_all_table(ReccurentDomain)
    liste_domains = json.dumps([d['domain'] for d in domaines])
    liste_reccurent_nb = json.dumps([d['reccurent_nb'] for d in domaines])

    return render_template('stats.html', url=liste_domains, nbURL=liste_reccurent_nb)
    
@app.route('/informations')
def informations():
    return render_template('informations.html')

@app.route('/', methods=['POST'])
def validate_url():
    phishing_link = request.form['phishing-link']

    # Vérifier de l'URL
    if (phishing_link.startswith('http://') or phishing_link.startswith('https://')) and len(phishing_link)<=255:

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
    
    official_sites=Questions().get_all_table(OfficalSite)

    allDatas = Main(phishing_link).main(official_sites)

    datas=allDatas["datas"]
    scores=allDatas["scores"]
    id_official=allDatas["id_official"]

    my_phish_site = PhishingSite(id_offical_site=1, phishing_url=phishing_link, url=str(datas["checkURL"]), list_url=str(datas["extractURL"]), logo=str(datas["extractLogo"]), key_word=str(datas["extractKeyword"]), certificate=str(datas["extractCert"][1]), template=str(datas["extractTemplate"]))
    Post().insert_table(upload=my_phish_site)

    last_phishing_id=Questions().get_last_phishing_id()
    my_score = Score(id_phishing_site=last_phishing_id, score_url=scores["checkURL"], score_list_url=scores["extractURL"], score_certificate=scores["extractCert"], score_logo=scores["extractLogo"], score_key_word=scores["extractKeyword"])
    Post().insert_table(upload=my_score)


    Post().update_recurrant_domain(phishing_link=phishing_link)
    cert_issuer = datas["extractCert"][1]["issuer"][1][0][1]
    Post().update_reccurent_ca(certificat=cert_issuer)

    url_analyzer = URLAnalyzer(phishing_link)
    positive_points, negative_points = url_analyzer.analyze()

    return render_template('valid_url.html', datas=datas, scores=scores, id_official=id_official, 
                           phishing_link=phishing_link, positive_points=positive_points, negative_points=negative_points)

if __name__ == '__main__':
    app.run(debug=True)
