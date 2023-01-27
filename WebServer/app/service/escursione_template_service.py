from .. import db
from app.model.escursione_template import EscursioneTemplate
from datetime import datetime
import uuid
from flask import abort

def get_all_escursioni_template():
    return EscursioneTemplate.query.all()

def save_new_escursione_template(data):
    id = str(uuid.uuid4())
    new_escursione_template = EscursioneTemplate(
        id_escursione_template = id,
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
    response_object = {
        'id_escursione_template': id
    }
    return response_object, 200 
   
def get_escursione_template(id):
    return EscursioneTemplate.query.filter_by(id_escursione_template=id).first_or_404()

def delete_escursione_template(id):
    escursione_template = EscursioneTemplate.query.filter_by(id_escursione_template=id).first()
    if escursione_template:
        db.session.delete(escursione_template)
        db.session.commit()
        response_object = {
            'status': 'successo',
            'message': 'Template escursione eliminato con successo',
        }
        return response_object, 200
    else:
        return abort(404, 'Template escursione non esistente')

def save_changes(data):
    db.session.add(data)
    db.session.commit()