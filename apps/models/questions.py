from flask import Flask # type: ignore
from flask_sqlalchemy import SQLAlchemy # type: ignore

from apps.models.models import db, OfficalSite, PhishingSite, ReccurentDomain, Score

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
db = SQLAlchemy(app)

class Questions():

    def __init__(self) -> None:
        pass

    def get_all_table(self, table):
        try:
            with app.app_context():
                datas = db.session.query(table).all()

                if datas:
                    if table == OfficalSite:
                        results = [
                        {
                            "id": data.id,
                            "url": data.url,
                            "list_url" : data.list_url,
                            "logo" : data.logo,
                            "key_word" : data.key_word,
                            "certificate" : data.certificate,
                            "template" : data.template
                            
                        } for data in datas
                        ]
                    elif table == PhishingSite:
                        results = [
                        {
                            "id": data.id,
                            "id_offical_site" : data.id_offical_site,
                            "url": data.url,
                            "list_url" : data.list_url,
                            "logo" : data.logo,
                            "key_word" : data.key_word,
                            "certificate" : data.certificate,
                            "template" : data.template
                            
                        } for data in datas
                        ]
                    elif table == Score:
                        results = [
                        {
                            "id": data.id,
                            "id_phishing_site" : data.id_phishing_site,
                            "score_url": data.score_url,
                            "score_certificate" : data.score_certificate,
                            "score_logo" : data.score_logo,
                            "score_key_word" : data.score_key_word
                        } for data in datas
                        ]
                    elif table == ReccurentDomain:
                        results = [
                        {
                            "domain": data.domain,
                            "reccurent_nb" : data.reccurent_nb
                        } for data in datas
                        ]
                    return results
        except:
            raise Exception("Error while trying to use Flask app")
    
    def get_table_with_id(self,table,id):
        try:
            with app.app_context():
                if table == ReccurentDomain:
                    datas = db.session.query(table).filter_by(domain=id).all()
                else:
                    datas = db.session.query(table).filter_by(id=id).all()
                if datas:
                    if table == OfficalSite:
                        results = [
                        {
                            "id": data.id,
                            "url": data.url,
                            "list_url" : data.list_url,
                            "logo" : data.logo,
                            "key_word" : data.key_word,
                            "certificate" : data.certificate,
                            "template" : data.template
                            
                        } for data in datas
                        ]
                    elif table == PhishingSite:
                        results = [
                        {
                            "id": data.id,
                            "id_offical_site" : data.id_offical_site,
                            "url": data.url,
                            "list_url" : data.list_url,
                            "logo" : data.logo,
                            "key_word" : data.key_word,
                            "certificate" : data.certificate,
                            "template" : data.template
                            
                        } for data in datas
                        ]
                    elif table == Score:
                        results = [
                        {
                            "id": data.id,
                            "id_phishing_site" : data.id_phishing_site,
                            "score_url": data.score_url,
                            "score_certificate" : data.score_certificate,
                            "score_logo" : data.score_logo,
                            "score_key_word" : data.score_key_word
                        } for data in datas
                        ]
                    elif table == ReccurentDomain:
                        results = [
                        {
                            "domain": data.domain,
                            "reccurent_nb" : data.reccurent_nb
                        } for data in datas
                        ]
                    return results
        except:
            raise Exception("Error while trying to use Flask app")

