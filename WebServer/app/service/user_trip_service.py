from .. import db
from app.model.user_trip import UserTrip
from app.model.trip import Trip
from app.model.trip_template import TripTemplate
from app.model.user import User
from flask import abort
from sqlalchemy import and_

def get_user_trips(user_id):
    """
    Retrieves all trips a user is registered for, including trip and template details.
    """
    joined_data = db.session.query(UserTrip, Trip, TripTemplate).select_from(UserTrip)\
        .filter(UserTrip.user_id == user_id)\
        .join(Trip)\
        .join(TripTemplate)\
        .all()
    json_data = []
    for row in joined_data:
        json_data.append({**row[0].__dict__, **row[1].__dict__, **row[2].__dict__})
    return json_data

def save_new_registration(user_id, data):
    """
    Registers a user for a trip
    """
    trip = Trip.query.filter_by(trip_id=data['trip_id']).first()
    if not trip:
        abort(404, 'Trip not found')

    # TODO: Check if the trip has already happened

    existing_registration = UserTrip.query.filter_by(user_id=user_id, trip_id=data['trip_id']).first()
    if not existing_registration:
        new_registration = UserTrip(
            user_id=user_id,
            trip_id=data['trip_id'],
            status=1,  # Assuming 1 means 'registered'
            rating=-1  # Assuming -1 means 'not rated yet'
        )
        save_changes(new_registration)
        response_object = {
            'status': 'success',
            'message': 'Registration successful'
        }
        return response_object, 200
    else:
        abort(409, 'User is already registered for this trip')

def update_registration(user_id, data):
    """
    Updates a user's registration for a trip (e.g., change status or rating)
    """
    registration = UserTrip.query.filter_by(user_id=user_id, trip_id=data['trip_id']).first()
    if registration:
        registration.status = data['status']
        registration.rating = data['rating']
        db.session.commit()
        response_object = {
            'status': 'success',
            'message': 'Registration updated successfully'
        }
        return response_object, 200
    else:
        abort(404, 'Registration not found')

def delete_registration(user_id, data):
    """
    Cancels a user's registration for a trip
    """
    registration = UserTrip.query.filter_by(user_id=user_id, trip_id=data['trip_id']).first()
    if registration:
        # TODO: Check the registration status before allowing cancellation

        db.session.delete(registration)
        db.session.commit()
        response_object = {
            'status': 'success',
            'message': 'Registration cancelled successfully'
        }
        return response_object, 200
    else:
        abort(404, 'Registration not found')

def get_trip_participants(trip_id):
    """
    Retrieves all users registered for a specific trip, including user details
    """
    joined_data = db.session.query(UserTrip, User).filter(UserTrip.trip_id == trip_id).join(User).all()
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