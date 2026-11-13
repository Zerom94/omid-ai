import os

class Config:
    SECRET_KEY = os.getenv('FLASK_SECRET_KEY', 'this-should-be-changed')
    SQLALCHEMY_DATABASE_URI = 'sqlite:///site.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False