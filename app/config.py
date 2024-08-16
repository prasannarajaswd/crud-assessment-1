import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'default_secret_key')
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    @staticmethod
    def init_app(app):
        pass

class DevelopmentConfig(Config):
    DEBUG = True

class ProductionConfig(Config):
    DEBUG = False

# Determine the configuration based on FLASK_DEBUG
debug_mode = os.getenv('FLASK_DEBUG', '0') == '1'
config = {
    True: DevelopmentConfig,
    False: ProductionConfig
}.get(debug_mode, ProductionConfig)