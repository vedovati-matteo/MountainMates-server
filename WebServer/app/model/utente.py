from .. import db

class Utente(db.Model):
    __tablename__ = "Utente"
    id_firebase = db.Column(db.String(50), primary_key=True)
    nome = db.Column(db.String(50))
    cognome = db.Column(db.String(50))
    nickname = db.Column(db.String(50))
    flag_organizzatore =db.Column(db.Boolean) 
    bio = db.Column(db.String(500))
    data_di_nascita = db.Column(db.Date)
    numero_amici =  db.Column(db.Integer)
    livello_camminatore = db.Column(db.Integer)
    img = db.Column(db.String(500)) 