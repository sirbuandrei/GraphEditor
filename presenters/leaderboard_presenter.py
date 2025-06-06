from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QTableWidgetItem


class LeaderboardPresenter:
    def __init__(self, leaderboard_page, leaderboard_model):
        self.leaderboard_page = leaderboard_page
        self.leaderboard_model = leaderboard_model

        self.leaderboard_page.show_page.connect(self.show_leaderboard)

    def show_leaderboard(self):
        leaderboard = self.leaderboard_model.get_leaderboard()
        self.leaderboard_page.tableWidget_leaderboard.setRowCount(len(leaderboard))

        if not bool(leaderboard):
            return

        for row, entry in enumerate(leaderboard):
            email_item = QTableWidgetItem(str(entry['email']))
            score_item = QTableWidgetItem(str(entry['score']))
            score_item.setTextAlignment(Qt.AlignCenter)

            self.leaderboard_page.tableWidget_leaderboard.setItem(row, 0, email_item)
            self.leaderboard_page.tableWidget_leaderboard.setItem(row, 1, score_item)

    def update_leaderboard(self):
        ...