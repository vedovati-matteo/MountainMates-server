from .. import db

class Amici(db.Model):
    __tablename__ = "Amici"
    id_firebase = db.Column(db.String(50), db.ForeignKey('Utente.id_firebase', ondelete="CASCADE"), primary_key=True) 
    id_friend = db.Column(db.String(50), db.ForeignKey('Utente.id_firebase', ondelete="CASCADE"), primary_key=True)
    user = db.relationship("Utente", back_populates="friends", foreign_keys=[id_firebase])
    friend = db.relationship("Utente", foreign_keys=[id_friend])