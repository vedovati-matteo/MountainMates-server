from flask_restx import Api
from flask import Blueprint

# Importing each API namespace
from .utente_api import api as api_utente
from .utente_escursione_api import api as api_utente_escursione
from .organizza_api import api as api_organizza
from .escursione_api import api as api_escursione
from .escursione_template_api import api as api_escursione_template

# Define the API instance with metadata
blueprint = Blueprint('api', __name__)

api = Api(blueprint,
    title='MountainMates API',
    version='0.1',
    description='This API is part of the MountainMates web application, which facilitates hiking trips, participant registration, and trip organization.',
    doc='/doc/'  # This enables Swagger UI at /api/doc/
)

# Adding all the defined namespaces to the main API
api.add_namespace(api_utente)
api.add_namespace(api_utente_escursione)
api.add_namespace(api_organizza)
api.add_namespace(api_escursione)
api.add_namespace(api_escursione_template)