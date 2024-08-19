import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_swagger_ui import get_swaggerui_blueprint
from app.config import config
from flask_migrate import Migrate
from app.models import db
from app.config import config_by_name 

migrate = Migrate()

# def create_app():
#     app = Flask(__name__)
#     app.config.from_object(config)

#     db.init_app(app)
#     migrate.init_app(app, db)

#     # Register blueprints
#     from app.routes.book_routes import book_bp
#     from app.routes.user_routes import user_bp

#     app.register_blueprint(book_bp, url_prefix='/api')
#     app.register_blueprint(user_bp, url_prefix='/api')

#     # Swagger UI setup
#     SWAGGER_URL = '/api/docs'  # URL for accessing Swagger UI
#     API_URL = '/static/swagger.json'  # Path to your Swagger specification file

#     swaggerui_blueprint = get_swaggerui_blueprint(
#         SWAGGER_URL, 
#         API_URL,
#         config={  # Swagger UI config overrides
#             'app_name': "Prasanna Assessment JKTECH"
#         }
#     )

#     app.register_blueprint(swaggerui_blueprint, url_prefix=SWAGGER_URL)

#     return app

def create_app(config_name='default'):
    app = Flask(__name__)
    app.config.from_object(config_by_name[config_name])  # Load configuration based on the config_name

    db.init_app(app)
    migrate.init_app(app, db)

    # Register blueprints
    from app.routes.book_routes import book_bp
    from app.routes.user_routes import user_bp

    app.register_blueprint(book_bp, url_prefix='/api')
    app.register_blueprint(user_bp, url_prefix='/api')

    # Swagger UI setup
    SWAGGER_URL = '/api/docs'
    API_URL = '/static/swagger.json'
    
    swaggerui_blueprint = get_swaggerui_blueprint(
        SWAGGER_URL, 
        API_URL,
        config={ 
            'app_name': "Prasanna Assessment JKTECH"
        }
    )

    app.register_blueprint(swaggerui_blueprint, url_prefix=SWAGGER_URL)

    return app