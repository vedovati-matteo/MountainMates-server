from .. import db
from app.model.utente import Utente
from datetime import datetime

def get_all_utenti(data):
    return Utente.query.all()

def save_new_utente(data, id_req):
    utente = Utente.query.filter_by(id_firebase=id_req).first()
    if not utente:
        new_utente = Utente(
            id_firebase=id_req,
            nome = data['nome'],
            cognome = data['cognome'],
            nickname = data['nickname'],
            data_di_nascita = datetime.strptime(data['data_di_nascita'], "%Y-%m-%d").date(),
            bio = data['bio'],
            livello_camminatore = data['livello_camminatore'],
            flag_organizzatore = False
        )
        save_changes(new_utente)
        response_object = {
            'status': 'successo',
            'message': 'Utente registrato con successo',
        }
        return response_object, 200 
    else:
        response_object = {
            'status': 'fallimento',
            'message': 'Utente già esistente',
        }
        return response_object, 409

def get_utente_self(data):
    print("------ Trovato")
    return "Va bene"

def get_utente(data, id):
    return Utente.query.filter_by(id_firebase=id).first_or_404()

def save_changes(data):
    db.session.add(data)
    db.session.commit()