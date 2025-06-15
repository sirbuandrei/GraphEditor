from firebase_admin import db, auth


class LeaderboardModel:
    def __init__(self):
        self.ref = db.reference('leaderboard')

    def get_leaderboard(self):
        try:
            data = self.ref.get()

            if not data:
                return []

            result = []
            for id, entry in data.items():
                email = auth.get_user(id).email
                points = entry.get('points', 0)
                result.append((email, points))

            result.sort(key=lambda x: x[1], reverse=True)
            return result

        except Exception as e:
            print(f"Error fetching leaderboard data: {e}")