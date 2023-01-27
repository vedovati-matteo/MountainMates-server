
from .. import db

class Organizza(db.Model):
    __tablename__ = "Organizza"
    id_organizzatore = db.Column(db.String(50), db.ForeignKey('Utente.id_firebase'), primary_key=True) 
    id_escursione = db.Column(db.String(50), db.ForeignKey('Escursione.id_escursione'), primary_key=True)
    organizzatore = db.relationship("Utente", back_populates="escursioni_organizzate", foreign_keys=[id_organizzatore])
    escursione = db.relationship("Escursione", back_populates="organizzatori", foreign_keys=[id_escursione])
    