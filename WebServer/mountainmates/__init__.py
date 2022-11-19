import os

from flask import Flask, jsonify


def create_app(test_config=None):

    app = Flask(__name__, instance_relative_config=True)

    # a simple page that says hello
    @app.route('/')
    def hello():
        return 'Hello, World!'

    return app