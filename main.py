import sys

from PyQt5.QtCore import QPointF
from PyQt5.QtWidgets import QApplication

from models.graph_model import GraphModel
from models.leaderboard import Leaderboard
from models.user_model import UserModel

from views.config_page import ConfigPage
from views.input_page import InputPage
from views.leaderboard_page import LeaderboardPage
from views.login_screen import LoginScreen
from views.graph_view import GraphView
from views.main_window import MainWindow

from presenters.login_presenter import LoginPresenter
from presenters.leaderboard_presenter import LeaderboardPresenter
from presenters.input_presenter import InputPresenter
from presenters.graph_presenter import GraphPresenter
from views.node import Node

#counter = 0  # PROGRESS BAR COUNTER

# class MainWindow(QMainWindow, Ui_MainWindow):
#     """Clasa principala a aplicatiei
#
#     Atribute
#     --------
#     funtions : Ui_Functions
#         funtiile window-ului
#     Restul de atribute sunt mostenite
#     de la clasa Ui_MainWindow
#
#     Metode
#     ------
#     setup_ui_functions()
#         atribuirea de functii
#     setup_initial_settings()
#         setarile initiale
#     setup_key_timer()
#         crearea unui timer
#     eventFilter(obj, event)
#         manipuleaza eventurile aplicatiei
#     """
#
#     def __init__(self, user_uid=None):
#         super(MainWindow, self).__init__()
#         self.user_uid = user_uid
#         self.setupUi(self)
#         self.functions = Ui_Functions(self)
#         self.setup_ui_functions()
#         self.setup_initial_settings()
#         self.setup_key_timer()
#
#         # Insaland un event filter se vor putea manipula mai
#         # bine eventurile care provin de la aceste atribute
#         self.textEdit_node_data.installEventFilter(self)
#         self.frame_actions_btns.installEventFilter(self)
#
#     def setup_ui_functions(self):
#         """Atribuirea functilor specifice fiecarui buton"""
#
#         self.pushButton_close.clicked.connect(lambda: self.close())
#         self.pushButton_minimize.clicked.connect(lambda: self.showMinimized())
#         self.pushButton_maximize.clicked.connect(self.functions.maximize_restore)
#         self.pushButton_mode.clicked.connect(self.functions.change_theme)
#         self.pushButton_settings.clicked.connect(self.functions.show_settings_page)
#         self.pushButton_run_commands.clicked.connect(self.functions.run_commands)
#         self.pushButton_save_graph.clicked.connect(self.functions.save_graph)
#         self.pushButton_leaderboard.clicked.connect(self.functions.show_leaderboard_page)
#         self.pushButton_force_mode.clicked.connect(self.functions.force_mode)
#         self.pushButton_home.clicked.connect(self.functions.show_home_page)
#         self.pushButton_directed.clicked.connect(self.functions.select_directed)
#         self.pushButton_undirected.clicked.connect(self.functions.select_undirected)
#         self.pushButton_clear_DFS.clicked.connect(self.functions.DFS_clear)
#         self.pushButton_clear_BFS.clicked.connect(self.functions.BFS_clear)
#         self.pushButton_clear_DIJKSTRA.clicked.connect(self.functions.DIJKSTRA_clear)
#         self.pushButton_user_algorithm.clicked.connect(self.functions.run_custom_algorithm)
#
#     def setup_initial_settings(self):
#         """Setarile intiale ale aplicatiei"""
#
#         self.setAttribute(Qt.WA_DeleteOnClose)
#         self.setWindowFlag(Qt.FramelessWindowHint)
#
#         self.frame_change_settings.hide()
#
#         self.spinBox_node_radius.setRange(10, 30)
#         self.spinBox_node_radius.setValue(15)
#
#         self.pushButton_mode.click()
#         self.pushButton_force_mode.click()
#         self.pushButton_undirected.click()
#
#     def setup_key_timer(self):
#         """Creearea unui timer pentru taste
#
#         Pentru a optimiza trimiterea datelor grafului catre engine, se
#         implementeaza un key timer pentru a impiedica trimiterea datelor la
#         fiecare tasta apasata. Datele vor fi trimise la 0.8 secude dupa oprirea
#         din tastat, in cazul in care se apasa o tasta inainte de 0.8 secunde
#         de la ultima apasare timer-ul se va reseta. Astfel se vor operatiile
#         de manipulare a datelor grafului se vor efectua de mai putine ori.
#         """
#
#         self.keyTimer = QTimer()
#         self.keyTimer.setSingleShot(True)
#         self.keyTimer.setInterval(800)
#         self.keyTimer.timeout.connect(self.functions.send_data)
#
#     def eventFilter(self, obj, event):
#         """Filtrarea event-urilor aplicatiei
#
#         Event-urile importante provin de la 2 atribute : textEdit_node_data
#         si frame_actions_btns.
#         De la textEdit_node_data se va manipula event-ul de KeyPress, de
#         fiecare data cand o tasta este apasata in interiorul textEdit_node_data
#         se va reseta timer-ul pentru tastat. Alte event-uri de KeyPress nu sunt
#         relevante.
#         De la frame_actions_btns se vor manipula event-urile : MouseButtonDblClick,
#         MouseButtonPress, MouseMove . Primul event va maximiza / micsora aplicatia
#         in cazul unui dublu click pe frame-ul superior. Cel de-al doilea event tine
#         minte pozitia in care se apasa frame-ul superior pentru ca mai apoi sa fie
#         folosita de event-ul MouseMove puntru a muta window-ul aplicatiei, in cazul
#         miscarii de mouse-ului.
#
#         Parametrii
#         ----------
#         obj : QObject
#             obiectul care trimite eventul
#         event : QEvent
#             tipul de event
#         """
#
#         if obj == self.textEdit_node_data and event.type() == QEvent.KeyPress:
#             self.keyTimer.start()
#
#         elif obj == self.frame_actions_btns:
#
#             if event.type() == QEvent.MouseButtonDblClick:
#                 self.functions.maximize_restore()
#
#             elif event.type() == QEvent.MouseButtonPress:
#                 self.drag_pos = event.pos()
#
#             elif event.type() == QEvent.MouseMove:
#                 if not self.isMaximized():
#                     self.move(event.globalPos() - self.drag_pos)
#                 # else:
#                 #     self.functions.maximize_restore()
#                 #     #self.move(self.drag_pos)
#                 #     #print(ratio)
#                 #     # TODO: check bug
#
#         return super(MainWindow, self).eventFilter(obj, event)


