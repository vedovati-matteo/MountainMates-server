from .. import db

class Utente_Escursione(db.Model):
    __tablename__ = "Utente_Escursione"
    id_firebase = db.Column(db.String(50), db.ForeignKey('Utente.id_firebase'), primary_key=True) 
    id_escursione = db.Column(db.Integer, db.ForeignKey('Escursione.id_escursione'), primary_key=True)
    stato =  db.Column(db.Integer)
    valutazione =  db.Column(db.Integer)