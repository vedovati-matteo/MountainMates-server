from .. import db

class Utente_Escursione(db.Model):
    __tablename__ = "Utente_Escursione"
    id_firebase = db.Column(db.String(50), db.ForeignKey('Utente.id_firebase', ondelete="CASCADE"), primary_key=True) 
    id_escursione = db.Column(db.String(50), db.ForeignKey('Escursione.id_escursione', ondelete="CASCADE"), primary_key=True)
    stato =  db.Column(db.Integer)
    valutazione =  db.Column(db.Integer)
    user = db.relationship("Utente", back_populates="escursioni", foreign_keys=[id_firebase])
    escursione = db.relationship("Escursione", back_populates="partecipanti", foreign_keys=[id_escursione])
    