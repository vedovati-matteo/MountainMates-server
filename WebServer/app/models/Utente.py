from .. import db

class Utente(db.Model):
    __tablename__ = "Utente"
    id_firebase = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, unique=True, nullable=False)
    email = db.Column(db.String)