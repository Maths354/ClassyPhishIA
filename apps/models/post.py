from flask import Flask # type: ignore
from flask_sqlalchemy import SQLAlchemy # type: ignore

from apps.models.models import db, OfficalSite, PhishingSite, ReccurentDomain, ReccurentCA, Score

from apps.config import Config

app = Flask(__name__, template_folder="apps/templates", static_folder="apps/static")
app.config.from_object(Config)
db = SQLAlchemy(app)


class Post():
    
    def __init__(self) -> None:
        pass

    def insert_table(self,upload):
        assert isinstance(upload,(OfficalSite,PhishingSite,ReccurentDomain,Score))
        try:
            with app.app_context():
                db.session.add(upload)
                db.session.commit()
        except:
            raise Exception("Error while trying to use Flask app")
        


    def update_recurrant_domain(self, phishing_link):
        assert isinstance(phishing_link,str)
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
        
    def update_reccurent_ca(self, certificat):
        assert isinstance(certificat,str)
        try:
            with app.app_context():
                update = db.session.get(ReccurentCA, certificat)
                if update:
                    update.reccurent_nb += 1
                    db.session.commit()
                else:
                    update = ReccurentCA(ca=certificat,reccurent_nb=1)
                    db.session.add(update)
                    db.session.commit()
        except:
            raise Exception("Error while trying to use Flask app")