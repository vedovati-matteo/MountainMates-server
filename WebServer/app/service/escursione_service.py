from .. import db
import uuid
from datetime import datetime
from app.model.escursione import Escursione
from app.model.escursione_template import EscursioneTemplate
from flask import abort

def get_all_escursioni():
    joined_data  = db.session.query(Escursione, EscursioneTemplate).join(EscursioneTemplate).all()
    json_data = []
    for row in joined_data:
            json_data.append({**row[0].__dict__, **row[1].__dict__})
    return json_data

def save_new_escursione(data):
    template = EscursioneTemplate.query.filter_by(id_escursione_template = data['id_escursione_template'])
    if template:
        id = str(uuid.uuid4())
        new_escursione = Escursione(
            id_escursione = id,
            orario_ritrovo = data['orario_ritrovo'],
            data = datetime.strptime(data['data'], "%Y-%m-%d").date(),
            numero_max = data['numero_max'],
            id_escursione_template = data['id_escursione_template']
        )
        save_changes(new_escursione)
        response_object = {
            'id_escursione': id
        }
        return response_object, 200
    else:
        return abort(404, 'Template non esiste')

def save_new_escursione_no_template(data):
    # Add template
    id_template = str(uuid.uuid4())
    new_escursione_template = EscursioneTemplate(
        id_escursione_template = id_template,
        nome = data['nome'],
        provincia = data['provincia'],
        partenza = data['partenza'],
        mapLink = data['mapLink'],
        dislivello = data['dislivello'], 
        distanza= data['distanza'],
        tempo_stimato = data['tempo_stimato'],
        altezza_min = data['altezza_min'],
        altezza_max = data['altezza_max'],
        difficulty = data['difficulty'],
        strumenti_richiesti = data['strumenti_richiesti'],
        descrizione_percorso = data['descrizione_percorso'],
        img = data['img']
    )
    save_changes(new_escursione_template)
    # Add escursione
    id_escursione = str(uuid.uuid4())
    new_escursione = Escursione(
        id_escursione = id_escursione,
        orario_ritrovo = data['orario_ritrovo'],
        data = datetime.strptime(data['data'], "%Y-%m-%d").date(),
        numero_max = data['numero_max'],
        id_escursione_template = id_template
    )
    save_changes(new_escursione)
    response_object = {
        'id_escursione': id_escursione
    }
    return response_object, 200

def get_escursione(id):
    row  = db.session.query(Escursione, EscursioneTemplate).join(EscursioneTemplate).filter(Escursione.id_escursione == id).first()
    if not row:
        return abort(404, 'Escursione non esistente')
    json_data = {**row[0].__dict__, **row[1].__dict__}
    return json_data

def put_escursione(id, data):
    escursione = Escursione.query.filter_by(id_escursione=id).first()
    if escursione:
        escursione.id_escursione_template = data['id_escursione_template']
        escursione.orario_ritrovo = data['orario_ritrovo']
        escursione.data = data['data']
        escursione.numero_max = data['numero_max']
        db.session.commit()
        response_object = {
            'status': 'successo',
            'message': 'escursione aggiornata con successo',
        }
        return response_object, 200
    else:
        return abort(404, 'Escursione non esistente')

def delete_escursione(id):
    escursione = Escursione.query.filter_by(id_escursione=id).first()
    if escursione:
        db.session.delete(escursione);
        db.session.commit()
        response_object = {
            'status': 'successo',
            'message': 'Escursione eliminata con successo',
        }
        return response_object, 200 
    else:
        return abort(404, 'Escursione non esistente')

def get_all_escursioni_template(id):
    joined_data  = db.session.query(Escursione, EscursioneTemplate).join(EscursioneTemplate).filter(EscursioneTemplate.id_escursione_template == id).all()
    json_data = []
    for row in joined_data:
            json_data.append({**row[0].__dict__, **row[1].__dict__})
    return json_data

def save_changes(data):
    db.session.add(data)
    db.session.commit()