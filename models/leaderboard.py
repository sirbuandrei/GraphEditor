from firebase_admin import firestore, auth


class Leaderboard:
    def __init__(self):
        self.db = firestore.client()

    def get_leaderboard(self):
        try:
            users_ref = self.db.collection("leaderboard")
            docs = users_ref.stream()

            if not docs:
                return []

            leaderboard_list = []
            for doc in docs:
                email = auth.get_user(doc.id).email
                leaderboard_list.append({'email': email, 'score': int(doc.to_dict()['Points'])})

            return sorted(leaderboard_list, key=lambda x: x['score'], reverse=True)

        except Exception as e:
            print(f"Error fetching leaderboard data: {e}")