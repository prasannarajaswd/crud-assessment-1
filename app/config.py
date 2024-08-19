import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# class Config:
#     SECRET_KEY = os.getenv('SECRET_KEY', 'default_secret_key')
#     SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL')
#     SQLALCHEMY_TRACK_MODIFICATIONS = False

#     @staticmethod
#     def init_app(app):
#         pass

# class DevelopmentConfig(Config):
#     DEBUG = True

# class ProductionConfig(Config):
#     DEBUG = False

# # Determine the configuration based on FLASK_DEBUG
# debug_mode = os.getenv('FLASK_DEBUG', '0') == '1'
# config = {
#     True: DevelopmentConfig,
#     False: ProductionConfig
# }.get(debug_mode, ProductionConfig)

import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'my_precious_secret_key')
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'sqlite:///:memory:')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    @staticmethod
    def init_app(app):
        pass

class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'sqlite:///dev.db')

class TestingConfig(Config):
    DEBUG = True
    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_TEST_URL', 'sqlite:///:memory:')
    PRESERVE_CONTEXT_ON_EXCEPTION = False

class ProductionConfig(Config):
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'sqlite:///prod.db')

# Mapping of configuration names to config classes
config_by_name = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig  # Default configuration if none is provided
}

# Dynamic selection of config based on FLASK_DEBUG
debug_mode = os.getenv('FLASK_DEBUG', '0') == '1'
config = config_by_name.get('development' if debug_mode else 'production')

