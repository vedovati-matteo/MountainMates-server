from flask import request
from flask_restx import Namespace, Resource, fields
from ..service.auth_service import token_required
from ..service.user_trip_service import get_user_trips, save_new_registration, delete_registration, update_registration, get_trip_participants

from .trip_api import trip_complete
from .user_api import complete_user

api = Namespace('registration', description='Actions related to trip registrations')

# Define data models for input/output clarity & Swagger UI
trip_id = api.model('Trip ID', {
    'trip_id': fields.String(description='Trip ID')
})

registration_no_id = api.model('Registration without ID', {
    'trip_id': fields.String(description='Trip ID'),
    'status': fields.Integer(description='Registration status'),
    'rating': fields.Integer(description='User\'s rating of the trip')
})

user_trip_complete = api.inherit('Complete User Trip', trip_complete, {
    'firebase_id': fields.String(description='ID of the registered user'),
    'status': fields.Integer(description='Registration status'),
    'rating': fields.Integer(description='User\'s rating of the trip')
})

trip_user_complete = api.inherit('Complete Trip User', complete_user, {
    'trip_id': fields.String(description='Trip ID'),
    'status': fields.Integer(description='Registration status'),
    'rating': fields.Integer(description='User\'s rating of the trip')
})


@api.route('/user/self')
class UserTripList(Resource):
    @api.doc('Get a list of all trips the current user is registered for')
    @api.marshal_list_with(user_trip_complete)
    @api.doc(security='Bearer Auth')
    @token_required
    def get(self, req_id):
        """Get a list of all trips the current user is registered for."""
        return get_user_trips(req_id)

    @api.doc('Register the current user for a trip')
    @api.expect(trip_id, validate=True)
    @api.doc(security='Bearer Auth')
    @token_required
    def post(self, req_id):
        """Register the current user for a trip."""
        return save_new_registration(req_id, request.json)

    @api.doc('Modify the current user\'s registration for a trip')
    @api.expect(registration_no_id, validate=True)
    @api.doc(security='Bearer Auth')
    @token_required
    def put(self, req_id):
        """Modify the current user's registration for a trip."""
        return update_registration(req_id, request.json)

    @api.doc('Cancel the current user\'s registration for a trip')
    @api.expect(trip_id, validate=True)
    @api.doc(security='Bearer Auth')
    @token_required
    def delete(self, req_id):
        """Cancel the current user's registration for a trip."""
        return delete_registration(req_id, request.json)


@api.route('/user/<firebase_id>')
@api.param('firebase_id', 'Firebase User ID')
class UserRegistrations(Resource):
    @api.doc('Get a list of all trips a specific user is registered for')
    @api.marshal_list_with(user_trip_complete)
    @api.doc(security='Bearer Auth')
    @token_required
    def get(self, req_id, firebase_id):
        """Get a list of all trips a specific user is registered for."""
        return get_user_trips(firebase_id)


@api.route('/trip/<trip_id>')
@api.param('trip_id', 'Trip Identifier')
class TripParticipants(Resource):
    @api.doc('Get a list of all users registered for a specific trip')
    @api.marshal_list_with(trip_user_complete)
    @api.doc(security='Bearer Auth')
    @token_required
    def get(self, req_id, trip_id):
        """Get a list of all users registered for a specific trip."""
        return get_trip_participants(trip_id)