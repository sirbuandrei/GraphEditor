import requests, json


class UserModel:
    def __init__(self, API_KEY):
        self._key = API_KEY

    def login(self, email, password):
        url = f"https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword?key={self._key}"
        payload = {
            "email": email,
            "password": password,
            "returnSecureToken": True
        }

        response = requests.post(url, json=payload)
        if response.status_code == 200:
            return True, response.json()['localId']
        else:
            return False, response.json()['error']['message']

    def register(self, email, password):
        url = f"https://identitytoolkit.googleapis.com/v1/accounts:signUp?key={self._key}"
        payload = {
            "email": email,
            "password": password,
            "returnSecureToken": True
        }

        response = requests.post(url, json=payload)
        if response.status_code == 200:
            return True, response.json()
        else:
            return False, response.json()['error']['message']