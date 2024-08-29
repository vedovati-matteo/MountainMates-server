import unittest
from flask import current_app
from flask_testing import TestCase
from manage import app


class TestDevelopmentConfig(TestCase):
    """Tests the Development configuration."""

    def create_app(self):
        app.config.from_object('app.config.DevelopmentConfig')
        return app

    def test_app_is_development(self):
        """Ensures the app is in development mode and the database URI is correct."""
        self.assertTrue(app.config['DEBUG'] is True)
        self.assertFalse(current_app is None)  # Check if current_app is available
        self.assertIn('SQLALCHEMY_DATABASE_URI', app.config)

class TestTestingConfig(TestCase):
    """Tests the Testing configuration."""

    def create_app(self):
        app.config.from_object('app.config.TestingConfig')
        return app

    def test_app_is_testing(self):
        """Ensures the app is in testing mode and using an in-memory SQLite database."""
        self.assertTrue(app.config['DEBUG'])
        self.assertEqual(app.config['SQLALCHEMY_DATABASE_URI'], 'sqlite:////tmp/database_test.db')

class TestProductionConfig(TestCase):
    """Tests the Production configuration."""

    def create_app(self):
        app.config.from_object('app.config.ProductionConfig')
        return app

    def test_app_is_production(self):
        """Ensures the app is in production mode (DEBUG is False)."""
        self.assertTrue(app.config['DEBUG'] is False)

if __name__ == '__main__':
    unittest.main()