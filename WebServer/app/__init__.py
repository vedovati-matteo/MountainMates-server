from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate


from .config import config_by_name

db = SQLAlchemy()
migrate = Migrate()

def create_app(config_name='dev'): # factory pattern
    app = Flask(__name__)
    app.config.from_object(config_by_name[config_name])
    # lazy init
    db.init_app(app)
    migrate.init_app(app, db)
    from app.api import api
    api.init_app(app)

    return app