# class LoginScreen(QMainWindow):
#     def __init__(self):
#         super().__init__()
#         self.initialize_firebase()
#         self.ui = Ui_LoginScreen()
#         self.ui.setupUi(self)
#         self.ui.pushButton_login.clicked.connect(self.handle_login)
#         self.ui.pushButton_register.clicked.connect(self.handle_register)
#
#     def initialize_firebase(self):
#         if not firebase_admin._apps:  # Check if Firebase is already initialized
#             try:
#                 cred = credentials.Certificate(KEY_PATH)
#                 firebase_admin.initialize_app(cred)
#                 print("Firebase Admin SDK initialized successfully.")
#             except FileNotFoundError:
#                 print(f"Error: Service account key file not found at {KEY_PATH}. Please ensure the file exists.")
#                 # Optionally, disable login button or show error on UI
#                 #self.ui.pushButton_login.setEnabled(False)
#                 #self.ui.label_error.setText(f"Firebase Error: Key file not found.\nPlease check console.")
#             except Exception as e:
#                 print(f"An error occurred during Firebase initialization: {e}")
#                 # Optionally, disable login button or show error on UI
#                 #self.ui.pushButton_login.setEnabled(False)
#                 #self.ui.label_error.setText(f"Firebase Error: {e}\nPlease check console.")
#
#     def handle_login(self):
#         email = self.ui.lineEdit_email.text()
#         password = self.ui.lineEdit_password.text()
#
#
#         self.ui.label_error.setText("")  # Clear previous errors
#
#         if not FIREBASE_WEB_API_KEY or FIREBASE_WEB_API_KEY == "YOUR_FIREBASE_WEB_API_KEY":
#             self.ui.label_error.setText("Error: Firebase Web API Key not configured.\nPlease check login_screen.py.")
#             print(
#                 "Error: FIREBASE_WEB_API_KEY is not configured in login_screen.py. Please replace 'YOUR_FIREBASE_WEB_API_KEY' with your actual key.")
#             return
#
#         rest_api_url = f"https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword?key={FIREBASE_WEB_API_KEY}"
#         payload = {
#             'email': email,
#             'password': password,
#             'returnSecureToken': True
#         }
#
#         try:
#             response = requests.post(rest_api_url, data=json.dumps(payload),
#                                      headers={'Content-Type': 'application/json'})
#             response_data = response.json()
#
#             if response.status_code == 200:
#                 id_token = response_data.get('idToken')
#                 local_id = response_data.get('localId')  # User's UID
#                 print(f"Login successful! User UID: {local_id}, ID Token: {id_token}")
#
#                 # Proceed to main application window
#                 MainWindow(local_id).show()
#                 self.close()  # Close the login window
#             else:
#                 error_info = response_data.get('error', {})
#                 message = error_info.get('message', 'Unknown authentication error.')
#                 print(f"Login failed: {message}. Full error: {response_data}")
#                 self.ui.label_error.setText(f"Login Failed: {message}")
#                 self.ui.lineEdit_password.setText("")  # Clear password field
#
#         except requests.exceptions.RequestException as e:
#             print(f"Network error during login: {e}")
#             self.ui.label_error.setText(f"Network error: Please check your connection.")
#             self.ui.lineEdit_password.setText("")  # Clear password field
#         except json.JSONDecodeError:
#             print(
#                 f"Error decoding JSON response from Firebase. Status: {response.status_code}, Response text: {response.text}")
#             self.ui.label_error.setText("Error: Invalid response from server.")
#             self.ui.lineEdit_password.setText("")  # Clear password field
#         except Exception as e:
#             print(f"An unexpected error occurred during login: {e}")
#             self.ui.label_error.setText(f"An unexpected error occurred.")
#             self.ui.lineEdit_password.setText("")  # Clear password field
#
#     def handle_register(self):
#         email = self.ui.lineEdit_email.text()
#         password = self.ui.lineEdit_password.text()
#         self.ui.label_error.setText("")  # Clear previous errors
#
#         if not FIREBASE_WEB_API_KEY or FIREBASE_WEB_API_KEY == "YOUR_FIREBASE_WEB_API_KEY":
#             self.ui.label_error.setText("Error: Firebase Web API Key not configured.\nPlease check login_screen.py.")
#             print(
#                 "Error: FIREBASE_WEB_API_KEY is not configured in login_screen.py. Please replace it with your actual key.")
#             return
#
#         if not email or not password:
#             self.ui.label_error.setText("Email and password cannot be empty.")
#             return
#
#         if len(password) < 6:
#             self.ui.label_error.setText("Password must be at least 6 characters.")
#             return
#
#         rest_api_url = f"https://identitytoolkit.googleapis.com/v1/accounts:signUp?key={FIREBASE_WEB_API_KEY}"
#         payload = {
#             'email': email,
#             'password': password,
#             'returnSecureToken': True
#         }
#
#         try:
#             response = requests.post(rest_api_url, data=json.dumps(payload),
#                                      headers={'Content-Type': 'application/json'})
#             response_data = response.json()
#
#             if response.status_code == 200:
#                 local_id = response_data.get('localId')
#                 print(f"Registration successful! User UID: {local_id}")
#                 self.ui.label_error.setStyleSheet("color: lightgreen; font: 10pt 'Segoe UI';")
#                 self.ui.label_error.setText("Registration successful! You can now log in.")
#                 self.ui.lineEdit_password.setText("")  # Clear password field
#             else:
#                 error_info = response_data.get('error', {})
#                 message = error_info.get('message', 'Unknown registration error.')
#                 print(f"Registration failed: {message}")
#                 self.ui.label_error.setStyleSheet("color: red; font: 10pt 'Segoe UI';")
#                 self.ui.label_error.setText(f"Registration Failed: {message}")
#                 self.ui.lineEdit_password.setText("")
#
#         except requests.exceptions.RequestException as e:
#             print(f"Network error during registration: {e}")
#             self.ui.label_error.setText("Network error: Please check your connection.")
#             self.ui.lineEdit_password.setText("")
#         except Exception as e:
#             print(f"Unexpected error during registration: {e}")
#             self.ui.label_error.setText("Unexpected error occurred.")
#             self.ui.lineEdit_password.setText("")


