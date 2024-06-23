import os

basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    DEBUG = True
    DEVELOPMENT = True
    SECRET_KEY = 'secret_key_test'
    FLASK_SECRET = SECRET_KEY
    SQLALCHEMY_DATABASE_URI = 'sqlite:///data.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
