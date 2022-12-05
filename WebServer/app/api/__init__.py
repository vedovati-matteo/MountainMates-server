from flask_restx import Api

from .utente_api import api as api_utente
from .utente_escursione_api import api as api_utente_escursione
from .escursione_api import api as api_escursione
from .escursione_template_api import api as api_escursione_template

api = Api(
    title = 'MountainMates API',
    version = '0.0',
    description=  'Descrizione ... ', # TODO aggungere descrizione
)

api.add_namespace(api_utente)
api.add_namespace(api_utente_escursione)
api.add_namespace(api_escursione)
api.add_namespace(api_escursione_template)