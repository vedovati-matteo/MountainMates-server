from flask import request
from flask_restx import Namespace, Resource, fields
from ..service.auth_service import token_required, organizer_required
from ..service.organize_service import get_trips_organized_by_user, assign_trip_to_organizer, remove_trip_from_organizer, get_organizers_for_trip

from .trip_api import trip_complete
from .user_api import complete_user

api = Namespace('organize', description='Actions related to trip organizers')

trip_id = api.model('Trip ID', {
    'trip_id': fields.String(description='Trip ID')
})


@api.route('/user/<organizer_id>')
@api.param('organizer_id', 'Firebase User ID of the organizer')
class OrganizerTrips(Resource):
    @api.doc('Get a list of all trips organized by the specified organizer')
    @api.marshal_list_with(trip_complete)
    @api.doc(security='Bearer Auth')
    @token_required
    def get(self, req_id, organizer_id):
        """Get a list of all trips organized by the specified organizer."""
        return get_trips_organized_by_user(organizer_id)

    @api.doc('Assign a trip to an organizer')
    @api.expect(trip_id, validate=True)
    @api.doc(security='Bearer Auth')
    @token_required
    @organizer_required
    def post(self, req_id, organizer_id):
        """Assign a trip to an organizer."""
        return assign_trip_to_organizer(organizer_id, request.json)

    @api.doc('Remove a trip from an organizer')
    @api.expect(trip_id, validate=True)
    @api.doc(security='Bearer Auth')
    @token_required
    @organizer_required
    def delete(self, req_id, organizer_id):
        """Remove a trip from an organizer."""
        return remove_trip_from_organizer(organizer_id, request.json)


@api.route('/trip/<trip_id>')
@api.param('trip_id', 'Trip Identifier')
class TripOrganizers(Resource):
    @api.doc('Get a list of all organizers for a trip')
    @api.marshal_list_with(complete_user)
    @api.doc(security='Bearer Auth')
    @token_required
    def get(self, req_id, trip_id):
        """Get a list of all organizers for a trip."""
        return get_organizers_for_trip(trip_id)