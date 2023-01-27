from .. import db
from app.model.utente import Utente
from app.model.amici import Amici
from datetime import datetime
from flask import abort

def get_all_utenti():
    return Utente.query.all()

def save_new_utente(data, id):
    utente = Utente.query.filter_by(id_firebase=id).first()
    if not utente:
        new_utente = Utente(
            id_firebase=id,
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
        return abort(409, 'Utente già esistente')

def get_utente(id):
    return Utente.query.filter_by(id_firebase=id).first_or_404()

def put_utente(data, id):
    utente = Utente.query.filter_by(id_firebase=id).first()
    if utente:
        utente.nome = data['nome']
        utente.cognome = data['cognome']
        utente.nickname = data['nickname']
        utente.data_di_nascita = datetime.strptime(data['data_di_nascita'], "%Y-%m-%d").date()
        utente.bio = data['bio']
        utente.livello_camminatore = data['livello_camminatore']
        utente.img = data['img']
        db.session.commit()
        response_object = {
            'status': 'successo',
            'message': 'Utente aggiornato con successo',
        }
        return response_object, 200 
    else:
        return abort(404, 'Utente non esistente')

def delete_utente(id):
    utente = Utente.query.filter_by(id_firebase=id).first()
    if utente:
        db.session.delete(utente);
        db.session.commit()
        response_object = {
            'status': 'successo',
            'message': 'Utente eliminato con successo',
        }
        return response_object, 200 
    else:
        return abort(404, 'Utente non esistente')

def get_amici_utente(id):
    utente = Utente.query.filter_by(id_firebase=id).first()
    if utente:
        amici = Utente.query.filter(Utente.id_firebase.in_(db.session.query(Amici.id_friend).filter_by(id_firebase=id))).all()
        return amici
    else:
        return abort(404, 'Utente non esistente')

def add_amico(data, id):
    utente = Utente.query.filter_by(id_firebase=id).first()
    if utente:
        if id == data['id_firebase']:
            return abort(409, 'Impossibile essere amici di se stessi')
        amcizia_esistente = Amici.query.filter_by(id_firebase=id, id_friend=data['id_firebase']).first()
        if amcizia_esistente:
            response_object = {
                'status': 'successo',
                'message': 'Amiciazia già esistente',
            }
            return response_object, 200
        else:
            amiciazia = Amici(id_firebase=id, id_friend=data['id_firebase'])
            save_changes(amiciazia)
            response_object = {
                'status': 'successo',
                'message': 'Amicizia effettuata',
            }
            return response_object, 200
    else:
        return abort(404, 'Utente non esistente')

def remove_amico(data, id):
    utente = Utente.query.filter_by(id_firebase=id).first()
    if utente:
        amcizia = Amici.query.filter_by(id_firebase=id, id_friend=data['id_firebase']).first()
        if amcizia:
            db.session.delete(amcizia)
            db.session.commit()
            response_object = {
                'status': 'successo',
                'message': 'Amiciazia rimossa',
            }
            return response_object, 200
        else:
            response_object = {
                'status': 'successo',
                'message': 'Amicizia non esistente',
            }
            return response_object, 200
    else:
        return abort(404, 'Utente non esistente')  

def get_all_organizzatori():
    return Utente.query.filter_by(flag_organizzatore=True).all()

def save_changes(data):
    db.session.add(data)
    db.session.commit()