from flask import Flask # type: ignore
from flask_sqlalchemy import SQLAlchemy # type: ignore

from models import db, OfficalSite, PhishingSite, ReccurentDomain, Score

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
db = SQLAlchemy(app)



def insert_table(upload):
    try:
        with app.app_context():
            db.session.add(upload)
            db.session.commit()
    except:
        raise Exception("Error while trying to use Flask app")

def update_recurrant_domain(phishing_link):
    try:
        url = phishing_link.split("/")[2].split(".")
        domain_id = url[len(url)-1]
        with app.app_context():
            update = db.session.get(ReccurentDomain, domain_id)
            if update:
                update.reccurent_nb += 1
                db.session.commit()
            else:
                update = ReccurentDomain(domain=domain_id,reccurent_nb=1)
                db.session.add(update)
                db.session.commit()
    except:
        raise Exception("Error while trying to use Flask app")