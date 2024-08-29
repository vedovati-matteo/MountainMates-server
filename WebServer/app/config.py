import os
from dotenv import load_dotenv

import logging
# Configure Flask's logger
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

currdir = os.path.dirname(__file__)
basedir = os.path.abspath(os.path.dirname(currdir))  # Go one level up from currdir
load_dotenv(os.path.join(basedir, '.env')) 

class Config:
    """Base configuration class."""
    pass


class DevelopmentConfig(Config):
    """Development configuration."""
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class TestingConfig(Config):
    """Testing configuration."""
    DEBUG = True
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:////tmp/database_test.db'  # In-memory SQLite for testing
    PRESERVE_CONTEXT_ON_EXCEPTION = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class ProductionConfig(Config):
    """Production configuration."""
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
    SQLALCHEMY_TRACK_MODIFICATIONS = False


# Dictionary to map configuration names to their respective classes
config_by_name = dict(
    dev=DevelopmentConfig,
    test=TestingConfig,
    prod=ProductionConfig
)