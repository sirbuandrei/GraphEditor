# PyQt5 Graph Editor and Algorithm Visualizer

This is a PyQt5-based desktop application for visualizing graphs and graph algorithms.

---

## Requirements

- Python 3.8 or higher
- Firebase Realtime Database project
- Firebase Admin SDK credentials
- Firebase Web API Key

---

## 📦 Installation

### 1. Clone the repository

git clone https://... \

---

### 2. Set up a Firebase project

To use authentication and leaderboard features, set up Firebase:

1. Go to https://console.firebase.google.com/
2. Create a new project.
3. In the **Authentication** tab, enable **Email/Password** sign-in.
4. In the **Realtime Database**, create a new database and choose a region.
5. In **Project Settings > Service Accounts**, generate a new private key and download the `.json` file.

---

### 3. Create `config.yaml`

Inside the root directory of the project, change the file named `config.yaml` and fill in the following fields:

DATABASE: "https://your-project-id.firebaseio.com/" \
KEY_PATH: "path/to/your/firebase-key.json" \
API_KEY: "your-firebase-web-api-key"
---

### 4. Install dependencies

Make sure you're in a Python 3.8+ virtual environment, then run:

pip install -r requirements.txt

---

## 5. Running the App

Once everything is set up, run:

python main.py

The app will start at the login screen. After logging in, a splash screen will appear, followed by the main window.
