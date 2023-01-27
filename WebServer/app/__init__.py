from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from firebase_admin import credentials
import firebase_admin

from .config import config_by_name

db = SQLAlchemy()
migrate = Migrate()
firebase_app = None

def create_app(config_name='dev'): # factory pattern
    app = Flask(__name__)
    app.config.from_object(config_by_name[config_name])
    #app.run(use_reloader=False)
    
    # Initialize Firebase admin SDK
    cred = credentials.Certificate('mountainmates-prova-firebase-adminsdk-nx3qa-c29fd7c82d.json')
    global firebase_app
    if firebase_app is None:
        firebase_app = firebase_admin.initialize_app(cred)

    # lazy init
    db.init_app(app)
    migrate.init_app(app, db)
    from app.api import api
    api.init_app(app)
    

    return app