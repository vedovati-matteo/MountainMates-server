from .. import db
import uuid
from datetime import datetime
from app.model.trip import Trip
from app.model.trip_template import TripTemplate
from flask import abort


def get_all_trips():
    """
    Retrieves all trips with their associated templates from the database.
    """
    joined_data = db.session.query(Trip, TripTemplate).join(TripTemplate).all()
    json_data = []
    for row in joined_data:
        json_data.append({**row[0].__dict__, **row[1].__dict__})
    return json_data


def save_new_trip(data):
    """
    Creates and saves a new trip to the database based on an existing template.
    """
    template = TripTemplate.query.filter_by(trip_template_id=data['trip_template_id']).first()
    if template:
        trip_id = str(uuid.uuid4())
        new_trip = Trip(
            trip_id=trip_id,
            meeting_time=data['meeting_time'],
            date=datetime.strptime(data['date'], "%Y-%m-%d").date(),
            max_participants=data['max_participants'],
            trip_template_id=data['trip_template_id']
        )
        save_changes(new_trip)
        response_object = {
            'trip_id': trip_id
        }
        return response_object, 200
    else:
        abort(404, 'Template does not exist')


def save_new_trip_no_template(data):
    """
    Creates and saves a new trip and a new template to the database.
    """
    # Create and save the new template
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
    # Create and save the new trip using the newly created template
    trip_id = str(uuid.uuid4())
    new_trip = Trip(
        trip_id=trip_id,
        meeting_time=data['meeting_time'],
        date=datetime.strptime(data['date'], "%Y-%m-%d").date(),
        max_participants=data['max_participants'],
        trip_template_id=template_id
    )
    save_changes(new_trip)

    response_object = {
        'trip_id': trip_id
    }
    return response_object, 200


def get_trip(trip_id):
    """
    Retrieves a specific trip with its associated template from the database.
    """
    row = db.session.query(Trip, TripTemplate).join(TripTemplate).filter(Trip.trip_id == trip_id).first()
    if not row:
        abort(404, 'Trip not found')
    json_data = {**row[0].__dict__, **row[1].__dict__}
    return json_data


def update_trip(trip_id, data):
    """
    Updates an existing trip in the database.
    """
    trip = Trip.query.filter_by(trip_id=trip_id).first()
    
    if trip:
        keys_to_update = ['trip_template_id', 'meeting_time', 'date', 'max_participants']

        for key in keys_to_update:
            if key in data:
                setattr(trip, key, data[key])


        db.session.commit()
        response_object = {
            'status': 'success',
            'message': 'Trip updated successfully'
        }
        return response_object, 200
    else:
        abort(404, 'Trip not found')


def delete_trip(trip_id):
    """
    Deletes a trip from the database.
    """
    trip = Trip.query.filter_by(trip_id=trip_id).first()
    if trip:
        db.session.delete(trip)
        db.session.commit()
        response_object = {
            'status': 'success',
            'message': 'Trip deleted successfully'
        }
        return response_object, 200
    else:
        abort(404, 'Trip not found')


def get_all_trips_from_template(template_id):
    """
    Retrieves all trips associated with a specific template.
    """
    joined_data = db.session.query(Trip, TripTemplate).join(TripTemplate).filter(
        TripTemplate.trip_template_id == template_id).all()
    json_data = []
    for row in joined_data:
        json_data.append({**row[0].__dict__, **row[1].__dict__})
    return json_data


def save_changes(data):
    """
    Helper function to save changes to the database.
    """
    db.session.add(data)
    db.session.commit()