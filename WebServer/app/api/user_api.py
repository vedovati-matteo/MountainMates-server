from flask import request
from flask_restx import Namespace, Resource, fields
from ..service.user_service import save_new_user, get_all_users, get_a_user

api = Namespace('user', description='user related operations')
user = api.model('user', {
    'id_firebase': fields.String(description='user Identifier'),
    'username': fields.String(description='user username'),
    'email': fields.String(description='user email')
})

@api.route('/')
class UserList(Resource):
    @api.doc('list_of_registered_users')
    @api.marshal_list_with(user)
    def get(self):
        return get_all_users()

    @api.response(201, 'User successfully created.')
    @api.doc('create a new user')
    @api.expect(user, validate=True)
    def post(self):
        """Creates a new User """
        data = request.get_json()
        return save_new_user(data=data)


@api.route('/<id_firebase>')
@api.param('id_firebase', 'The User identifier')
@api.response(404, 'User not found.')
class User(Resource):
    @api.doc('get a user')
    @api.marshal_with(user)
    def get(self, id_firebase):
        """get a user given its identifier"""
        user = get_a_user(id_firebase)
        if not user:
            api.abort(404)
        else:
            return user