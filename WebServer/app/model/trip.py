from .. import db
from app.model.user_trip import UserTrip
from app.model.organize import Organize

class Trip(db.Model):
    """
    Represents a hiking trip.
    """
    __tablename__ = "trip"
    trip_id = db.Column(db.String(50), primary_key=True)
    meeting_time = db.Column(db.String(20))
    date = db.Column(db.DateTime())
    max_participants = db.Column(db.Integer)
    trip_template_id = db.Column(db.String(50), db.ForeignKey('trip_template.trip_template_id'))
    participants = db.relationship("UserTrip", foreign_keys=[UserTrip.trip_id], back_populates="trip", cascade="all, delete-orphan")
    organizers = db.relationship("Organize", foreign_keys=[Organize.trip_id], back_populates="trip", cascade="all, delete-orphan")