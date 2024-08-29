from .. import db

class Organize(db.Model):
    """
    Represents the relationship between an organizer and a trip they organize
    """
    __tablename__ = "organize"
    organizer_id = db.Column(db.String(50), db.ForeignKey('user.firebase_id'), primary_key=True)
    trip_id = db.Column(db.String(50), db.ForeignKey('trip.trip_id'), primary_key=True)
    organizer = db.relationship("User", back_populates="organized_trips", foreign_keys=[organizer_id])
    trip = db.relationship("Trip", back_populates="organizers", foreign_keys=[trip_id])