import json

import firebase_admin
import requests
from firebase_admin import credentials

FIREBASE_WEB_API_KEY = 'AIzaSyDduUjffM8IBT5WT5J9z6ZLYhM9XFnz8BA'
KEY_PATH = r"C:\Users\andre\OneDrive\Documents\GitHub\GraphEditor\FirebaseKey\graph-editor-5e2d6-firebase-adminsdk-fbsvc-5d8d4e89a1.json"

def initialize_firebase():
    if not firebase_admin._apps:  # Check if Firebase is already initialized
        try:
            cred = credentials.Certificate(KEY_PATH)
            firebase_admin.initialize_app(cred)
            print("Firebase Admin SDK initialized successfully.")
        except FileNotFoundError:
            print(f"Error: Service account key file not found at {KEY_PATH}. Please ensure the file exists.")
            # Optionally, disable login button or show error on UI
            #self.ui.pushButton_login.setEnabled(False)
            #self.ui.label_error.setText(f"Firebase Error: Key file not found.\nPlease check console.")
        except Exception as e:
            print(f"An error occurred during Firebase initialization: {e}")
            # Optionally, disable login button or show error on UI
            #self.ui.pushButton_login.setEnabled(False)
            #self.ui.label_error.setText(f"Firebase Error: {e}\nPlease check console.")


class UserModel:
    def __init__(self):
        initialize_firebase()

    def login(self, email, password):
        rest_api_url = f"https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword?key={FIREBASE_WEB_API_KEY}"
        payload = {
            'email': email,
            'password': password,
            'returnSecureToken': True
        }

        try:
            response = requests.post(rest_api_url, data=json.dumps(payload),
                                     headers={'Content-Type': 'application/json'})
            response_data = response.json()

            if response.status_code == 200:
                uid = response_data.get('localId')
                return True, uid
            else:
                error_info = response_data.get('error', {})
                message = error_info.get('message', 'Unknown authentication error.')
                return False, message

        except requests.exceptions.RequestException as e:
            return False, str(e)

        except json.JSONDecodeError:
            error = "Error decoding JSON response from Firebase."
            return False, str(error)

        except Exception as e:
            return False, str(e)

    def register(self, email, password):
        rest_api_url = f"https://identitytoolkit.googleapis.com/v1/accounts:signUp?key={FIREBASE_WEB_API_KEY}"
        payload = {
            'email': email,
            'password': password,
            'returnSecureToken': True
        }

        try:
            response = requests.post(rest_api_url, data=json.dumps(payload),
                                     headers={'Content-Type': 'application/json'})
            response_data = response.json()

            if response.status_code == 200:
                uid = response_data.get('localId')
                return True, uid
            else:
                error_info = response_data.get('error', {})
                message = error_info.get('message', 'Unknown authentication error.')
                return False, message

        except requests.exceptions.RequestException as e:
            return False, str(e)

        except Exception as e:
            return False, str(e)

