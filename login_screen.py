import sys
import requests  # For making HTTP requests
import json  # For parsing JSON responses
from PyQt5.QtWidgets import QMainWindow, QApplication
from ui_login_screen import Ui_LoginScreen
# from main import MainWindow # Circular import will be resolved by local import

import firebase_admin
from firebase_admin import credentials, auth

KEY_PATH = r"/FirebaseKey/graph-editor-5e2d6-firebase-adminsdk-fbsvc-5d8d4e89a1.json"
# IMPORTANT: Replace "YOUR_FIREBASE_WEB_API_KEY" with your actual Firebase Web API Key.
# You can find this in your Firebase project settings: Project settings > General > Your apps > Web API Key.
FIREBASE_WEB_API_KEY = "AIzaSyDduUjffM8IBT5WT5J9z6ZLYhM9XFnz8BA"


class LoginScreen(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initialize_firebase()  # Call Firebase initialization
        self.ui = Ui_LoginScreen()
        self.ui.setupUi(self)

        # Instantiate MainWindow but don't show it yet
        # from main import MainWindow  # Local import to avoid circular dependency
        # self.main_win = MainWindow()

        # Connect the login button's clicked signal
        #self.ui.pushButton_login.clicked.connect(self.handle_login)

        # For now, a standard window appearance is used.
        # If a frameless or translucent window is desired later,
        # the following lines can be uncommented and Qt.FramelessWindowHint
        # and Qt.WA_TranslucentBackground imported from PyQt5.QtCore.
        # self.setWindowFlag(Qt.FramelessWindowHint)
        # self.setAttribute(Qt.WA_TranslucentBackground)

    # def initialize_firebase(self):
    #     if not firebase_admin._apps:  # Check if Firebase is already initialized
    #         try:
    #             cred = credentials.Certificate(KEY_PATH)
    #             firebase_admin.initialize_app(cred)
    #             print("Firebase Admin SDK initialized successfully.")
    #         except FileNotFoundError:
    #             print(f"Error: Service account key file not found at {KEY_PATH}. Please ensure the file exists.")
    #             # Optionally, disable login button or show error on UI
    #             self.ui.pushButton_login.setEnabled(False)
    #             self.ui.label_error.setText(f"Firebase Error: Key file not found.\nPlease check console.")
    #         except Exception as e:
    #             print(f"An error occurred during Firebase initialization: {e}")
    #             # Optionally, disable login button or show error on UI
    #             self.ui.pushButton_login.setEnabled(False)
    #             self.ui.label_error.setText(f"Firebase Error: {e}\nPlease check console.")
    #
    # def handle_login(self):
    #     email = self.ui.lineEdit_email.text()
    #     password = self.ui.lineEdit_password.text()
    #     self.ui.label_error.setText("")  # Clear previous errors
    #
    #     if not FIREBASE_WEB_API_KEY or FIREBASE_WEB_API_KEY == "YOUR_FIREBASE_WEB_API_KEY":
    #         self.ui.label_error.setText("Error: Firebase Web API Key not configured.\nPlease check login_screen.py.")
    #         print(
    #             "Error: FIREBASE_WEB_API_KEY is not configured in login_screen.py. Please replace 'YOUR_FIREBASE_WEB_API_KEY' with your actual key.")
    #         return
    #
    #     rest_api_url = f"https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword?key={FIREBASE_WEB_API_KEY}"
    #     payload = {
    #         'email': email,
    #         'password': password,
    #         'returnSecureToken': True
    #     }
    #
    #     try:
    #         response = requests.post(rest_api_url, data=json.dumps(payload),
    #                                  headers={'Content-Type': 'application/json'})
    #         response_data = response.json()
    #
    #         if response.status_code == 200:
    #             id_token = response_data.get('idToken')
    #             local_id = response_data.get('localId')  # User's UID
    #             print(f"Login successful! User UID: {local_id}, ID Token: {id_token}")
    #
    #             # Proceed to main application window
    #             self.main_win.show()
    #             self.close()  # Close the login window
    #         else:
    #             error_info = response_data.get('error', {})
    #             message = error_info.get('message', 'Unknown authentication error.')
    #             print(f"Login failed: {message}. Full error: {response_data}")
    #             self.ui.label_error.setText(f"Login Failed: {message}")
    #             self.ui.lineEdit_password.setText("")  # Clear password field
    #
    #     except requests.exceptions.RequestException as e:
    #         print(f"Network error during login: {e}")
    #         self.ui.label_error.setText(f"Network error: Please check your connection.")
    #         self.ui.lineEdit_password.setText("")  # Clear password field
    #     except json.JSONDecodeError:
    #         print(
    #             f"Error decoding JSON response from Firebase. Status: {response.status_code}, Response text: {response.text}")
    #         self.ui.label_error.setText("Error: Invalid response from server.")
    #         self.ui.lineEdit_password.setText("")  # Clear password field
    #     except Exception as e:
    #         print(f"An unexpected error occurred during login: {e}")
    #         self.ui.label_error.setText(f"An unexpected error occurred.")
    #         self.ui.lineEdit_password.setText("")  # Clear password field


if __name__ == '__main__':
    app = QApplication(sys.argv)
    login_window = LoginScreen()
    login_window.show()
    sys.exit(app.exec_())
