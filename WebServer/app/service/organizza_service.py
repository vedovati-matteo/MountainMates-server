from .. import db
from app.model.organizza import Organizza
from app.model.escursione import Escursione
from app.model.escursione_template import EscursioneTemplate
from app.model.utente import Utente
from flask import abort

def get_escursioni(id):
    joined_data = db.session.query(Organizza, Escursione, EscursioneTemplate).select_from(Organizza).filter(Organizza.id_organizzatore==id).join(Escursione).join(EscursioneTemplate).all()
    json_data = []
    for row in joined_data:
            json_data.append({**row[0].__dict__, **row[1].__dict__, **row[2].__dict__})
    return json_data

def save_new_organizza(id, data):
    escursione = Escursione.query.filter_by(id_escursione=data['id_escursione']).first()
    if not escursione:
        return abort(404, 'Escursione non esistente')
    organizza = Organizza.query.filter_by(id_organizzatore=id, id_escursione=data['id_escursione']).first()
    if not organizza: # TODO check escursione non sia ancora avvenuta
        new_organizza = Organizza(
            id_organizzatore = id,
            id_escursione = data['id_escursione']
        )
        save_changes(new_organizza)
        response_object = {
            'status': 'successo',
            'message': 'Aggiunto organizzatore ad escursione'
        }
        return response_object, 200
    else:
        return abort(409, 'Già organizzatore')
    
def delete_organizza(id, data):
    organizza = Organizza.query.filter_by(id_organizzatore=id, id_escursione=data['id_escursione']).first()
    if organizza: # TODO check altri organizzatori
        db.session.delete(organizza);
        db.session.commit()
        response_object = {
            'status': 'successo',
            'message': 'Tolto organizzatore ad escursione',
        }
        return response_object, 200 
    else:
        return abort(404, 'Escursione non organizzata da tale organizzatore')

def get_organizzatori(id):
    joined_data  = db.session.query(Organizza, Utente).filter(Organizza.id_escursione == id).join(Utente).all()
    json_data = []
    for row in joined_data:
            json_data.append({**row[0].__dict__, **row[1].__dict__})
    return json_data

def save_changes(data):
    db.session.add(data)
    db.session.commit()