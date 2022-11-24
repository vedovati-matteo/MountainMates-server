from flask_restx import Api

from .user_api import api as api_user

api = Api(
    title = '',
    version = '0.0',
    description=  'A description',
)

api.add_namespace(api_user)