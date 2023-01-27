from flask import request
from flask_restx import Namespace, Resource, fields
from ..service.auth_service import token_required
from ..service.organizza_service import get_escursioni, save_new_organizza, delete_organizza, get_organizzatori

from .escursione_api import escursione_completa
from .utente_api import utente

api = Namespace('organizza', description='Azioni relative agli organizzatori di una Escursione')

id_escursione = api.model('id_escursione', {
    'id_escursione': fields.String(description='id escursione')
})

@api.route('/utente/<id_organizzatore>')
@api.param('id_organizzatore', 'Identificatore firebase utente')
class Iscrizione(Resource):
    @api.doc('Ottieni la lista di tutte le escursioni organizzate dall\'organizzatore specificato')
    @api.marshal_list_with(escursione_completa)
    @api.expect(None, validate = True)
    @token_required
    def get(req_id, self, id_organizzatore):
        """ Ottieni la lista di tutte le escursioni organizzate dall\'organizzatore specificato """
        return get_escursioni(id=id_organizzatore)
    
    @api.doc('Assegnazione escursione ad organizzatore')
    @api.expect(id_escursione, validate = True)
    @token_required
    def post(req_id, self, id_organizzatore):
        """ Assegnazione escursione ad organizzatore """
        return save_new_organizza(id=id_organizzatore, data=request.json)
    
    @api.doc('Rimozione escursione da organizzatore')
    @api.expect(id_escursione, validate = True)
    @token_required
    def delete(req_id, self, id_organizzatore):
        """ Rimozione escursione da organizzatore """
        return delete_organizza(id=id_organizzatore, data=request.json)

@api.route('/escursione/<id_escursione>')
@api.param('id_escursione', 'Identificatore escursione')
class Iscrizione(Resource):
    @api.doc('Ottieni la lista di tutti gli organizzatori di un escursione')
    @api.marshal_list_with(utente)
    @api.expect(None, validate = True)
    @token_required
    def get(req_id, self, id_escursione):
        """ Ottieni la lista di tutti gli organizzatori di un escursione """
        return get_organizzatori(id=id_escursione)
    