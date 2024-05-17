from os import path
from flask import Flask # type: ignore
from flask_sqlalchemy import SQLAlchemy # type: ignore

from models import db, PhishingInfo, ReccurentDomain

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
db = SQLAlchemy(app)


def post_data(phishing_link):
    upload = PhishingInfo(url_phish=phishing_link, data_logo='data_logo', data_cert='data_cert',data_url='data_url')

    try:
        with app.app_context():
            db.session.add(upload)
            db.session.commit()
    except:
        raise Exception("Error while trying to use Flask app")

    try:
        url = phishing_link.split("/")[2].split(".")
        domain_id = url[len(url)-1]  # Par exemple
        with app.app_context():
            # Récupérer l'objet Upload depuis la base de données
            update = db.session.get(ReccurentDomain, domain_id)
            if update:
                # Incrémenter la colonne download_count
                update.reccurent_nb += 1
                # Enregistrer les modifications dans la base de données
                db.session.commit()
            else:
                update = ReccurentDomain(domain=domain_id,reccurent_nb=1)
                db.session.add(update)
                db.session.commit()
    except:
        raise Exception("Error while trying to use Flask app")

    #table_domain = ReccurentDomain(domain="net")