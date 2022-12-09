from flask import request
from flask_restx import Namespace, Resource, fields

from ..service.escursione_service import get_all_escursioni, save_new_escursione, get_escursione_self

from .escursione_template_api import escursione_template 
from .utente_api import utente

api = Namespace('escursione', description='Azioni su Escursione')

escursione_completa = api.inherit('escursione completa', escursione_template, {
    'id_escursione': fields.Integer(description='escursion id'),
    'id_escursione_template': fields.Integer(description='template id'),
    'orario_ritrovo': fields.String(description='meeting time'),
    'data': fields.Date(dt_format='rfc822', description = 'date of the trip'),
    'max_participant':fields.Integer(description='maximum number of participants'),
    'organizzatori': fields.List(fields.Nested(utente))
})

escursione = api.model('escursione api', {
    'id_escursione': fields.Integer(description='escursion id'),
    'id_escursione_template': fields.Integer(description='template id'),
    'orario_ritrovo': fields.String(description='meeting time'),
    'data': fields.Date(dt_format='rfc822', description = 'date of the trip'),
    'max_participant':fields.Integer(description='maximum number of participants'),
    'organizzatori': fields.List(fields.Nested(utente))
})

escursioneIdOrg = api.model('lista dei nickname degli organizzatori', {
    'id_escursione': fields.Integer(description='escursion id'),
    'id_escursione_template': fields.Integer(description='template id'),
    'orario_ritrovo': fields.String(description='meeting time'),
    'data': fields.Date(dt_format='rfc822', description = 'date of the trip'),
    'max_participant':fields.Integer(description='maximum number of participants'),
    'organizzatori': fields.List(fields.String(description='id organizzatore'))
})

@api.route('/')
class EscursioniList(Resource):
    @api.doc('Lista di tutte le escursioni')
    @api.marshal_list_with(escursione_completa)
    @api.expect(None, validate = True)
    def get(self):
        """ Ottieni la lista di tutte le escursioni che sono nel database """
        return get_all_escursioni(data=request)
    
    @api.doc('Creazione nuova escursione')
    @api.expect(escursioneIdOrg, validate = True)
    def post(self):
        """ Aggungi al database una nuova escursione """
        return save_new_escursione(data=request)
    
@api.route('/<id_escursione>')
@api.param('id_escursione', 'Identificatore dell\'escursione')
class Escursione(Resource):
    @api.doc('Ottieni l\'escursione specificata')
    @api.marshal_with(escursione_completa)
    @api.expect(None, validate = True)
    def get(self, id_escursione):
        """ Ottieni l'escursione specificata """
        return

@api.route('fromTemplate/<id_escursione_template>')
@api.param('id_escursione_template', 'Identificatore del template')
class EscursioniListDaTemplate(Resource):
    @api.doc('Ottieni la lista di tutte le escursioni di uno specifico template')
    @api.marshal_list_with(escursione_completa)
    @api.expect(None, validate = True)
    def get(self, id_escursione_template):
        """ Ottieni la lista di tutte le escursioni di uno specifico template """
        return