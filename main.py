import os, sys, yaml

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
from views.splash_screen import SplashScreen


#TODO: splash screen

def load_config(filepath='config.yaml'):
    req_keys = ['DATABASE', 'KEY_PATH', 'API_KEY']

    try:
        if not os.path.exists(filepath):
            raise FileNotFoundError(f"Configuration file '{filepath}' not found.")

        with open(filepath, 'r') as stream:
            try:
                config = yaml.safe_load(stream)
                print(config)
            except yaml.YAMLError as exc:
                raise ValueError(f"YAML parsing error: {exc}")

        if not isinstance(config, dict):
            raise ValueError(f"The configuration in '{filepath}' is empty or malformed.")

        missing_keys = [key for key in req_keys if key not in config]
        if missing_keys:
            raise KeyError(f"Missing keys in config: {', '.join(missing_keys)}")

        return config

    except (FileNotFoundError, KeyError, ValueError) as e:
        print(f"Configuration Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    app = QApplication(sys.argv)

    config = load_config()

    cred = credentials.Certificate(config['KEY_PATH'])
    firebase_app = firebase_admin.initialize_app(cred, {'databaseURL': config['DATABASE']})

    graph_model = GraphModel()
    user_model = UserModel(config['API_KEY'])

    login_screen = LoginScreen()
    input_page = InputPage()
    config_page = ConfigPage()
    leaderboard_page = LeaderboardPage()
    graph_view = GraphView()
    main_window = MainWindow()
    #splash_screen = SplashScreen()

    leaderboard_presenter = LeaderboardPresenter(leaderboard_page, LeaderboardModel)
    input_presenter = InputPresenter(input_page, graph_model)
    graph_presenter = GraphPresenter(graph_view, graph_model)
    coordinator = Coordinator(config_page, graph_view, graph_model)

    def start_app(user_id):
        coordinator.set_current_user(user_id)
        main_window.set_pages(input_page, config_page, leaderboard_page, graph_view)
        main_window.show()

    login_presenter = LoginPresenter(login_screen, user_model, on_login_success=start_app)

    sys.exit(app.exec_())
