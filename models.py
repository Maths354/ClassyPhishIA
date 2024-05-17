from os import path
from flask import Flask # type: ignore
from flask_sqlalchemy import SQLAlchemy # type: ignore

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
db = SQLAlchemy(app)

# Création table 'official_site'
class OfficalSite(db.Model):
    __tablename__ = 'official_site'
    id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.String(255), nullable=False)
    list_url = db.Column(db.String(255), nullable=False)
    logo = db.Column(db.String(255), nullable=False)
    key_word = db.Column(db.String(255), nullable=False)
    certificate = db.Column(db.String(255), nullable=False)
    template = db.Column(db.String(255), nullable=False)

    def __repr__(self):
        return f"<PhishingInfo {self.id}>"

# Création table 'phishing_site'
class PhishingSite(db.Model):
    __tablename__ = 'phishing_site'
    id = db.Column(db.Integer, primary_key=True)
    id_offical_site = db.Column(db.Integer, db.ForeignKey('official_site.id'))
    url = db.Column(db.String(255), nullable=False)
    list_url = db.Column(db.String(255), nullable=False)
    logo = db.Column(db.String(255), nullable=False)
    key_word = db.Column(db.String(255), nullable=False)
    certificate = db.Column(db.String(255), nullable=False)
    template = db.Column(db.String(255), nullable=False)


# Création table 'score'
class Score(db.Model):
    __tablename__ = 'score'
    id = db.Column(db.Integer, primary_key=True)
    id_phishing_site = db.Column(db.Integer, db.ForeignKey('phishing_site.id'))
    score_url = db.Column(db.String(255), nullable=False)
    score_certificate = db.Column(db.String(255), nullable=False)
    score_logo = db.Column(db.String(255), nullable=False)
    score_key_word = db.Column(db.String(255), nullable=False)   

# Création table 'reccurent_domain'
class ReccurentDomain(db.Model):
    __tablename__ = 'reccurent_domain'
    domain = db.Column(db.String(255), nullable=False, primary_key=True)
    reccurent_nb = db.Column(db.Integer, nullable=False)


# Création database 'data' si non présente
if not path.exists('data.db'):
    with app.app_context():
        db.create_all()