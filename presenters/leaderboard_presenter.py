from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QTableWidgetItem


class LeaderboardPresenter:
    def __init__(self, leaderboard_page, leaderboard_model):
        self.leaderboard_page = leaderboard_page
        self.leaderboard_model = leaderboard_model

        self.leaderboard_page.show_page.connect(self.show_leaderboard)

    def show_leaderboard(self):
        leaderboard = self.leaderboard_model.get_leaderboard()
        print(leaderboard)

    def update_leaderboard(self):
        ...