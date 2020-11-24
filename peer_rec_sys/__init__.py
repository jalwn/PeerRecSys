from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from peer_rec_sys.config import Config


# SECRET_KEY protects against modifying cookies and cross site request forgery attacks and more stuff
# app.config is how you set config values for the application
# SECRET_KEY is supposed to be a random string
# Database something
# Update!: Loading the configuration for sqllite to app.cofig
# Creating the SQLAlchemy object by passing it the application
# Object contains all the functions and helpers from both sqlalchemy and sqlalchemy.orm
# Provides a class called Model that is a declarative base which can be used to declare models
db = SQLAlchemy()

bcrypt = Bcrypt()

login_manager = LoginManager()

login_manager.login_view = 'users.login'

def create_app(config_class=Config):

    app = Flask(__name__)
    app.config.from_object(config_class)
    with app.app_context():
        db.init_app(app)
        bcrypt.init_app(app)
        login_manager.init_app(app)

    from peer_rec_sys.users.routes import users
    from peer_rec_sys.main.routes import main
    app.register_blueprint(users)
    app.register_blueprint(main)

    return app

