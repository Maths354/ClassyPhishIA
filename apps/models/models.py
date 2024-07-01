from os import path
from flask import Flask # type: ignore
from flask_sqlalchemy import SQLAlchemy # type: ignore
from apps.config import Config

app = Flask(__name__, template_folder="apps/templates", static_folder="apps/static")
app.config.from_object(Config)
db = SQLAlchemy(app)


# Création table 'official_site'
class OfficalSite(db.Model):
    __tablename__ = 'official_site'
    id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.String(10000), nullable=False)
    list_url = db.Column(db.String(10000), nullable=False)
    logo = db.Column(db.String(10000), nullable=False)
    key_word = db.Column(db.String(10000), nullable=False)
    certificate = db.Column(db.String(10000), nullable=False)
    template = db.Column(db.String(10000), nullable=False)


# Création table 'phishing_site'
class PhishingSite(db.Model):
    __tablename__ = 'phishing_site'
    id = db.Column(db.Integer, primary_key=True)
    phishing_url = db.Column(db.String(10000), nullable=False)
    url = db.Column(db.String(10000), nullable=False)
    list_url = db.Column(db.String(10000), nullable=False)
    logo = db.Column(db.String(10000), nullable=False)
    key_word = db.Column(db.String(10000), nullable=False)
    certificate = db.Column(db.String(10000), nullable=False)
    template = db.Column(db.String(100000), nullable=False)


# Création table 'score'
class Score(db.Model):
    __tablename__ = 'score'
    id = db.Column(db.Integer, primary_key=True)
    id_phishing_site = db.Column(db.Integer, db.ForeignKey('phishing_site.id'))
    score_url = db.Column(db.Float, nullable=False)
    score_list_url = db.Column(db.Float, nullable=False)
    score_certificate = db.Column(db.Float, nullable=False)
    score_logo = db.Column(db.Float, nullable=False)
    score_key_word = db.Column(db.Float, nullable=False)   

# Création table 'reccurent_domain'
class ReccurentDomain(db.Model):
    __tablename__ = 'reccurent_domain'
    domain = db.Column(db.String(10000), nullable=False, primary_key=True)
    reccurent_nb = db.Column(db.Integer, nullable=False)

# Création table 'reccurent_ca'
class ReccurentCA(db.Model):
    __tablename__ = 'reccurent_ca'
    ca = db.Column(db.String(10000), nullable=False, primary_key=True)
    reccurent_nb = db.Column(db.Integer, nullable=False)

# Création database 'data' si non présente
if not path.exists('data.db'):
    with app.app_context():
        db.create_all()