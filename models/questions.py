from flask import Flask # type: ignore
from flask_sqlalchemy import SQLAlchemy # type: ignore

from models.models import db, OfficalSite, PhishingSite, ReccurentDomain, Score

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
db = SQLAlchemy(app)

class Questions():

    def __init__(self) -> None:
        pass

    def get_table(self,table):
        assert isinstance(table,(OfficalSite,PhishingSite,ReccurentDomain,Score))
        try:
            with app.app_context():
                datas = db.session.get(table,1)
                return datas
        except:
            raise Exception("Error while trying to use Flask app")

