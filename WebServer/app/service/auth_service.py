# Authentication decorator
from functools import wraps
from flask import request, abort

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        if "Authorization" in request.headers:
            token = request.headers["Authorization"].split(" ")[1]
        if not token:
            return {
                "message": "Authentication Token is missing!",
                "data": None,
                "error": "Unauthorized"
            }, 401
        req_id = "ok" # TODO chimaata a firebase
        return f(req_id, *args, **kwargs)
    return decorated