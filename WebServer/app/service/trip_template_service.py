from .. import db
from app.model.trip_template import TripTemplate
from datetime import datetime
import uuid
from flask import abort

def get_all_trip_templates():
    """
    Retrieves all trip templates from the database
    """
    return TripTemplate.query.all()

def save_new_trip_template(data):
    """
    Creates and saves a new trip template to the database
    """
    template_id = str(uuid.uuid4())
    new_trip_template = TripTemplate(
        trip_template_id=template_id,
        name=data['name'],
        province=data['province'],
        starting_point=data['starting_point'],
        map_link=data['map_link'],
        elevation_gain=data['elevation_gain'],
        distance=data['distance'],
        estimated_time=data['estimated_time'],
        min_altitude=data['min_altitude'],
        max_altitude=data['max_altitude'],
        difficulty=data['difficulty'],
        required_tools=data['required_tools'],
        path_description=data['path_description'],
        image=data['image']
    )
    save_changes(new_trip_template)
    response_object = {
        'trip_template_id': template_id
    }
    return response_object, 200 

def get_trip_template(template_id):
    """
    Retrieves a specific trip template from the database
    """
    return TripTemplate.query.filter_by(trip_template_id=template_id).first_or_404()

def delete_trip_template(template_id):
    """
    Deletes a trip template from the database if it has no associated trips
    """
    trip_template = TripTemplate.query.filter_by(trip_template_id=template_id).first()
    if trip_template:
        db.session.delete(trip_template)
        db.session.commit()
        response_object = {
            'status': 'success',
            'message': 'Trip template deleted successfully'
        }
        return response_object, 200
    else:
        abort(404, 'Trip template not found')

def save_changes(data):
    """
    Helper function to save changes to the database
    """
    db.session.add(data)
    db.session.commit()