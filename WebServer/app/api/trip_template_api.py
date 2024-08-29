from flask import request
from flask_restx import Namespace, Resource, fields
from ..service.auth_service import token_required, organizer_required
from ..service.trip_template_service import get_all_trip_templates, save_new_trip_template, get_trip_template, delete_trip_template

api = Namespace('trip_template', description='Actions on Trip Templates')

# Data models for better structure and Swagger documentation
trip_template_no_id = api.model('Trip Template without ID', {
    'name': fields.String(description='Trip name'),
    'province': fields.String(description='Province of the trip'),
    'starting_point': fields.String(description='Starting point of the trip'),
    'map_link': fields.String(description='Link to the map'),
    'elevation_gain': fields.Integer(description='Difference in altitude'),
    'distance': fields.Float(description='Distance'),
    'estimated_time': fields.String(description='Estimated time of the trip'),
    'min_altitude': fields.Integer(description='Minimum altitude'),
    'max_altitude': fields.Integer(description='Maximum altitude'),
    'difficulty': fields.Integer(description='Difficulty of the trip'),
    'required_tools': fields.String(description='Required tools'),
    'path_description': fields.String(description='Path description'),
    'image': fields.String(description='Picture of the trip')
})

trip_template = api.inherit('Complete Trip Template', trip_template_no_id, {
    'trip_template_id': fields.String(description='Template ID')
})

trip_template_id = api.model('Trip Template ID', {
    'trip_template_id': fields.String(description='Template ID')
})


@api.route('/')
class TripTemplateList(Resource):
    @api.doc('List all trip templates')
    @api.marshal_list_with(trip_template)
    @api.doc(security='Bearer Auth')
    @token_required
    def get(self, req_id):
        """Get a list of all trip templates in the database."""
        return get_all_trip_templates()

    @api.doc('Create a new trip template')
    @api.marshal_with(trip_template_id)
    @api.expect(trip_template_no_id, validate=True)
    @api.doc(security='Bearer Auth')
    @token_required
    @organizer_required
    def post(self, req_id):
        """Add a new trip template to the database."""
        return save_new_trip_template(request.json)


@api.route('/<trip_template_id>')
@api.param('trip_template_id', 'Trip Template Identifier')
class TripTemplate(Resource):
    @api.doc('Get a specific trip template')
    @api.marshal_with(trip_template)
    @api.doc(security='Bearer Auth')
    @token_required
    def get(self, req_id, trip_template_id):
        """Get the specified trip template."""
        return get_trip_template(trip_template_id)

    @api.doc('Delete the specified trip template if it has no associated trips')
    @api.doc(security='Bearer Auth')
    @token_required
    @organizer_required
    def delete(self, req_id, trip_template_id):
        """Delete the specified trip template if it has no associated trips."""
        return delete_trip_template(trip_template_id)