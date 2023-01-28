from flask_restx import Api

# TODO set each http code (401, 403, ...) on every API
from .utente_api import api as api_utente
from .utente_escursione_api import api as api_utente_escursione
from .organizza_api import api as api_organizza
from .escursione_api import api as api_escursione
from .escursione_template_api import api as api_escursione_template

api = Api(
    title = 'MountainMates API',
    version = '0.1',
    description=  'Web Application di MountainMates', # TODO aggungere descrizione
)

api.add_namespace(api_utente)
api.add_namespace(api_utente_escursione)
api.add_namespace(api_organizza)
api.add_namespace(api_escursione)
api.add_namespace(api_escursione_template)