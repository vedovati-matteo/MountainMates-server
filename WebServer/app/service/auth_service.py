# Authentication decorator
from functools import wraps
from flask import request, abort
from firebase_admin import auth
from app.model.utente import Utente

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        if "Authorization" in request.headers:
            req_id = ""
            try :
                token = request.headers["Authorization"].split(' ').pop()
                user_info = check_token(token)
                req_id = user_info['uid']
            except:
                return abort(401, 'Firebase Authentication Declined')
            return f(req_id, *args, **kwargs)
        else:
            return abort(401, 'Authentication Token is missing!')
    return decorated

def check_token(token):
    try:
        # Verify the token using the firebase_admin library
        decoded_token = auth.verify_id_token(token)
        return decoded_token
    except Exception as e:
        # If the token is invalid or has expired, return an error
        return abort(401, str(e))


def organizzatore_required(f):
    @wraps(f)
    def decorated(req_id, *args, **kwargs):
        utente = Utente.query.filter_by(id_firebase=req_id).first()
        if utente:
            organizzatore = utente.flag_organizzatore
            if organizzatore:
                return f(req_id, *args, **kwargs)
            else:
                return abort(403, 'Utente non è organizzatore')
        return abort(404, 'Utente non registrato')
    return decorated