from flask_testing import TestCase
from app import db  # Assuming 'app' is your Flask application instance
from manage import app  # Assuming 'manage.py' is where you create your app

class BaseTestCase(TestCase):
    """Base class for all test cases. Provides common setup and teardown methods."""

    def create_app(self):
        """Creates and configures the Flask app for testing."""
        app.config.from_object('app.config.TestingConfig')  # Use TestingConfig
        return app

    def setUp(self):
        """Sets up the database before each test."""
        db.create_all()  # Create all database tables
        db.session.commit()  # Commit any pending changes

    def tearDown(self):
        """Cleans up the database after each test."""
        db.session.remove()  # Remove the current session
        db.drop_all()  # Drop all database tables