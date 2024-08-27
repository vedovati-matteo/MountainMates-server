from os import environ
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from firebase_admin import credentials

import firebase_admin
from flask import jsonify

from .config import config_by_name

# Initialize Firebase admin SDK
cred = credentials.Certificate(environ.get('FIREBASE_CREDENTIALS_PATH'))

db = SQLAlchemy()
migrate = Migrate()
firebase_app = None

def create_app(config_name='dev'): # factory pattern
    app = Flask(__name__)
    app.config.from_object(config_by_name[config_name])
    
    global firebase_app
    if firebase_app is None:
        firebase_app = firebase_admin.initialize_app(cred)

    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)

    # Register blueprints
    from .api import blueprint
    app.register_blueprint(blueprint, url_prefix='/api') 

    # Centralized error handling (example)
    @app.errorhandler(Exception)
    def default_error_handler(e):
        return jsonify(error=str(e)), getattr(e, 'code', 500)

    return app