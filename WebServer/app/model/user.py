from .. import db

class User(db.Model): # class model of user
    __tablename__ = "User"
    id_firebase = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, unique=True, nullable=False)
    email = db.Column(db.String)