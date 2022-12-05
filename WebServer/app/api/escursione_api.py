from flask import request
from flask_restx import Namespace, Resource, fields

from ..service.escursione_service import get_all_escursioni, save_new_escursione, get_escursione_self

api = Namespace('escursione', description='Azioni della classe template')

escursione = api.model('escursione completa', {
    'id_escursione': fields.Integer(description='trip id'),
    'nome': fields.String(description= 'user name'),
    'id_organizzatore': fields.String(description='guide id'),
    'data': fields.Date(dt_format='rfc822', description = 'date of the trip'),
    'provincia': fields.String(description= 'province of the trip'),
    'partenza':fields.String(description= 'starting of the trip'),
    'mapLink': fields.String(description= 'starting of the trip'),
    'dislivello': fields.Integer(description='difference in altitude'), 
    'distanza': fields.Float(description='distance'),
    'tempo_stimato': fields.String(description= 'time of the trip'),
    'altezza_min': fields.Integer(description='min altitude'),
    'altezza_max': fields.Integer(description='max altitude'),
    'difficulty': fields.Integer(descrription='difficulty of the trio'),
    'strumenti_richiesti':fields.String(description= 'required tools'),
    'descrizione_percorso': fields.String(description='path_description'),
    'max_participant':fields.Integer(description='maximum number of participants'),
})


@api.route('/')
class UtenteList(Resource):
    @api.doc('Lista di tutte le escursioni')
    @api.marshal_list_with(escursione)
    @api.expect(None, validate = True)
    def get(self):
        """ Ottieni la lista di tutte le escursioni che sono nel database """
        return get_all_escursioni(data=request)
    
    @api.doc('Creazione di un nuovo utente')
    @api.expect(escursione, validate = True)
    def post(self):
        """ Aggungi al database un nuovo utente """
        return save_new_escursione(data=request)

@api.route('/self')
class UtenteSelf(Resource):
    @api.doc('Ottinei dati dell\'utente stesso')
    #Da chiedere a Vedo questa riga
    #@api.marshal_with(utente_create)
    @api.expect(None, validate = True)
    def get(self):
        """Ottieni i dati di un'escursione specifica """
        return get_escursione_self(data=request)
