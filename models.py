from os import path
from flask import Flask # type: ignore
from flask_sqlalchemy import SQLAlchemy # type: ignore

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
db = SQLAlchemy(app)

# Création base 'phishingInfo'
class PhishingInfo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    url_phish = db.Column(db.String(255), nullable=False)
    data_logo = db.Column(db.String(255), nullable=False)
    data_cert = db.Column(db.String(255), nullable=False)
    data_url = db.Column(db.String(255), nullable=False)

    def __repr__(self):
        return f"<PhishingInfo {self.id}>"
    
if not path.exists('data.db'):
    with app.app_context():
        db.create_all()