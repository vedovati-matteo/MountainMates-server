from .. import db
from app.model.utente_escursione import Utente_Escursione
from app.model.organizza import Organizza

class Escursione(db.Model):
    __tablename__ = "Escursione"
    id_escursione = db.Column(db.String(50), primary_key=True)
    orario_ritrovo = db.Column(db.String(20))
    data = db.Column(db.DateTime())
    numero_max =  db.Column(db.Integer)
    id_escursione_template = db.Column(db.String(50), db.ForeignKey('EscursioneTemplate.id_escursione_template'))
    partecipanti = db.relationship("Utente_Escursione", foreign_keys=[Utente_Escursione.id_escursione], back_populates="escursione", cascade="all, delete-orphan")
    organizzatori = db.relationship("Organizza", foreign_keys=[Organizza.id_escursione], back_populates="escursione", cascade="all, delete-orphan")