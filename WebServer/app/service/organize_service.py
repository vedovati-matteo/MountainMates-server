from .. import db
from app.model.organize import Organize
from app.model.trip import Trip
from app.model.trip_template import TripTemplate
from app.model.user import User
from flask import abort

def get_trips_organized_by_user(user_id):
    """
    Retrieves all trips organized by a specific user, including trip and template details.
    """
    joined_data = db.session.query(Organize, Trip, TripTemplate).select_from(Organize)\
        .filter(Organize.organizer_id == user_id)\
        .join(Trip)\
        .join(TripTemplate)\
        .all()
    json_data = []
    for row in joined_data:
        json_data.append({**row[0].__dict__, **row[1].__dict__, **row[2].__dict__})
    return json_data

def assign_trip_to_organizer(organizer_id, data):
    """
    Assigns an existing trip to an organizer.
    """
    trip = Trip.query.filter_by(trip_id=data['trip_id']).first()
    if not trip:
        abort(404, 'Trip not found')

    # TODO: Check if the trip has already taken place

    existing_organizer = Organize.query.filter_by(organizer_id=organizer_id, trip_id=data['trip_id']).first()
    if not existing_organizer:
        new_organizer = Organize(
            organizer_id=organizer_id,
            trip_id=data['trip_id']
        )
        save_changes(new_organizer)
        response_object = {
            'status': 'success',
            'message': 'Organizer added to the trip'
        }
        return response_object, 200
    else:
        abort(409, 'User is already an organizer for this trip')

def remove_trip_from_organizer(organizer_id, data):
    """
    Removes a trip from an organizer's list of organized trips
    """
    organizer_trip = Organize.query.filter_by(organizer_id=organizer_id, trip_id=data['trip_id']).first()
    if organizer_trip:
        # TODO: Check if there are other organizers for the trip

        db.session.delete(organizer_trip)
        db.session.commit()
        response_object = {
            'status': 'success',
            'message': 'Organizer removed from the trip'
        }
        return response_object, 200
    else:
        abort(404, 'Trip not organized by this organizer')

def get_organizers_for_trip(trip_id):
    """
    Retrieves all organizers for a specific trip, including user details
    """
    joined_data = db.session.query(Organize, User).filter(Organize.trip_id == trip_id).join(User).all()
    json_data = []
    for row in joined_data:
        json_data.append({**row[0].__dict__, **row[1].__dict__})
    return json_data

def save_changes(data):
    """
    Helper function to save changes to the database
    """
    db.session.add(data)
    db.session.commit()