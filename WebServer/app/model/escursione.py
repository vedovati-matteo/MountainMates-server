from .. import db

class Ecursione(db.Model):
    __tablename__ = "Escursione"
    id_escursione = db.Column(db.Integer, primary_key=True)
    orario_ritrovo = db.Column(db.String(20))
    data = db.Column(db.DateTime())
    numero_max =  db.Column(db.Integer)
    id_escursione_template = db.Column(db.Integer, db.ForeignKey('EcursioneTemplate.id_escursione_template'))
     