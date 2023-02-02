from flask import request
from flask_restx import Namespace, Resource, fields
from ..service.auth_service import token_required, organizzatore_required
from ..service.utente_service import get_all_utenti, save_new_utente, get_utente, put_utente, delete_utente, get_amici_utente, add_amico, remove_amico, get_all_organizzatori
from ..service.suggested_service import suggest_friends

api = Namespace('utente', description='Azioni relative all\'utente')

utente = api.model('utente_completo', {
    'id_firebase': fields.String(description='user Identifier'),
    'nome': fields.String(description='user name'),
    'cognome': fields.String(description='user surname'),
    'data_di_nascita': fields.String(description='data nel fromato: 2022-12-15'),
    'nickname': fields.String(description='user nickname'),
    'bio': fields.String(description= 'user bio'),
    'flag_organizzatore': fields.Boolean(description= 'if the user is a mountain guide'),
    'livello_camminatore': fields.Integer(description='level ability'),
    'img': fields.String(description='user profile picture')
})

utente_self = api.model('utente_self', {
    'nome': fields.String(description='user name'),
    'cognome': fields.String(description='user surname'),
    'data_di_nascita': fields.String(description='data nel fromato: 2022-12-15'),
    'nickname': fields.String(description='user nickname'),
    'bio': fields.String(description= 'user bio'),
    'livello_camminatore': fields.Integer(description='level ability'),
    'img': fields.String(description='user profile picture')
})

utente_create = api.model('crea_utente', {
    'nome': fields.String(description='user name'),
    'cognome': fields.String(description='user surname'),
    'data_di_nascita': fields.String(description='data nel fromato: 2022-12-15'),
    'nickname': fields.String(description='user nickname'),
    'bio': fields.String(description= 'user bio'),
    'livello_camminatore': fields.Integer(description='level ability')
})

utente_id = api.model('utente_id', {
    'id_firebase': fields.String(description='user Identifier')
})

@api.route('/')
class UtenteList(Resource):
    @api.doc('Lista di tutti gli utenti registrati')
    @api.marshal_list_with(utente)
    @api.expect(None, validate = True)
    @token_required
    def get(req_id, self):
        """ Ottieni la lista di tutti gli utenti che sono nel database """
        return get_all_utenti()
    
    @api.doc('Creazione di un nuovo utente')
    @api.expect(utente_create, validate = True)
    @token_required
    def post(req_id, self):
        """ Aggungi al database un nuovo utente """
        return save_new_utente(data=request.json, id=req_id)

@api.route('/<id_firebase>')
@api.param('id_firebase', 'Identificatore firebase utente')
class Utente(Resource):
    @api.doc('Ottieni l\'utente specificato')
    @api.marshal_with(utente)
    @api.expect(None, validate = True)
    @token_required
    def get(req_id, self, id_firebase):
        """ Ottieni l'utente specificato """
        return get_utente(id=id_firebase)

@api.route('/self')
class UtenteSelf(Resource):
    @api.doc('Ottieni dati dell\'utente stesso')
    @api.expect(None, validate = True)
    @api.marshal_with(utente)
    @token_required
    def get(req_id, self):
        """ Ottiene i dati dell'utente stesso """
        return get_utente(id=req_id)
    
    @api.doc('Aggiona dati dell\'utente')
    @api.expect(utente_self, validate = True)
    @token_required
    def put(req_id, self):
        """ Aggiona dati dell\'utente """
        return put_utente(data=request.json, id=req_id)
    
    @api.doc('Elimina l\'utente stesso')
    @api.expect(None, validate = True)
    @token_required
    def delete(req_id, self):
        """ Elimina l\'utente stesso """
        return delete_utente(id=req_id)

@api.route('/friends/<id_firebase>')
@api.param('id_firebase', 'Identificatore firebase utente')
class Utente(Resource):
    @api.doc('Ottieni lista amicia dell\'utente specificato')
    @api.marshal_list_with(utente)
    @api.expect(None, validate = True)
    @token_required
    def get(req_id, self, id_firebase):
        """ Ottieni lista amicia dell\'utente specificato """
        return get_amici_utente(id=id_firebase)
    
@api.route('/friendsSelf')
class UtenteFriends(Resource):
    @api.doc('Ottieni lista amicia dell\'utente stesso')
    @api.marshal_list_with(utente)
    @api.expect(None, validate = True)
    @token_required
    def get(req_id, self):
        """ Ottieni lista amicia dell\'utente stesso """
        return get_amici_utente(id=req_id)
    
    @api.doc('Aggungi amico')
    @api.expect(utente_id, validate = True)
    @token_required
    def post(req_id, self):
        """ Aggungi amico """
        return add_amico(data=request.json, id=req_id)
        
    @api.doc('Rimuovi amicizia')
    @api.expect(utente_id, validate = True)
    @token_required
    def delete(req_id, self):
        """ Rimuovi amicizia """
        return remove_amico(data=request.json, id=req_id)
    
@api.route('/organizzatore')
class Organizzatori(Resource):
    @api.doc('Lista di tutti gli organizzatori registrati')
    @api.marshal_list_with(utente)
    @api.expect(None, validate = True)
    @token_required
    def get(req_id, self):
        """ Ottieni la lista di tutti gli organizzatori registrati """
        return get_all_organizzatori()

@api.route('/suggestedFriends')
class SuggestedFriends(Resource):
    @api.doc('Lista degli utenti consigliati')
    @api.marshal_list_with(utente)
    @api.expect(None, validate = True)
    @token_required
    def get(req_id, self):
        """ Lista degli utenti consigliati """
        return suggest_friends(req_id)