# class SplashScreen(QMainWindow):
#     """SpalshScreen-ul de inceput"""
#
#     def __init__(self):
#         QMainWindow.__init__(self)
#         self.login_win = LoginScreen() # Instantiating LoginScreen
#         self.ui = Ui_SplashScreen()
#         self.ui.setupUi(self)
#
#         # REMOVE TITLE BAR
#         self.setWindowFlag(Qt.FramelessWindowHint)
#         self.setAttribute(Qt.WA_TranslucentBackground)
#
#         # DROP SHADOW EFFECT
#         self.shadow = QGraphicsDropShadowEffect(self)
#         self.shadow.setBlurRadius(40)
#         self.shadow.setXOffset(0)
#         self.shadow.setYOffset(0)
#         self.shadow.setColor(QColor(0, 0, 0, 60))
#         self.ui.dropShadowFrame.setGraphicsEffect(self.shadow)
#
#         # INITIAL TEXT
#         self.ui.label_loading.setText("loading...")
#
#         # CHANGE LOADING DOTS
#         QTimer.singleShot(750, lambda: self.ui.label_loading.setText("loading."))
#         QTimer.singleShot(1500, lambda: self.ui.label_loading.setText("loading.."))
#         QTimer.singleShot(2250, lambda: self.ui.label_loading.setText("loading..."))
#         QTimer.singleShot(3000, lambda: self.ui.label_loading.setText("loading."))
#         QTimer.singleShot(3750, lambda: self.ui.label_loading.setText("loading.."))
#         QTimer.singleShot(4500, lambda: self.ui.label_loading.setText("loading..."))
#
#         # PROGRESS BAR TIMER
#         self.time = QTimer()
#         self.time.timeout.connect(self.progress)
#         self.time.start(75)
#
#         self.show()
#
#     def progress(self):
#         global counter
#
#         # UPDATE PROGRESS BAR
#         self.ui.progressBar.setValue(counter)
#
#         # STOP THE TIMER
#         if counter > 100:
#             self.time.stop()
#             self.login_win.show() # Show LoginScreen instead of MainWindow
#             self.close()
#
#         counter += 5


if __name__ == "__main__":
    app = QApplication(sys.argv)

    # Models
    graph_model = GraphModel()
    user_model = UserModel()
    leaderboard_model = Leaderboard()

    # Views
    login_screen = LoginScreen()
    input_page = InputPage()
    config_page = ConfigPage()
    leaderboard_page = LeaderboardPage()
    graph_view = GraphView()

    def show_main_window(user_id):
        main_window = MainWindow(user_id)

        main_window.set_pages(input_page, config_page, leaderboard_page, graph_view)

        main_window.show()

    login_presenter = LoginPresenter(login_screen, user_model, on_login_success=show_main_window)
    leaderboard_presenter = LeaderboardPresenter(leaderboard_page, leaderboard_model)
    input_presenter = InputPresenter(input_page, graph_model)
    graph_presenter = GraphPresenter(graph_view, graph_model)

    sys.exit(app.exec_())
