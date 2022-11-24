import uuid

from .. import db
from app.model.user import User

# logic of class Utente

def save_new_user(data):
    new_user = User(
        id_firebase = str(uuid.uuid4()),
        username = data['username'],
        email = data['email']
    )
    save_changes(new_user)
    response_object = {
        'status': 'success',
        'message': 'Successfully registered.'
    }
    return response_object, 201

def get_all_users():
    return User.query.all()

def get_a_user(id_firebase):
    return User.query.filter_by(id_firebase=id_firebase).first()
    
def save_changes(data):
    db.session.add(data)
    db.session.commit()