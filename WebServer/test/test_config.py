from  os import path
import unittest
from re import sub

from flask import current_app
from flask_testing import TestCase

from manage import app
from app.config import basedir

def getEnvDic(dotenvPath): # get dict of variables stored in the .env file
    with open(dotenvPath, 'r') as fh:
        vars_dict = dict(
            tuple(sub('\'', '', line).replace('\n', '').split('='))
            for line in fh.readlines() if not line.startswith('#')
        )
        return vars_dict

vars_dict = getEnvDic(path.join(basedir, '.env'));

class TestDevelopmentConfig(TestCase):
    def create_app(self):
        app.config.from_object('app.config.DevelopmentConfig')
        return app

    def test_app_is_development(self):
        self.assertFalse(app.config['SECRET_KEY'] is vars_dict.get('SECRET_KEY'))
        self.assertTrue(app.config['DEBUG'] is True)
        self.assertFalse(current_app is None)
        self.assertTrue(
            app.config['SQLALCHEMY_DATABASE_URI'] == 'sqlite:///' + path.join(basedir, 'database_main.db')
        )


class TestTestingConfig(TestCase):
    def create_app(self):
        app.config.from_object('app.config.TestingConfig')
        return app

    def test_app_is_testing(self):
        self.assertFalse(app.config['SECRET_KEY'] is vars_dict.get('SECRET_KEY'))
        self.assertTrue(app.config['DEBUG'])
        self.assertTrue(
            app.config['SQLALCHEMY_DATABASE_URI'] == 'sqlite:///' + path.join(basedir, 'database_test.db')
        )


class TestProductionConfig(TestCase):
    def create_app(self):
        app.config.from_object('app.config.ProductionConfig')
        return app

    def test_app_is_production(self):
        self.assertTrue(app.config['DEBUG'] is False)


if __name__ == '__main__':
    unittest.main()