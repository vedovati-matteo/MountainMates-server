from .. import db

class EcursioneTemplate(db.Model):
    __tablename__ = "EcursioneTemplate"
    id_escursione = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(50))
    provincia  = db.Column(db.String(2))
    partenza = db.Column(db.String(30))
    mapLink =  db.Column(db.String(2000))
    dislivello = db.Column(db.Integer)
    distanza = db.Column(db.Float)
    tempo_stimato = db.Column(db.String(20)) 
    altezza_min = db.Column(db.Integer) 
    altezza_max = db.Column(db.Integer) 
    difficulty = db.Column(db.Integer) 
    strumenti_richiesti = db.Column(db.String(500)) 
    descrizione_percorso =  db.Column(db.String(2000))
    numero_max =  db.Column(db.Integer) 
    img = db.Column(db.String(500)) 