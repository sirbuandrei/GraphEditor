from PyQt5.QtCore import QThread


class LeaderboardPresenter:
    def __init__(self, leaderboard_page, leaderboard_model):
        self.leaderboard_page = leaderboard_page
        self.leaderboard_model = leaderboard_model

        self.leaderboard_page.show_page.connect(self.show_leaderboard)

    def show_leaderboard(self):
        self.leaderboard_page.set_loading(True)

        self.thread = QThread()
        self.worker = self.leaderboard_model()
        self.worker.moveToThread(self.thread)

        self.thread.started.connect(self.worker.get_leaderboard)
        self.worker.finished.connect(self.thread.quit)
        self.worker.finished.connect(self.on_leaderboard_loaded)
        self.worker.finished.connect(self.worker.deleteLater)
        self.thread.finished.connect(self.thread.deleteLater)

        self.thread.start()

    def on_leaderboard_loaded(self, data):
        self.leaderboard_page.set_loading(False)
        self.leaderboard_page.update_leaderboard(data)
