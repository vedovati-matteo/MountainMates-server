from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_restx import Api

from .config import config_by_name

db = SQLAlchemy()
migrate = Migrate()
api = Api()

def create_app(config_name='dev'): # factory pattern
    app = Flask(__name__)
    app.config.from_object(config_by_name[config_name])
    # lazy init
    db.init_app(app)
    migrate.init_app(app, db)
    api.init_app(app)

    return app