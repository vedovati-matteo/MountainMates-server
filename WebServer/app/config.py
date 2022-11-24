from os import environ, path, pardir
from dotenv import load_dotenv

# uncomment the line below for postgres database url from environment variable
# postgres_local_base = environ.get('DATABASE_URL')
#note postegers format: postgresql://username:password@host:port/database_name

currdir = path.dirname(__file__)
basedir = path.abspath(path.join(currdir, pardir))
load_dotenv(path.join(basedir, '.env'))
    
class Config: # Base config
    SECRET_KEY = environ.get('SECRET_KEY')


class DevelopmentConfig(Config):
    # uncomment the line below to use postgres
    # SQLALCHEMY_DATABASE_URI = postgres_local_base
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + path.join(basedir, 'database_main.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class TestingConfig(Config):
    DEBUG = True
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + path.join(basedir, 'database_test.db')
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

key = Config.SECRET_KEY