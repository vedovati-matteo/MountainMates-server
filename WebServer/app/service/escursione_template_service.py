from .. import db
from app.model.escursione_template import EcursioneTemplate
from datetime import datetime
import uuid

def get_all_escursioni_template(data):
    return EcursioneTemplate.query.all()

def save_new_escursione_template(data):
    escursione_template = escursione_template.query.filter_by(id_escursione_template=id_req).first()
    if not escursione_template:

        new_escursione_template = EcursioneTemplate(
            id_escursione_template = uuid.uuid1(),
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
            img = data['img'],
        )
        save_changes(new_escursione_template)
        response_object = {
            'status': 'successo',
            'message': "template dell'escursione registrato con successo",
        }
        return response_object, 200 
    else:
        response_object = {
            'status': 'fallimento',
            'message': "template dell'escursione già esistente",
        }
        return response_object, 409

def get_escursione_template_self(data):
    pass

def get_escursione_template(data, id):
    return EcursioneTemplate.query.filter_by(id_escursione_template=id).first_or_404()


def save_changes(data):
    db.session.add(data)
    db.session.commit()