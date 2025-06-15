from PyQt5.QtCore import Qt, QThread, QObject, pyqtSignal
from PyQt5.QtWidgets import QTableWidgetItem


class LeaderboardPresenter:
    def __init__(self, leaderboard_page, leaderboard_model):
        self.leaderboard_page = leaderboard_page
        self.leaderboard_model = leaderboard_model

        self.leaderboard_page.show_page.connect(self.show_leaderboard)
        self.leaderboard_model.finished.connect(self.on_leaderboard_loaded)

    def show_leaderboard(self):
        self.leaderboard_page.set_loading(True)

        self.thread = QThread()
        self.leaderboard_model.moveToThread(self.thread)

        self.thread.started.connect(self.leaderboard_model.get_leaderboard)
        self.leaderboard_model.finished.connect(self.thread.quit)
        #self.leaderboard_model.finished.connect(self.leaderboard_model.deleteLater)
        #self.leaderboard_model.finished.connect(self.on_leaderboard_loaded)
        self.thread.finished.connect(self.thread.deleteLater)

        self.thread.start()

    def on_leaderboard_loaded(self, data):
        self.leaderboard_page.set_loading(False)
        self.leaderboard_page.update_leaderboard(data)
