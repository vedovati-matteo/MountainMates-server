from flask_restx import Api

from .utente_api import api as api_utente

api = Api(
    title = 'MountainMates',
    version = '0.0',
    description=  'Descrizione ... ',
)

api.add_namespace(api_utente)