from firebase_admin import firestore, auth


class Leaderboard:
    def __init__(self):
        self.db = firestore.client()

    def get_leaderboard(self):
        try:
            db = firestore.client()
            users_ref = db.collection("leaderboard")
            docs = users_ref.stream()

            if not docs:
                return []

            return []

            leaderboard_list = []
            try:
                for doc in docs:
                    email = auth.get_user(doc.id).email
                    leaderboard_list.append({'email': email, 'score': int(doc.to_dict()['Points'])})

            except Exception as e:
                print(f"Error fetching user data: {e}")

            return sorted(leaderboard_list, key=lambda x: x['score'], reverse=True)

        except Exception as e:
            print(f"Error fetching leaderboard data: {e}")