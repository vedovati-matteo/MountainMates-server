from .. import db
from app.model.friends import Friends
from app.model.user_trip import UserTrip
from app.model.organize import Organize

class User(db.Model):
    """
    Represents a user in the application
    """
    __tablename__ = "user"
    firebase_id = db.Column(db.String(50), primary_key=True)
    first_name = db.Column(db.String(50))
    last_name = db.Column(db.String(50))
    nickname = db.Column(db.String(50))
    is_organizer = db.Column(db.Boolean)
    bio = db.Column(db.String(500))
    date_of_birth = db.Column(db.Date)
    hiker_level = db.Column(db.Integer)
    profile_picture = db.Column(db.String(500))
    friends = db.relationship("Friends", foreign_keys=[Friends.user_id], back_populates="user", cascade="all, delete-orphan")
    trips = db.relationship("UserTrip", foreign_keys=[UserTrip.user_id], back_populates="user", cascade="all, delete-orphan")
    organized_trips = db.relationship("Organize", foreign_keys=[Organize.organizer_id], back_populates="organizer", cascade="all, delete-orphan")