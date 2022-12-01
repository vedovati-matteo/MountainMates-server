from .. import db

class Utente_Escursione(db.Model):
    __tablename__ = "Utente_Escursione"
    id_firebase = db.Column(db.String(50), primary_key=True) 
    id_escursione = db.Column(db.Integer, primary_key=True)
    stato =  db.Column(db.Integer)
    int =  db.Column(db.Integer)