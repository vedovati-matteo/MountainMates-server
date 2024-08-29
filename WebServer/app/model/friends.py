from .. import db

class Friends(db.Model):
    """
    Represents a friendship relationship between two users.
    """
    __tablename__ = "friends"
    user_id = db.Column(db.String(50), db.ForeignKey('user.firebase_id', ondelete="CASCADE"), primary_key=True)
    friend_id = db.Column(db.String(50), db.ForeignKey('user.firebase_id', ondelete="CASCADE"), primary_key=True)
    user = db.relationship("User", back_populates="friends", foreign_keys=[user_id])
    friend = db.relationship("User", foreign_keys=[friend_id])