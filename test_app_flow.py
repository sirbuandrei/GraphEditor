import unittest
from unittest.mock import patch, MagicMock
import sys

from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import QTimer, Qt

# Add the project root to sys.path if tests are run from a different directory
# import os
# sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from main import SplashScreen, MainWindow
from login_screen import LoginScreen
import login_screen # To patch FIREBASE_WEB_API_KEY
import firebase_admin

# Global reference to QApplication to avoid re-creation issues
app = None

class TestAppFlow(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        global app
        if QApplication.instance():
            app = QApplication.instance()
        else:
            app = QApplication(sys.argv)
        cls.app = app

    def setUp(self):
        self.splash_screen = None
        self.login_screen_instance = None
        self.main_window_instance = None

        # Clean up firebase_admin apps before each test if necessary
        # This is important if initialize_app is called multiple times across tests
        # without proper cleanup, which can lead to errors.
        # However, since we are mocking initialize_app for the login test,
        # and the splash test doesn't use it directly, this might not be strictly needed.
        # If firebase_admin.initialize_app was called in a previous test without full mocking,
        # this might be useful.
        if firebase_admin._apps:
             # A bit of a hack, as there's no public "reset" for firebase_admin SDK
             # This is to ensure tests don't interfere with each other regarding Firebase init state.
             # For robust testing, more sophisticated mocking or setup/teardown of Firebase might be needed.
            firebase_admin._apps.clear()


    def tearDown(self):
        # Close any windows that might have been opened
        if self.splash_screen and self.splash_screen.isVisible():
            self.splash_screen.close()
        if self.login_screen_instance and self.login_screen_instance.isVisible():
            self.login_screen_instance.close()
        if self.main_window_instance: # MainWindow might be self.login_screen_instance.main_win
             if self.login_screen_instance and self.login_screen_instance.main_win.isVisible():
                self.login_screen_instance.main_win.close()
        
        # Process events to ensure windows are actually closed
        self.app.processEvents()


    def test_splash_to_login_transition(self):
        """Test that the SplashScreen transitions to the LoginScreen."""
        self.splash_screen = SplashScreen()
        self.splash_screen.show()
        self.app.processEvents() # Allow splash screen to show

        # login_win is created in SplashScreen's __init__
        login_window = self.splash_screen.login_win 
        self.assertIsNotNone(login_window, "Login window should be instantiated by SplashScreen")
        self.assertFalse(login_window.isVisible(), "Login window should not be visible initially")

        # Simulate the progress bar completing
        # Directly manipulating the counter and calling progress()
        # is more reliable in a test than depending on QTimer.
        global counter # Access the global counter from main.py
        original_counter_value = counter
        counter = 0 # Ensure counter starts at 0 for the test

        while counter <= 100:
            self.splash_screen.progress()
            self.app.processEvents() # Process events like UI updates

        # After loop, counter is > 100, progress() should have triggered transition
        self.assertTrue(login_window.isVisible(), "Login window should be visible after splash screen finishes")
        self.assertFalse(self.splash_screen.isVisible(), "Splash screen should be hidden after it finishes")
        
        # Clean up counter
        counter = original_counter_value
        
        # Ensure login_window is closed for subsequent tests
        if login_window.isVisible():
            login_window.close()
        self.app.processEvents()


    @patch('login_screen.requests.post')
    @patch('firebase_admin.initialize_app')
    @patch('firebase_admin.credentials.Certificate')
    @patch('login_screen.FIREBASE_WEB_API_KEY', 'test_api_key') # Patch the constant in the module
    def test_login_to_main_transition(self, mock_certificate, mock_initialize_app, mock_post):
        """Test that the LoginScreen transitions to the MainWindow on successful login."""
        
        # Mock Firebase Admin SDK initialization
        # mock_certificate.return_value = MagicMock() # Don't care about its return for this
        # mock_initialize_app.return_value = None # Simulate successful initialization
        
        # If initialize_firebase is called in __init__, it needs to not fail.
        # The patches for Certificate and initialize_app should handle this.
        # We also ensure that firebase_admin._apps is empty before this test.
        # (Handled in setUp for now, but could be more targeted if needed)

        # Configure the mock for requests.post
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {'idToken': 'fake_token', 'localId': 'fake_user_id'}
        mock_post.return_value = mock_response

        self.login_screen_instance = LoginScreen()
        # The initialize_firebase call in LoginScreen.__init__ should now use the mocks
        
        # Check if initialization disabled the login button (it shouldn't with mocks)
        self.assertTrue(self.login_screen_instance.ui.pushButton_login.isEnabled(), 
                        "Login button should be enabled with Firebase init mocked.")

        self.login_screen_instance.show()
        self.app.processEvents()
        
        self.assertFalse(self.login_screen_instance.main_win.isVisible(), "Main window should not be visible initially")

        # Simulate user input
        self.login_screen_instance.ui.lineEdit_email.setText("test@example.com")
        self.login_screen_instance.ui.lineEdit_password.setText("password123")
        self.app.processEvents()

        # Click the login button (by directly calling handle_login)
        self.login_screen_instance.handle_login()
        self.app.processEvents() # Allow signals and UI updates

        self.assertTrue(self.login_screen_instance.main_win.isVisible(), "Main window should be visible after login")
        self.assertFalse(self.login_screen_instance.isVisible(), "Login screen should be hidden after login")

        # Store main_window_instance for teardown
        self.main_window_instance = self.login_screen_instance.main_win


if __name__ == '__main__':
    unittest.main()
