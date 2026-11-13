from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from config import Config

# extensions

db = SQLAlchemy()
login_manager = LoginManager()
login_manager.login_view = 'main.login'


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # initialise extensions
    db.init_app(app)
    login_manager.init_app(app)

    # import blueprints / routes
    from . import routes  # registers blueprint inside routes
    app.register_blueprint(routes.bp)

    # create database tables if they don't exist
    with app.app_context():
        db.create_all()

    return app