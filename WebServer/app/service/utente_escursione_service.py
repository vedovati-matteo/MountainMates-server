from .. import db
from app.model.utente_escursione import Utente_Escursione
from app.model.escursione import Escursione
from app.model.escursione_template import EscursioneTemplate
from app.model.utente import Utente
from flask import abort
from sqlalchemy import and_


def get_escursioni(id):
    joined_data  = db.session.query(Utente_Escursione, Escursione, EscursioneTemplate).select_from(Utente_Escursione).filter(Utente_Escursione.id_firebase==id).join(Escursione).join(EscursioneTemplate).all()
    json_data = []
    for row in joined_data:
            json_data.append({**row[0].__dict__, **row[1].__dict__, **row[2].__dict__})
    return json_data

def save_new_iscrizione(id, data):
    escursione = Escursione.query.filter_by(id_escursione=data['id_escursione'])
    if not escursione:
        return abort(404, 'Escursione non esistente')
    iscrizione = Utente_Escursione.query.filter_by(id_firebase=id, id_escursione=data['id_escursione']).first()
    if not iscrizione: # TODO check escursione non sia ancora avvenuta
        new_iscrizione = Utente_Escursione(
            id_firebase = id,
            id_escursione = data['id_escursione'],
            stato = 1,
            valutazione = -1
        )
        save_changes(new_iscrizione)
        response_object = {
            'status': 'successo',
            'message': 'Iscrizione effettuata'
        }
        return response_object, 200
    else:
        return abort(409, 'Iscrizione già esistente')

def update_iscrizione(id, data):
    iscrizione = Utente_Escursione.query.filter_by(id_firebase=id, id_escursione=data['id_escursione']).first()
    if iscrizione:
        iscrizione.stato = data['stato']
        iscrizione.valutazione = data['valutazione']
        db.session.commit()
        response_object = {
            'status': 'successo',
            'message': 'iscrizione aggiornata con successo',
        }
        return response_object, 200
    else:
        return abort(404, 'Iscrizione non esistente')

def delete_iscrizione(id, data):
    iscrizione = Utente_Escursione.query.filter_by(id_firebase=id, id_escursione=data['id_escursione']).first()
    if iscrizione: # TODO check stato iscrizione
        db.session.delete(iscrizione);
        db.session.commit()
        response_object = {
            'status': 'successo',
            'message': 'Iscrizione eliminata con successo',
        }
        return response_object, 200 
    else:
        return abort(404, 'Iscirzione non esistente')

def get_utenti(id):
    joined_data  = db.session.query(Utente_Escursione, Utente).filter(Utente_Escursione.id_escursione == id).join(Utente).all()
    json_data = []
    for row in joined_data:
            json_data.append({**row[0].__dict__, **row[1].__dict__})
    return json_data


def save_changes(data):
    db.session.add(data)
    db.session.commit()