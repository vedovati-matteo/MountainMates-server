import sys
import firebase_admin
from firebase_admin import credentials, auth
from os import environ
import requests
import json

# Load environment variables from .env file
from dotenv import load_dotenv
load_dotenv()

def get_id_token(custom_token):
    # Firebase Auth REST API endpoint for verifying custom token
    url = f"https://www.googleapis.com/identitytoolkit/v3/relyingparty/verifyCustomToken?key={FIREBASE_WEB_API_KEY}"
    
    data = {
        "token": custom_token,
        "returnSecureToken": True
    }
    
    response = requests.post(url, json=data)
    if response.status_code == 200:
        return response.json()['idToken']
    else:
        raise Exception(f"Failed to get ID token: {response.text}")

def process_arguments(*args):
    num_args = len(args)

    if num_args == 0:
        print("No arguments provided.")
    elif num_args == 1 or num_args == 2:
        # Initialize Firebase Admin SDK
        cred = credentials.Certificate('WebServer/' + environ.get('FIREBASE_CREDENTIALS_PATH'))
        firebase_admin.initialize_app(cred)

        # Get Firebase Web API Key from environment variable
        global FIREBASE_WEB_API_KEY
        FIREBASE_WEB_API_KEY = environ.get('FIREBASE_WEB_API_KEY')
        if not FIREBASE_WEB_API_KEY:
            raise ValueError("FIREBASE_WEB_API_KEY environment variable is not set")

        if num_args == 1:
            # Get an ID token for a specific UID
            custom_token = auth.create_custom_token(args[0])
        else:
            # Generate an ID token for an existing user (using email)
            user = auth.get_user_by_email(args[0])
            custom_token = auth.create_custom_token(user.uid)

        # Convert custom token to ID token
        id_token = get_id_token(custom_token.decode('utf-8'))
        print('Bearer ' + id_token)
    else:
        print("Usage: python auth_token_getter.py [uid] or python auth_token_getter.py [email] [password]")
        sys.exit(1)

# Slice sys.argv to exclude the script name
process_arguments(*sys.argv[1:])