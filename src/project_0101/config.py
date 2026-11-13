import os

class Config:
    # Secret key for JWT signing
    SECRET_KEY = os.getenv('SECRET_KEY', 'change_this_to_a_random_secret')
    # Bcrypt configuration
    BCRYPT_LOG_ROUNDS = 12
    # Database configuration (SQLite for simplicity)
    SQLALCHEMY_DATABASE_URI = 'sqlite:///users.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
