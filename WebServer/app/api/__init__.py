from flask_restx import Api
from flask import Blueprint
import json

# Importing each API namespace (renamed files for clarity)
from .user_api import api as user_api
from .user_trip_api import api as user_trip_api
from .organize_api import api as organize_api
from .trip_api import api as trip_api
from .trip_template_api import api as trip_template_api

# Define the API instance with metadata
blueprint = Blueprint('api', __name__)

authorizations = {
    'Bearer Auth': {
        'type': 'apiKey',
        'in': 'header',
        'name': 'Authorization'
    }
}

api = Api(blueprint,
          title='MountainMates API',
          version='0.1',
          description='This API facilitates hiking trips, participant registration, and trip organization.',
          doc='/doc/',
          authorizations=authorizations
          )

# Adding all the defined namespaces to the main API
api.add_namespace(user_api)
api.add_namespace(user_trip_api)
api.add_namespace(organize_api)
api.add_namespace(trip_api)
api.add_namespace(trip_template_api)