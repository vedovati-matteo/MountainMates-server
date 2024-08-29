from os import environ, path
import logging
from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from firebase_admin import credentials, initialize_app
from flask_restx import Api

import json
import os

from .config import config_by_name 

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Initialize extensions (but not yet configured)
db = SQLAlchemy()
migrate = Migrate()
firebase_app = None  # Global Firebase app instance


def create_app(config_name='dev'):
    """
    Application factory function to create and configure a Flask application instance.
    """

    app = Flask(__name__)
    app.config.from_object(config_by_name[config_name])

    # Initialize Firebase app (only once)
    global firebase_app
    if firebase_app is None:
        try:
            cred_path = environ.get('FIREBASE_CREDENTIALS_PATH')
            cred = credentials.Certificate(cred_path)
            firebase_app = initialize_app(cred)
        except Exception as e:
            logger.error(f"Failed to initialize Firebase app: {str(e)}")
            raise

    # Configure extensions with the app instance
    db.init_app(app)
    migrate.init_app(app, db)

    # Register blueprints (APIs)
    from .api import blueprint
    app.register_blueprint(blueprint, url_prefix='/api')

    # Centralized error handling (example)
    @app.errorhandler(Exception)
    def default_error_handler(e):
        return jsonify(error=str(e)), getattr(e, 'code', 500)
    
    return app