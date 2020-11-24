import os

class Config:

    SECRET_KEY = os.environ.get('SECRET_KEY')
    # Database something
    # Update!: Loading the configuration for sqllite to app.cofig
    SQLALCHEMY_DATABASE_URI = os.environ.get('SQLALCHEMY_DATABASE_URI')