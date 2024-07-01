import os

basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = os.urandom(24) #'secret_key_test'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///data.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

class Dev(Config):
    DEBUG = True
    DEVELOPMENT = True

class Prod(Config):
    DEBUG = False
    DEVELOPMENT = False