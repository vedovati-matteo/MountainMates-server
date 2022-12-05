from flask_restx import Api

from .utente_api import api as api_utente
from .utente_escursione_api import api as api_utente_escursione

api = Api(
    title = 'MountainMates API',
    version = '0.0',
    description=  'Descrizione ... ', # TODO aggungere descrizione
)

api.add_namespace(api_utente)
api.add_namespace(api_utente_escursione)