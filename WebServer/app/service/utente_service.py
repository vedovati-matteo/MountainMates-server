from .. import db
from app.model.utente import Utente

def get_all_utenti(data):
    pass

def save_new_utente(data):
    response_object = {
        'status': 'prova',
        'message': 'Questa è una prova',
    }
    return response_object, 200

def get_utente_self(data):
    print("------ Trovato")
    return "Va bene"