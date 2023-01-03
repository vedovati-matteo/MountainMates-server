from flask import request
from flask_restx import Namespace, Resource, fields

from ..service.escursione_template_service import get_all_escursioni_template, save_new_escursione_template


api = Namespace('escursione_template', description='Azioni su Template')

escursione_template_no_id = api.model('template dell\'escursione senza id', {
    'nome': fields.String(description= 'user name'),
    'provincia': fields.String(description= 'province of the trip'),
    'partenza':fields.String(description= 'starting of the trip'),
    'mapLink': fields.String(description= 'starting of the trip'),
    'dislivello': fields.Integer(description='difference in altitude'), 
    'distanza': fields.Float(description='distance'),
    'tempo_stimato': fields.String(description= 'time of the trip'),
    'altezza_min': fields.Integer(description='min altitude'),
    'altezza_max': fields.Integer(description='max altitude'),
    'difficulty': fields.Integer(description='difficulty of the trio'),
    'strumenti_richiesti':fields.String(description= 'required tools'),
    'descrizione_percorso': fields.String(description='path_description'),
    'img':fields.String(description='picture of the escursion')
})

escursione_template = api.inherit( 'template dell\'escursione completa', escursione_template_no_id, {
    'id_escursione_template': fields.Integer(description='trip id')
})

#Nel secondo modello metto tutto tranne id escursione

@api.route('/')
class EscursioneTemplateList(Resource):
    @api.doc('Lista di tutte le escursioni')
    @api.marshal_list_with(escursione_template)
    @api.expect(None, validate = True)
    def get(self):
        """ Ottieni la lista di tutti i template di escursiono che sono nel database """
        return get_all_escursioni_template(data=request)
    
    @api.doc('Creazione di un nuovo template di un \' escursione')
    @api.expect(escursione_template_no_id, validate = True)
    def post(self):
        """ Aggungi al database un nuovo template """
        return save_new_escursione_template(data=request)

@api.route('/<id_escursione_template>')
@api.param('id_escursione_template', 'Identificatore template dell\'escursione')
class escursioneTemplate(Resource):
    @api.doc('Ottieni il teplate specificato')
    @api.marshal_with(escursione_template)
    @api.expect(None, validate = True)
    def get(self, id_escursione_template):
        """ Ottieni il teplate specificato """
        return
