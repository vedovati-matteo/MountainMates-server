from flask import request
from flask_restx import Namespace, Resource, fields
from ..service.utente_service import get_all_utenti, save_new_utente, get_utente_self 

api = Namespace('utente', description='Azioni relative all\'utente')

utente = api.model('utente_completo', {
    'id_firebase': fields.String(description='user Identifier'),
    'nome': fields.String(description='user name'),
    'cognome': fields.String(description='user surname'),
    'data_di_nascita': fields.Date(dt_format='rfc822'),
    'nickname': fields.String(description='user nickname'),
    'numero_amici': fields.Integer(description='number of friends'),
    'bio': fields.String(description= 'user bio'),
    'flag_organizzatore': fields.Boolean(description= 'if the user is a mountain guide'),
    'livello_camminatore': fields.Integer(description='level ability'),
    'img': fields.String(description='user profile picture')
})

utente_create = api.model('crea_utente', {
    'nome': fields.String(description='user name'),
    'cognome': fields.String(description='user surname'),
    'data_di_nascita': fields.Date(dt_format='rfc822'),
    'nickname': fields.String(description='user nickname'),
    'bio': fields.String(description= 'user bio'),
    'livello_camminatore': fields.Integer(description='level ability')
})

@api.route('/')
class UtenteList(Resource):
    @api.doc('Lista di tutti gli utenti registrati')
    @api.marshal_list_with(utente)
    @api.expect(None, validate = True)
    def get(self):
        """ Ottieni la lista di tutti gli utenti che sono nel database """
        return get_all_utenti(data=request)
    
    @api.doc('Creazione di un nuovo utente')
    @api.expect(utente, validate = True)
    def post(self):
        """ Aggungi al database un nuovo utente """
        return save_new_utente(data=request)

@api.route('/self')
class UtenteSelf(Resource):
    @api.doc('Ottinei dati dell\'utente stesso')
    @api.marshal_with(utente_create)
    @api.expect(None, validate = True)
    def get(self):
        """ Ottine i dati dell'utente stesso """
        return get_utente_self(data=request)
