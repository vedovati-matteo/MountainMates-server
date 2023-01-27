from .. import db
from app.model.amici import Amici
from app.model.utente_escursione import Utente_Escursione
from app.model.organizza import Organizza

class Utente(db.Model):
    __tablename__ = "Utente"
    id_firebase = db.Column(db.String(50), primary_key=True)
    nome = db.Column(db.String(50))
    cognome = db.Column(db.String(50))
    nickname = db.Column(db.String(50))
    flag_organizzatore =db.Column(db.Boolean) 
    bio = db.Column(db.String(500))
    data_di_nascita = db.Column(db.Date)
    livello_camminatore = db.Column(db.Integer)
    img = db.Column(db.String(500)) 
    friends = db.relationship("Amici", foreign_keys=[Amici.id_firebase], back_populates="user", cascade="all, delete-orphan")
    escursioni = db.relationship("Utente_Escursione", foreign_keys=[Utente_Escursione.id_firebase], back_populates="user", cascade="all, delete-orphan")
    escursioni_organizzate = db.relationship("Organizza", foreign_keys=[Organizza.id_organizzatore], back_populates="organizzatore", cascade="all, delete-orphan")