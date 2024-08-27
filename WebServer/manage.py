"""
This module contains the main of the web app
"""
import os
import unittest

from flask.cli import FlaskGroup

from app import create_app, db, migrate

app = create_app(os.getenv('BOILERPLATE_ENV') or 'dev')
app.app_context().push()

cli = FlaskGroup(app)

@cli.command('test')
def test():
    """Runs the unit tests."""
    tests = unittest.TestLoader().discover('test', pattern='test*.py')
    result = unittest.TextTestRunner(verbosity=2).run(tests)
    if result.wasSuccessful():
        return 0
    return 1

@cli.command('db_create')
def db_create():
    """Creates the database tables."""
    db.create_all()

@cli.command('db_migrate')
def db_migrate():
    """Generates a new database migration."""
    migrate.generate()

@cli.command('db_upgrade')
def db_upgrade():
    """Applies the latest database migrations."""
    migrate.upgrade()

if __name__ == '__main__':
    cli()