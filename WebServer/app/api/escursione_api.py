from flask import request
from flask_restx import Namespace, Resource, fields
from ..service.auth_service import token_required, organizzatore_required
from ..service.escursione_service import get_all_escursioni, save_new_escursione, save_new_escursione_no_template, get_escursione, put_escursione, delete_escursione, get_all_escursioni_template

from .escursione_template_api import escursione_template, escursione_template_no_id
from .utente_api import utente

api = Namespace('escursione', description='Azioni su Escursione')

escursione_completa = api.inherit('escursione completa', escursione_template, {
    'id_escursione': fields.String(description='escursion id'),
    'orario_ritrovo': fields.String(description='meeting time'),
    'data': fields.Date(dt_format='rfc822', description = 'date of the trip'),
    'numero_max':fields.Integer(description='maximum number of participants'),
})

escursione_no_id = api.model('escursione no id', {
    'id_escursione_template': fields.String(description='template id'),
    'orario_ritrovo': fields.String(description='meeting time'),
    'data': fields.Date(dt_format='rfc822', description = 'date of the trip'),
    'numero_max':fields.Integer(description='maximum number of participants'),
})

escursione_completa_no_id = api.inherit('escursione completa no id', escursione_template_no_id, {
    'orario_ritrovo': fields.String(description='meeting time'),
    'data': fields.Date(dt_format='rfc822', description = 'date of the trip'),
    'numero_max':fields.Integer(description='maximum number of participants'),
})

escursione_id = api.model('id escursione', {
    'id_escursione': fields.String(description='id escursione')
})

@api.route('/')
class EscursioniList(Resource):
    @api.doc('Lista di tutte le escursioni')
    @api.marshal_list_with(escursione_completa)
    @api.expect(None, validate = True)
    @token_required
    def get(req_id, self):
        """ Ottieni la lista di tutte le escursioni che sono nel database """
        return get_all_escursioni()
    
    @api.doc('Creazione nuova escursione')
    @api.marshal_with(escursione_id)
    @api.expect(escursione_no_id, validate = True)
    @token_required
    @organizzatore_required
    def post(req_id, self):
        """ Aggungi al database una nuova escursione """
        return save_new_escursione(data=request.json)

@api.route('/noTemplate')
class EscursioniList(Resource):
    @api.doc('Creazione nuova escursione e template')
    @api.marshal_with(escursione_id)
    @api.expect(escursione_completa_no_id, validate = True)
    @token_required
    @organizzatore_required
    def post(req_id, self):
        """ Aggungi al database una nuova escursione e nuovo template (template non specificato) """
        return save_new_escursione_no_template(data=request.json)

@api.route('/<id_escursione>')
@api.param('id_escursione', 'Identificatore dell\'escursione')
class Escursione(Resource):
    @api.doc('Ottieni l\'escursione specificata')
    @api.marshal_with(escursione_completa)
    @api.expect(None, validate = True)
    @token_required
    def get(req_id, self, id_escursione):
        """ Ottieni l'escursione specificata """
        return get_escursione(id=id_escursione)
    
    @api.doc('Modifica l\'escursione specificata')
    @api.expect(escursione_no_id, validate = True)
    @token_required
    @organizzatore_required
    def put(req_id, self, id_escursione):
        """ Modifica l\'escursione specificata """
        return put_escursione(id=id_escursione, data=request.json)
    
    @api.doc('Elimina l\'escursione specificata')
    @api.expect(None, validate = True)
    @token_required
    @organizzatore_required
    def delete(req_id, self, id_escursione):
        """ Elimina l'escursione specificata """
        return delete_escursione(id=id_escursione)

@api.route('/fromTemplate/<id_escursione_template>')
@api.param('id_escursione_template', 'Identificatore del template')
class EscursioniListDaTemplate(Resource):
    @api.doc('Ottieni la lista di tutte le escursioni di uno specifico template')
    @api.marshal_list_with(escursione_completa)
    @api.expect(None, validate = True)
    @token_required
    def get(req_id, self, id_escursione_template):
        """ Ottieni la lista di tutte le escursioni di uno specifico template """
        return get_all_escursioni_template(id=id_escursione_template)
