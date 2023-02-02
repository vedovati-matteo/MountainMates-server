from flask import request
from flask_restx import Namespace, Resource, fields
from ..service.auth_service import token_required
from ..service.utente_escursione_service import get_escursioni, save_new_iscrizione, delete_iscrizione, update_iscrizione, get_utenti

from .escursione_api import escursione_completa
from .utente_api import utente

api = Namespace('iscrizione', description='Azioni relative all\'iscrizione ad una Escursione')

id_escursione = api.model('id_escursione', {
    'id_escursione': fields.String(description='id escursione')
})

iscirzione_no_id = api.model('iscrizione no id', {
    'id_escursione': fields.String(description='id escursione'),
    'stato': fields.Integer(description='stato iscrizione'),
    'valutazione': fields.Integer(description='valutazione utente dell\'escursione')
        
})

escursione_utente_completa = api.inherit('escursione di utente completa', escursione_completa, {
    'id_firebase': fields.String(description='id utente iscritto'),
    'stato': fields.Integer(description='stato iscrizione'),
    'valutazione': fields.Integer(description='valutazione utente dell\'escursione')
})

utente_escursione_completa = api.inherit('utente di escursione completa', utente, {
    'id_escursione': fields.String(description='id escursione'),
    'stato': fields.Integer(description='stato iscrizione'),
    'valutazione': fields.Integer(description='valutazione utente dell\'escursione')
})

@api.route('/utente/self')
class UtenteList(Resource):
    @api.doc('Ottieni la lista di tutte le iscrizioni dell\'utente stesso')
    @api.marshal_list_with(escursione_utente_completa)
    @api.expect(None, validate = True)
    @token_required
    def get(req_id, self):
        """ Ottieni la lista di tutte le iscrizioni dell\'utente stesso """
        return get_escursioni(id=req_id)
    
    @api.doc('Iscrizione utente ad una Escursione')
    @api.expect(id_escursione, validate = True)
    @token_required
    def post(req_id, self):
        """ Iscrizione utente ad una Escursione """
        return save_new_iscrizione(id=req_id, data=request.json)
    
    @api.doc('Modifica iscrizone')
    @api.expect(iscirzione_no_id, validate = True)
    @token_required
    def put(req_id, self):
        """ Modifica iscrizone """
        return update_iscrizione(id=req_id, data=request.json)
    
    @api.doc('Rimozione iscrizione dell\'utente')
    @api.expect(id_escursione, validate = True)
    @token_required
    def delete(req_id, self):
        """ Rimozione iscrizione dell'utente """
        return delete_iscrizione(id=req_id, data=request.json)

@api.route('/utente/<id_firebase>')
@api.param('id_firebase', 'Identificatore firebase utente')
class Iscrizione(Resource):
    @api.doc('Ottieni la lista di tutte le iscrizioni dell\'utente specificato')
    @api.marshal_list_with(escursione_utente_completa)
    @api.expect(None, validate = True)
    @token_required
    def get(req_id, self, id_firebase):
        """ Ottieni la lista di tutte le iscrizioni dell\'utente specificato """
        return get_escursioni(id=id_firebase)

@api.route('/escursione/<id_escursione>')
@api.param('id_escursione', 'Identificatore escursione')
class Iscrizione(Resource):
    @api.doc('Ottieni la lista di tutti gli utenti iscritti ad una escursione')
    @api.marshal_list_with(utente_escursione_completa)
    @api.expect(None, validate = True)
    @token_required
    def get(req_id, self, id_escursione):
        """ Ottieni la lista di tutti gli utenti iscritti ad una escursione """
        return get_utenti(id=id_escursione)
    