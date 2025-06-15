from PyQt5.QtCore import QObject, pyqtSignal
from firebase_admin import auth, db


class LeaderboardModel(QObject):
    finished = pyqtSignal(list)

    def __init__(self):
        super().__init__()

    def get_leaderboard(self):
        try:
            ref = db.reference('leaderboard')
            data = ref.get()

            if not data:
                return []

            result = []
            for id, value in data.items():
                email = auth.get_user(id).email
                points = value.get('points', 0)
                result.append((email, points))

            result.sort(key=lambda x: x[1], reverse=True)
            self.finished.emit(result)

        except Exception as e:
            print(f"Error fetching leaderboard data: {e}")
            self.finished.emit([])