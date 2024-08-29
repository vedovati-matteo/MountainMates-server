from .. import db

class TripTemplate(db.Model):
    """
    Represents a template for creating hiking trips.
    """
    __tablename__ = "trip_template"
    trip_template_id = db.Column(db.String(50), primary_key=True)
    name = db.Column(db.String(50))
    province = db.Column(db.String(2))
    starting_point = db.Column(db.String(30))
    map_link = db.Column(db.String(2000))
    elevation_gain = db.Column(db.Integer)
    distance = db.Column(db.Float)
    estimated_time = db.Column(db.String(20))
    min_altitude = db.Column(db.Integer)
    max_altitude = db.Column(db.Integer)
    difficulty = db.Column(db.Integer)
    required_tools = db.Column(db.String(500))
    path_description = db.Column(db.String(2000))
    image = db.Column(db.String(500))