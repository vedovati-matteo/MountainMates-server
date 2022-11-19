import os

from flask import Flask


def create_app(test_config=None):

    app = Flask(__name__)

    # a simple page that says hello
    @app.route('/')
    def hello():
        return 'Hello, World!'

    return app