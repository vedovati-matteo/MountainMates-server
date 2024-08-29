"""
This module manages the Flask application, including database creation, migrations, and running tests.
"""

import os
import unittest
import json

from flask.cli import FlaskGroup

from app import create_app, db, migrate

# Create the Flask app instance based on the environment variable or default to 'dev'
app = create_app('dev') 
app.app_context().push()  # Push an application context to make `db` and `migrate` available

# Create a FlaskGroup to manage CLI commands
cli = FlaskGroup(app)


@cli.command('test')
def run_tests():
    """Runs the unit tests."""
    tests = unittest.TestLoader().discover('tests', pattern='test*.py')  # Assuming tests are in a 'tests' folder
    result = unittest.TextTestRunner(verbosity=2).run(tests)
    if result.wasSuccessful():
        return 0
    return 1


@cli.command('create_db')
def create_database():
    """Creates the database tables."""
    db.create_all()


@cli.command('migrate')
def generate_migration():
    """Generates a new database migration."""
    migrate.generate()


@cli.command('upgrade')
def apply_migrations():
    """Applies the latest database migrations."""
    migrate.upgrade()

            
if __name__ == '__main__':
    cli()