from flask import request
from flask_restx import Namespace, Resource, fields
from ..service.auth_service import token_required, organizer_required
from ..service.user_service import get_all_users, save_new_user, get_user, update_user, delete_user, get_user_friends, add_friend, remove_friend, get_all_organizers
from ..service.suggested_service import suggest_friends

api = Namespace('user', description='Actions related to users')

# Define data models for input/output and Swagger UI
complete_user = api.model('Complete User', {
    'firebase_id': fields.String(description='User Identifier'),
    'first_name': fields.String(description='User\'s first name'),
    'last_name': fields.String(description='User\'s last name'),
    'date_of_birth': fields.String(description='Date of birth in the format: YYYY-MM-DD'),
    'nickname': fields.String(description='User\'s nickname'),
    'bio': fields.String(description='User\'s bio'),
    'is_organizer': fields.Boolean(description='Indicates if the user is an organizer/mountain guide'),
    'hiker_level': fields.Integer(description='User\'s hiking ability level'),
    'profile_picture': fields.String(description='User\'s profile picture URL')
})

user_self = api.model('User Self', {
    'first_name': fields.String(description='User\'s first name'),
    'last_name': fields.String(description='User\'s last name'),
    'date_of_birth': fields.String(description='Date of birth in the format: YYYY-MM-DD'),
    'nickname': fields.String(description='User\'s nickname'),
    'bio': fields.String(description='User\'s bio'),
    'hiker_level': fields.Integer(description='User\'s hiking ability level'),
    'profile_picture': fields.String(description='User\'s profile picture URL')
})

create_user = api.model('Create User', {
    'first_name': fields.String(description='User\'s first name'),
    'last_name': fields.String(description='User\'s last name'),
    'date_of_birth': fields.String(description='Date of birth in the format: YYYY-MM-DD'),
    'nickname': fields.String(description='User\'s nickname'),
    'bio': fields.String(description='User\'s bio'),
    'hiker_level': fields.Integer(description='User\'s hiking ability level')
})

user_id = api.model('User ID', {
    'firebase_id': fields.String(description='User Identifier')
})


@api.route('/')
class UserList(Resource):
    @api.doc('List all registered users')
    @api.marshal_list_with(complete_user)
    @api.doc(security='Bearer Auth')
    @token_required
    def get(self, req_id):
        """Get a list of all users in the database."""
        return get_all_users()

    @api.doc('Create a new user')
    @api.expect(create_user, validate=True)
    @api.doc(security='Bearer Auth')
    @token_required
    def post(self, req_id):
        """Add a new user to the database."""
        return save_new_user(request.json, req_id)


@api.route('/<firebase_id>')
@api.param('firebase_id', 'Firebase User ID')
class User(Resource):
    @api.doc('Get a specific user')
    @api.marshal_with(complete_user)
    @api.doc(security='Bearer Auth')
    @token_required
    def get(self, req_id, firebase_id):
        """Get the specified user."""
        return get_user(firebase_id)


@api.route('/self')
class UserSelf(Resource):
    @api.doc('Get the current user\'s data')
    @api.marshal_with(complete_user)
    @api.doc(security='Bearer Auth')
    @token_required
    def get(self, req_id):
        """Get the current user's data."""
        return get_user(req_id)

    @api.doc('Update the current user\'s data')
    @api.expect(user_self, validate=True)
    @api.doc(security='Bearer Auth')
    @token_required
    def put(self, req_id):
        """Update the current user's data."""
        return update_user(request.json, req_id)

    @api.doc('Delete the current user')
    @api.doc(security='Bearer Auth')
    @token_required
    def delete(self, req_id):
        """Delete the current user."""
        return delete_user(req_id)


@api.route('/friends/<firebase_id>')
@api.param('firebase_id', 'Firebase User ID')
class UserFriends(Resource):
    @api.doc('Get a list of friends for the specified user')
    @api.marshal_list_with(complete_user)
    @api.doc(security='Bearer Auth')
    @token_required
    def get(self, req_id, firebase_id):
        """Get a list of friends for the specified user."""
        return get_user_friends(firebase_id)


@api.route('/friends/self')
class UserSelfFriends(Resource):
    @api.doc('Get a list of the current user\'s friends')
    @api.marshal_list_with(complete_user)
    @api.doc(security='Bearer Auth')
    @token_required
    def get(self, req_id):
        """Get a list of the current user's friends."""
        return get_user_friends(req_id)

    @api.doc('Add a friend for the current user')
    @api.expect(user_id, validate=True)
    @api.doc(security='Bearer Auth')
    @token_required
    def post(self, req_id):
        """Add a friend for the current user."""
        return add_friend(request.json, req_id)

    @api.doc('Remove a friend for the current user')
    @api.expect(user_id, validate=True)
    @api.doc(security='Bearer Auth')
    @token_required
    def delete(self, req_id):
        """Remove a friend for the current user."""
        return remove_friend(request.json, req_id)


@api.route('/organizer')
class Organizers(Resource):
    @api.doc('List all registered organizers')
    @api.marshal_list_with(complete_user)
    @api.doc(security='Bearer Auth')
    @token_required
    def get(self, req_id):
        """Get a list of all registered organizers."""
        return get_all_organizers()


@api.route('/suggestedFriends')
class SuggestedFriends(Resource):
    @api.doc('Get a list of suggested friends for the current user')
    @api.marshal_list_with(complete_user)
    @api.doc(security='Bearer Auth')
    @token_required
    def get(self, req_id):
        """Get a list of suggested friends for the current user."""
        return suggest_friends(req_id)