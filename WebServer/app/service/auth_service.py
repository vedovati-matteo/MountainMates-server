from functools import wraps
from flask import request, current_app, abort
from firebase_admin import auth
from app.model.user import User
import jwt
import logging

# Configure Flask's logger
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


def token_required(f):
    """
    Decorator to check for a valid Firebase ID token in the Authorization header.
    """

    @wraps(f)
    def decorated(*args, **kwargs):
        if current_app.config['TESTING']:  # Check if in testing mode
            # In testing mode, allow the request without authentication
            token = request.headers["Authorization"].split(' ').pop()
            user_id = token  # You can set a specific test user ID if needed
            return f(*args, req_id=user_id, **kwargs)
        
        token = None
        if "Authorization" in request.headers:
            try:
                token = request.headers["Authorization"].split(' ').pop()
                user_info = verify_token(token)
                user_id = user_info['uid']  # Extract user ID from the decoded token
                return f(*args, req_id=user_id, **kwargs)  # Pass the user_id to the decorated function
            except Exception as e:  # Catch any exceptions during token verification
                logger.error(f"Error during token verification: {str(e)}")
                return abort(401, 'Firebase Authentication Declined')
        else:
            return abort(401, 'Authentication Token is missing!')

    return decorated


def verify_token(token):
    """
    Verifies a Firebase ID token and returns the decoded token if valid.
    """
    try:
        logger.debug(f"Attempting to verify token: {token[:10]}...")
        decoded_token = auth.verify_id_token(token)
        logger.debug(f"Token successfully verified. User ID: {decoded_token.get('uid')}")
        return decoded_token
    except auth.InvalidIdTokenError:
        logger.error("Invalid ID token")
        abort(401, "Invalid ID token")
    except auth.ExpiredIdTokenError:
        logger.error("Expired ID token")
        abort(401, "Expired ID token")
    except auth.RevokedIdTokenError:
        logger.error("Revoked ID token")
        abort(401, "Revoked ID token")
    except auth.CertificateFetchError:
        logger.error("Error fetching certificates")
        abort(500, "Error fetching certificates")  # Server-side error
    except Exception as e:
        logger.error(f"Unexpected error verifying token: {str(e)}")
        # Attempt to decode token without verification for debugging (insecure, use with caution)
        try:
            decoded = jwt.decode(token, options={"verify_signature": False})
            logger.debug(f"Decoded token content: {decoded}")
        except:
            logger.error("Failed to decode token for debugging")
        abort(401, f"Firebase Authentication Declined: {str(e)}")


def organizer_required(f):
    """
    Decorator to check if the authenticated user is an organizer.
    """

    @wraps(f)
    def decorated(*args, req_id, **kwargs):
        user = User.query.filter_by(firebase_id=req_id).first()
        if user:
            if user.is_organizer:
                return f(*args, req_id, **kwargs)
            else:
                return abort(403, 'User is not an organizer')
        return abort(404, 'User not found')

    return decorated