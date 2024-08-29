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

    # Generate Swagger JSON
    @app.before_first_request
    def generate_swagger():
        logger.debug("==-- Start Swagger documentation generation --==")
        with app.app_context():
            api = None
            for extension in app.extensions.values():
                if isinstance(extension, Api):
                    api = extension
                    break
            
            if api is not None:
                try:
                    swagger_json = api.__schema__
                    
                    # Ensure the static directory exists
                    static_dir = os.path.join(app.root_path, 'static')
                    os.makedirs(static_dir, exist_ok=True)
                    
                    # Save Swagger JSON
                    with open(os.path.join(static_dir, 'swagger.json'), 'w') as f:
                        json.dump(swagger_json, f, indent=2)
                    
                    logger.info("Swagger JSON saved to static/swagger.json")
                    
                    # Generate HTML file that loads Swagger UI
                    html_content = """
                    <!DOCTYPE html>
                    <html lang="en">
                    <head>
                        <meta charset="UTF-8">
                        <title>Swagger UI</title>
                        <link rel="stylesheet" type="text/css" href="https://cdnjs.cloudflare.com/ajax/libs/swagger-ui/3.52.0/swagger-ui.css" >
                        <script src="https://cdnjs.cloudflare.com/ajax/libs/swagger-ui/3.52.0/swagger-ui-bundle.js"></script>
                    </head>
                    <body>
                        <div id="swagger-ui"></div>
                        <script>
                            window.onload = function() {
                                SwaggerUIBundle({
                                    url: "swagger.json",
                                    dom_id: '#swagger-ui',
                                    presets: [
                                        SwaggerUIBundle.presets.apis,
                                        SwaggerUIBundle.SwaggerUIStandalonePreset
                                    ],
                                    layout: "BaseLayout"
                                })
                            }
                        </script>
                    </body>
                    </html>
                    """
                    
                    with open(os.path.join(static_dir, 'swagger.html'), 'w') as f:
                        f.write(html_content)
                    
                    logger.info("Swagger UI HTML saved to static/swagger.html")
                except Exception as e:
                    logger.error(f"Error generating Swagger documentation: {str(e)}")
            else:
                logger.warning("Could not find Flask-RESTX Api instance. Swagger documentation not generated.")
        
        logger.info("Swagger documentation generation process completed.")
    
    return app