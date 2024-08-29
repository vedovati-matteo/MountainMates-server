from .. import db

class UserTrip(db.Model):
    """
    Represents a user's registration for a trip.
    """
    __tablename__ = "user_trip"
    user_id = db.Column(db.String(50), db.ForeignKey('user.firebase_id', ondelete="CASCADE"), primary_key=True)
    trip_id = db.Column(db.String(50), db.ForeignKey('trip.trip_id', ondelete="CASCADE"), primary_key=True)
    status = db.Column(db.Integer)
    rating = db.Column(db.Integer)
    user = db.relationship("User", back_populates="trips", foreign_keys=[user_id])
    trip = db.relationship("Trip", back_populates="participants", foreign_keys=[trip_id])