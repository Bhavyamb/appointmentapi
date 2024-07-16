import os

class Config:
    # Flask App Configuration
    DEBUG = True  # Set to False in production
    #SECRET_KEY = 'your_secret_key_here'  # Replace with a secure random key

    # SQLAlchemy Configuration
    SQLALCHEMY_DATABASE_URI = 'postgresql://admin:password@localhost/appoinments'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
