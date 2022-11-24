import os
import unittest

from flask.cli import FlaskGroup

from app import create_app

app = create_app(os.getenv('BOILERPLATE_ENV') or 'dev')

app.app_context().push()

cli = FlaskGroup(app)

@cli.command('test')
def test():
    """Runs the unit tests."""
    tests = unittest.TestLoader().discover('test', pattern='test*.py') # get all tests
    result = unittest.TextTestRunner(verbosity=2).run(tests)
    if result.wasSuccessful():
        return 0
    return 1

if __name__ == '__main__':
    cli()