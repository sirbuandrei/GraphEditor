import sys

from PyQt5.QtWidgets import QApplication

import firebase_admin
from firebase_admin import credentials

from models.graph_model import GraphModel
from models.leaderboard_model import LeaderboardModel
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
from presenters.coordinator import Coordinator

DATABASE = 'https://graph-editor-database-default-rtdb.europe-west1.firebasedatabase.app/'
KEY_PATH = r"C:\Users\andre\OneDrive\Documents\GitHub\GraphEditor\FirebaseKey\graph-editor-database-firebase-adminsdk-fbsvc-1b066eac85.json"
API_KEY = 'AIzaSyAp5_l7wA6a__54DT8mUfH7RlNyoMLrHLI'

if __name__ == "__main__":
    app = QApplication(sys.argv)

    cred = credentials.Certificate(KEY_PATH)
    firebase_app = firebase_admin.initialize_app(cred, {'databaseURL': DATABASE})

    graph_model = GraphModel()
    user_model = UserModel(API_KEY)

    login_screen = LoginScreen()
    input_page = InputPage()
    config_page = ConfigPage()
    leaderboard_page = LeaderboardPage()
    graph_view = GraphView()
    main_window = MainWindow()

    leaderboard_presenter = LeaderboardPresenter(leaderboard_page, LeaderboardModel)
    input_presenter = InputPresenter(input_page, graph_model)
    graph_presenter = GraphPresenter(graph_view, graph_model)
    coordinator = Coordinator(config_page, graph_view, graph_model)

    def start_app(user_id):
        print(user_id)
        coordinator.set_current_user(user_id)
        main_window.set_pages(input_page, config_page, leaderboard_page, graph_view)
        # splash screen.show()
        main_window.show()

    login_presenter = LoginPresenter(login_screen, user_model, on_login_success=start_app)

    sys.exit(app.exec_())
