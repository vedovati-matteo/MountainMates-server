from os import environ, path, pardir
from dotenv import load_dotenv


currdir = path.dirname(__file__)
basedir = path.abspath(path.join(currdir, pardir))
load_dotenv(path.join(basedir, '.env'))
    
class Config: # Base config
    pass


class DevelopmentConfig(Config):
    # uncomment the line below to use postgres
    # SQLALCHEMY_DATABASE_URI = postgres_local_base
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = environ.get('DATABASE_URL')
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class TestingConfig(Config):
    DEBUG = True
    TESTING = True
    #SQLALCHEMY_DATABASE_URI = 'sqlite:///' + path.join(basedir, 'database_test.db')
    SQLALCHEMY_DATABASE_URI = 'sqlite:////tmp/database_test.db'
    PRESERVE_CONTEXT_ON_EXCEPTION = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class ProductionConfig(Config):
    DEBUG = False
    # uncomment the line below to use postgres
    # SQLALCHEMY_DATABASE_URI = postgres_local_base


config_by_name = dict(
    dev=DevelopmentConfig,
    test=TestingConfig,
    prod=ProductionConfig
)