# firebase_config.py
import firebase_admin
from firebase_admin import credentials, firestore, auth, initialize_app
import os

USE_FIREBASE_EMULATOR = True  # Set to False in production

def initialize_firebase():
    # Check if Firebase app is already initialized
    if firebase_admin._apps:
        return firebase_admin.get_app(), firestore.client(), auth

    # Construct the path relative to the Django project's root directory
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # Project root
    service_account_key_path = os.path.join(base_dir, '..', 'etc', 'meetero-47be1-firebase-adminsdk-r8os9-6ae307bc69.json')

    #Check if the file exists
    if not os.path.exists(service_account_key_path):
       raise FileNotFoundError(f"Service account key file not found at: {service_account_key_path}")

    # Use a service account
    cred = credentials.Certificate(service_account_key_path)

    # Initialize the app with the credentials
    app = initialize_app(cred)

    if USE_FIREBASE_EMULATOR:
        # Configure Firestore to connect to the emulator
        db = firestore.client()
        db._client._transport.channel._target = 'localhost:8080'  # Replace with the Firestore emulator port if different

        # Configure Authentication to connect to the emulator
        auth._CLIENT = auth.Client(host='http://localhost:9099')  # Replace with the Authentication emulator port if different
        return app, db, auth
    else:
        # Use the default credentials (for production)
        db = firestore.client()
        auth_client = auth
        return app, db, auth_client
