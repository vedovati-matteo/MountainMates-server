from flask import request
from flask_restx import Namespace, Resource, fields
from ..service.auth_service import token_required, organizer_required
from ..service.trip_service import get_all_trips, save_new_trip, save_new_trip_no_template, get_trip, update_trip, delete_trip, get_all_trips_from_template

from .trip_template_api import trip_template, trip_template_no_id
from .user_api import complete_user

api = Namespace('trip', description='Actions on Trips')

# Define data models for input/output clarity & Swagger UI
trip_complete = api.inherit('Complete Trip', trip_template, {
    'trip_id': fields.String(description='Trip ID'),
    'meeting_time': fields.String(description='Meeting time'),
    'date': fields.Date(dt_format='rfc822', description='Date of the trip'),
    'max_participants': fields.Integer(description='Maximum number of participants'),
})

trip_no_id = api.model('Trip without ID', {
    'trip_template_id': fields.String(description='Template ID'),
    'meeting_time': fields.String(description='Meeting time'),
    'date': fields.Date(dt_format='rfc822', description='Date of the trip'),
    'max_participants': fields.Integer(description='Maximum number of participants'),
})

trip_complete_no_id = api.inherit('Complete Trip without ID', trip_template_no_id, {
    'meeting_time': fields.String(description='Meeting time'),
    'date': fields.Date(dt_format='rfc822', description='Date of the trip'),
    'max_participants': fields.Integer(description='Maximum number of participants'),
})

trip_id = api.model('Trip ID', {
    'trip_id': fields.String(description='Trip ID')
})


@api.route('/')
class TripList(Resource):
    @api.doc('List all trips')
    @api.marshal_list_with(trip_complete)
    @token_required  # Requires authentication
    def get(self, req_id):
        """Get a list of all trips in the database."""
        return get_all_trips()

    @api.doc('Create a new trip')
    @api.marshal_with(trip_id)
    @api.expect(trip_no_id, validate=True)
    @api.doc(security='Bearer Auth')
    @token_required
    @organizer_required  # Only organizers can create trips
    def post(self, req_id):
        """Add a new trip to the database."""
        return save_new_trip(request.json)


@api.route('/noTemplate')
class TripListNoTemplate(Resource):
    @api.doc('Create a new trip and template')
    @api.marshal_with(trip_id)
    @api.expect(trip_complete_no_id, validate=True)
    @api.doc(security='Bearer Auth')
    @token_required
    @organizer_required
    def post(self, req_id):
        """Add a new trip and a new template (template not specified) to the database."""
        return save_new_trip_no_template(request.json)


@api.route('/<trip_id>')
@api.param('trip_id', 'Trip Identifier')
class Trip(Resource):
    @api.doc('Get a specific trip')
    @api.marshal_with(trip_complete)
    @api.doc(security='Bearer Auth')
    @token_required
    def get(self, req_id, trip_id):
        """Get the specified trip."""
        return get_trip(trip_id)

    @api.doc('Modify the specified trip')
    @api.expect(trip_no_id, validate=True)
    @api.doc(security='Bearer Auth')
    @token_required
    @organizer_required
    def put(self, req_id, trip_id):
        """Modify the specified trip."""
        return update_trip(trip_id, request.json)

    @api.doc('Delete the specified trip')
    @api.doc(security='Bearer Auth')
    @token_required
    @organizer_required
    def delete(self, req_id, trip_id):
        """Delete the specified trip."""
        return delete_trip(trip_id)


@api.route('/fromTemplate/<trip_template_id>')
@api.param('trip_template_id', 'Template Identifier')
class TripListFromTemplate(Resource):
    @api.doc('Get a list of all trips from a specific template')
    @api.marshal_list_with(trip_complete)
    @api.doc(security='Bearer Auth')
    @token_required
    def get(self, req_id, trip_template_id):
        """Get a list of all trips based on a specific template."""
        return get_all_trips_from_template(trip_template_id)