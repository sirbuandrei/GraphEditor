"""Fisierul contine clasa care raspunde de funtiile interfatei"""
from traceback import print_tb

from PyQt5 import QtCore, QtWidgets, QtGui
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon, QPen
from PyQt5.QtWidgets import QFileDialog, QInputDialog, QMessageBox, QTableWidgetItem
from styles import Styles

import firebase_admin
from firebase_admin import firestore, auth

from user_algorithm_dialog import UserAlgorithmDialog
from PyQt5 import QtCore, QtGui, QtWidgets


class StyledMessageBox(QtWidgets.QDialog):
    def __init__(self, parent=None, title="", message="", is_warning=False):
        super().__init__(parent)
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint | QtCore.Qt.Dialog)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.setAttribute(QtCore.Qt.WA_StaticContents, True)

        self.setMinimumSize(350, 180)
        self.setMaximumSize(350, 180)
        self.setSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        self.old_pos = None

        # Main layout
        self.mainLayout = QtWidgets.QVBoxLayout(self)
        self.mainLayout.setContentsMargins(0, 0, 0, 0)
        self.mainLayout.setSpacing(0)

        # Top bar (styled same as body)
        self.titleBar = QtWidgets.QFrame(self)
        self.titleBar.setFixedHeight(30)
        self.titleBar.setStyleSheet("background-color: #2c2f33;")
        self.titleLayout = QtWidgets.QHBoxLayout(self.titleBar)
        self.titleLayout.setContentsMargins(0, 0, 0, 0)

        spacer = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.titleLayout.addItem(spacer)

        self.closeButton = QtWidgets.QPushButton()
        self.closeButton.setIcon(QtGui.QIcon("icons/cil-x.png"))
        self.closeButton.setIconSize(QtCore.QSize(20, 20))
        self.closeButton.setFixedSize(30, 30)
        self.closeButton.setStyleSheet("""
            QPushButton {
                background-color: transparent;
                border: none;
            }
            QPushButton:hover {
                background-color: red;
            }
        """)
        self.closeButton.clicked.connect(self.reject)
        self.titleLayout.addWidget(self.closeButton)

        # Content frame (bottom only rounded)
        self.contentFrame = QtWidgets.QFrame(self)
        self.contentFrame.setStyleSheet("""
            QFrame {
                background-color: #2c2f33;
            }
            QLabel {
                color: white;
                font: 12pt 'Segoe UI';
            }
            QPushButton {
                background-color: #7289da;
                color: white;
                border-radius: 6px;
                font: 11pt 'Segoe UI';
                padding: 5px 15px;
            }
            QPushButton:hover {
                background-color: #5b6eae;
            }
        """)
        self.contentLayout = QtWidgets.QVBoxLayout(self.contentFrame)
        self.contentLayout.setContentsMargins(20, 20, 20, 20)
        self.contentLayout.setSpacing(15)

        icon_prefix = "⚠️ " if is_warning else "ℹ️ "
        self.label = QtWidgets.QLabel(icon_prefix + message)
        self.label.setWordWrap(True)
        self.label.setAlignment(QtCore.Qt.AlignTop | QtCore.Qt.AlignLeft)
        self.label.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        self.label.setMinimumHeight(50)
        self.contentLayout.addWidget(self.label)

        self.ok_button = QtWidgets.QPushButton("OK")
        self.ok_button.clicked.connect(self.accept)
        self.contentLayout.addWidget(self.ok_button, alignment=QtCore.Qt.AlignRight)

        self.mainLayout.addWidget(self.titleBar)
        self.mainLayout.addWidget(self.contentFrame)

        # Make full dialog draggable (no freezing)
        self.mousePressEvent = self.mouse_press_event
        self.mouseMoveEvent = self.mouse_move_event
        self.mouseReleaseEvent = self.mouse_release_event

    def exec_(self):
        if self.parent():
            parent_geom = self.parent().frameGeometry()
            cx = parent_geom.x() + parent_geom.width() // 2
            cy = parent_geom.y() + parent_geom.height() // 2
            self.move(cx - self.width() // 2, cy - self.height() // 2)
        return super().exec_()

    def mouse_press_event(self, event):
        if event.button() == QtCore.Qt.LeftButton:
            self.old_pos = event.globalPos() - self.frameGeometry().topLeft()

    def mouse_move_event(self, event):
        if event.buttons() & QtCore.Qt.LeftButton and self.old_pos:
            self.move(event.globalPos() - self.old_pos)

    def mouse_release_event(self, event):
        self.old_pos = None
        self.update()


class StyledInputDialog(QtWidgets.QDialog):
    def __init__(self, parent=None, title="", label=""):
        super().__init__(parent)
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)

        self.setFixedSize(400, 200)
        self.setObjectName("StyledInputDialog")

        # Main layout
        self.mainLayout = QtWidgets.QVBoxLayout(self)
        self.mainLayout.setContentsMargins(0, 0, 0, 0)
        self.mainLayout.setSpacing(0)

        # Top bar (matches frame color)
        self.titleBar = QtWidgets.QFrame(self)
        self.titleBar.setFixedHeight(30)
        self.titleBar.setStyleSheet("background-color: #2c2f33;")
        self.titleLayout = QtWidgets.QHBoxLayout(self.titleBar)
        self.titleLayout.setContentsMargins(0, 0, 0, 0)
        self.titleLayout.setSpacing(0)

        spacer = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.titleLayout.addItem(spacer)

        self.closeButton = QtWidgets.QPushButton()
        self.closeButton.setIcon(QtGui.QIcon("icons/cil-x.png"))
        self.closeButton.setIconSize(QtCore.QSize(20, 20))
        self.closeButton.setFixedSize(30, 30)
        self.closeButton.setStyleSheet("""
            QPushButton {
                background-color: transparent;
                border: none;
            }
            QPushButton:hover {
                background-color: red;
            }
        """)
        self.closeButton.clicked.connect(self.reject)
        self.titleLayout.addWidget(self.closeButton)

        # Content frame (no top radius)
        self.contentFrame = QtWidgets.QFrame(self)
        self.contentFrame.setStyleSheet("""
            QFrame {
                background-color: #2c2f33;
            }
            QLabel {
                color: white;
                font: 12pt 'Segoe UI';
            }
            QLineEdit {
                background-color: transparent;
                border: none;
                border-bottom: 2px solid white;
                color: white;
                font: 12pt 'Segoe UI';
            }
            QPushButton {
                background-color: #7289da;
                color: white;
                border-radius: 6px;
                font: 11pt 'Segoe UI';
                padding: 5px 15px;
            }
            QPushButton:hover {
                background-color: #95a5de;
            }
        """)
        self.contentLayout = QtWidgets.QVBoxLayout(self.contentFrame)
        self.contentLayout.setContentsMargins(20, 20, 20, 20)
        self.contentLayout.setSpacing(15)

        self.label = QtWidgets.QLabel(label)
        self.label.setWordWrap(True)
        self.label.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred)
        self.contentLayout.addWidget(self.label)

        self.lineEdit = QtWidgets.QLineEdit()
        self.contentLayout.addWidget(self.lineEdit)

        buttonLayout = QtWidgets.QHBoxLayout()
        buttonLayout.addStretch()

        self.ok_button = QtWidgets.QPushButton("OK")
        self.cancel_button = QtWidgets.QPushButton("Cancel")
        buttonLayout.addWidget(self.ok_button)
        buttonLayout.addWidget(self.cancel_button)

        self.contentLayout.addLayout(buttonLayout)

        self.ok_button.clicked.connect(self.accept)
        self.cancel_button.clicked.connect(self.reject)

        self.mainLayout.addWidget(self.titleBar)
        self.mainLayout.addWidget(self.contentFrame)

        # Drag support
        self.old_pos = None
        self.titleBar.mousePressEvent = self.mouse_press_event
        self.titleBar.mouseMoveEvent = self.mouse_move_event

    def getText(self):
        return self.lineEdit.text()

    def mouse_press_event(self, event):
        if event.button() == QtCore.Qt.LeftButton:
            self.old_pos = event.globalPos()

    def mouse_move_event(self, event):
        if self.old_pos:
            delta = event.globalPos() - self.old_pos
            self.move(self.pos() + delta)
            self.old_pos = event.globalPos()

    def showEvent(self, event):
        super().showEvent(event)
        if self.parent():
            parent_geom = self.parent().frameGeometry()
            parent_center_x = parent_geom.width()
            parent_center_y = parent_geom.height()

            dialog_width = self.width()
            dialog_height = self.height()

            self.move(
                parent_center_x // 2 - dialog_width // 2,
                parent_center_y // 2 - dialog_height // 2,
            )


class Ui_Functions(object):
    """Funtiile corespunzatoare butoanelor si window-ului aplicatiei

    Atribute
    --------
    MainWindow : QMainWindow
        window-ul caruia ii corespund funtile
    dark_them : bool
        modul dark

    Metode
    ------
    send_data()
        trimite date catre engine
    maximize_restore()
        schimba starea aplicatiei
    settings_page()
        arata pagina de setari
    run_commands()
        trimite informatii catre engine
    force_mode()
        schimba modul de forte
    select_directed()
        seteaza graful ca unul orientat
    select_undirected()
        seteaza graful ca unul neorientat
    save_graph()
        salveaza graful
    change_theme()
        schimba tema grafului
    """

    def __init__(self, MainWindow):
        self.MainWindow = MainWindow
        self.dark_theme = False

    def send_data(self):
        """Trimite schimbarile facute in datele grafului catre engine"""

        self.MainWindow.view.engine.receive_data(self.MainWindow.textEdit_node_data.toPlainText())

    def maximize_restore(self):
        """Schimba starea aplicatiei in fullscreen sau inapoi la cea initiala"""

        if not self.MainWindow.isMaximized():
            self.MainWindow.pushButton_maximize.setIcon(QIcon(r"icons\cil-window-restore.png"))
            self.MainWindow.showMaximized()
        else:
            self.MainWindow.pushButton_maximize.setIcon(QIcon(r"icons\cil-window-maximize.png"))
            self.MainWindow.showNormal()

    def show_settings_page(self):
        """Arata sau ascunde pagina de setari ale aplicatiei"""

        if self.MainWindow.frame_change_settings.isHidden():
            self.MainWindow.frame_node_data.hide()
            self.MainWindow.frame_leaderboard.hide()
            self.MainWindow.frame_change_settings.show()

    def show_leaderboard_page(self):
        if self.MainWindow.frame_leaderboard.isHidden():
            self.MainWindow.frame_node_data.hide()
            self.MainWindow.frame_change_settings.hide()
            self.MainWindow.frame_leaderboard.show()
            self.populate_leaderboard()

    def show_home_page(self):
        if self.MainWindow.frame_node_data.isHidden():
            self.MainWindow.frame_change_settings.hide()
            self.MainWindow.frame_leaderboard.hide()
            self.MainWindow.frame_node_data.show()

    def populate_leaderboard(self):
        if not hasattr(self.MainWindow, 'tableWidget_leaderboard'):
            print("Error: tableWidget_leaderboard not found in MainWindow UI.")
            return

        table = self.MainWindow.tableWidget_leaderboard
        table.setRowCount(0)
        table.setColumnCount(2)
        table.setHorizontalHeaderLabels(["Email", "Points"])

        if not firebase_admin._apps:
            print("Error: Firebase Admin SDK not initialized. Cannot load leaderboard.")
            table.setRowCount(1)
            item = QTableWidgetItem("Error: Could not connect to Firebase.")
            item.setTextAlignment(Qt.AlignCenter)
            table.setItem(0, 0, item)
            table.setSpan(0, 0, 1, 2)
            return

        try:
            db = firestore.client()
            users_ref = db.collection("leaderboard")
            docs = users_ref.stream()

            if not docs:
                table.setRowCount(1)
                item = QTableWidgetItem("Leaderboard is empty.")
                item.setTextAlignment(Qt.AlignCenter)
                table.setItem(0, 0, item)
                table.setSpan(0, 0, 1, 2)
                return

            leaderboard_list = []
            for doc in docs:
                email = auth.get_user(doc.id).email
                leaderboard_list.append({'email': email, 'score': int(doc.to_dict()['Points'])})

            sorted_leaderboard = sorted(leaderboard_list, key=lambda x: x['score'], reverse=True)

            table.setRowCount(len(sorted_leaderboard))
            for row, entry in enumerate(sorted_leaderboard):
                email_item = QTableWidgetItem(str(entry['email']))
                score_item = QTableWidgetItem(str(entry['score']))
                score_item.setTextAlignment(Qt.AlignCenter)

                table.setItem(row, 0, email_item)
                table.setItem(row, 1, score_item)

            try:
                from PyQt5.QtWidgets import QHeaderView
                header = table.horizontalHeader()
                header.setSectionResizeMode(0, QHeaderView.Stretch)
                header.setSectionResizeMode(1, QHeaderView.ResizeToContents)
            except ImportError:
                print("QHeaderView not available for column resize.")

        except Exception as e:
            print(f"Error fetching or displaying leaderboard data: {e}")
            table.setRowCount(1)
            item = QTableWidgetItem(f"Error loading leaderboard.")
            item.setTextAlignment(Qt.AlignCenter)
            table.setItem(0, 0, item)
            table.setSpan(0, 0, 1, 2)

    def run_commands(self):
        """Incepe toate schimbarile facute legate de noduri si de animatiile acestora"""

        self.MainWindow.view.engine.node_radius = self.MainWindow.spinBox_node_radius.value()
        for node in self.MainWindow.view.engine.nodes:
            node.set_radius(self.MainWindow.spinBox_node_radius.value())

        text_DFS = self.MainWindow.lineEdit_DFS.text().strip()
        text_BFS = self.MainWindow.lineEdit_BFS.text().strip()
        text_DIJKSTRA_src = self.MainWindow.lineEdit_DIJKSTRA_src.text().strip()
        text_DIJKSTRA_end = self.MainWindow.lineEdit_DIJKSTRA_end.text().strip()

        user_guess_list = None
        algorithm_for_guess = ""
        actual_path = None
        prompt_title = ""
        prompt_label = ""

        num_algos_specified = 0
        if text_DFS:
            num_algos_specified += 1
        if text_BFS:
            num_algos_specified += 1
        if text_DIJKSTRA_src and text_DIJKSTRA_end:
            num_algos_specified += 1

        if num_algos_specified == 1:
            if text_DFS:
                algorithm_for_guess = "DFS"
                prompt_title = "DFS Guess"
                prompt_label = f"Enter your DFS sequence guess for start node '{text_DFS}' (e.g., A B C):"
            elif text_BFS:
                algorithm_for_guess = "BFS"
                prompt_title = "BFS Guess"
                prompt_label = f"Enter your BFS sequence guess for start node '{text_BFS}' (e.g., A B C):"
            elif text_DIJKSTRA_src and text_DIJKSTRA_end:
                algorithm_for_guess = "DIJKSTRA"
                prompt_title = "Dijkstra Guess"
                prompt_label = f"Enter your Dijkstra path guess from '{text_DIJKSTRA_src}' to '{text_DIJKSTRA_end}' (e.g., A B C):"

            if prompt_label:  # Ensure one of the conditions was met
                dialog = StyledInputDialog(self.MainWindow, prompt_title, prompt_label)
                ok = dialog.exec_()
                text = dialog.getText()

                if ok and text:
                    user_guess_list = [node_name.strip() for node_name in text.split()]

        actual_path = self.MainWindow.view.engine.start_animations(
            text_DFS, text_BFS, text_DIJKSTRA_src, text_DIJKSTRA_end,
            algorithm_to_get_path=algorithm_for_guess
        )

        if user_guess_list is not None and actual_path is not None:
            is_correct = False
            if len(user_guess_list) == len(actual_path):
                is_correct = all(
                    str(user_node) == str(engine_node) for user_node, engine_node in zip(user_guess_list, actual_path))

            if is_correct:
                self.award_point(self.MainWindow.user_uid)
                self.MainWindow.view.engine.show_result_text("Correct!", "#00ff66")
            else:
                actual = ' '.join(actual_path)
                self.MainWindow.view.engine.show_result_text(f"The actual path was: {actual}", "#ff4444")

            # if is_correct:
            #     self.award_point(self.MainWindow.user_uid)
            #     StyledMessageBox(self.MainWindow, "Result", "You are correct!").exec_()
            # else:
            #     StyledMessageBox(self.MainWindow, "Result", f"Wrong answer. Actual path was: {' '.join(actual_path)}", is_warning=True).exec_()
        elif user_guess_list is not None and actual_path is None and algorithm_for_guess:
            StyledMessageBox(self.MainWindow, "Result", "Wrong answer or no path found by the algorithm. Engine returned no path.", is_warning=True).exec_()

    def award_point(self, user_uid):
        if not user_uid:
            print("Error: No user_uid provided to award_point.")
            return
        if not firebase_admin._apps:
            print("Error: Firebase Admin SDK not initialized. Cannot award point.")
            # Optionally, show a message to the user via QMessageBox, but be careful not to be too intrusive.
            # QMessageBox.warning(self.MainWindow, "Firebase Error", "Could not connect to update score. Please ensure you are logged in and have internet access.")
            return
        try:
            db = firestore.client()
            users_ref = db.collection("leaderboard")
            docs = users_ref.stream()

            has_points = False
            points = 0
            for doc in docs:
                if doc.id == user_uid:
                    has_points = True
                    points_dict = doc.to_dict()
                    points = points_dict['Points']

            if has_points == False:
                doc_ref = db.collection("leaderboard").document(f"{user_uid}")
                doc_ref.set({"Points": 1})
            else:
                doc_ref = db.collection("leaderboard").document(f"{user_uid}")
                doc_ref.set({"Points": points + 1})
        except Exception as e:
            print(f"An error occurred while awarding point to {user_uid}: {e}")
            # Optionally, inform the user if the score update failed.
            # QMessageBox.critical(self.MainWindow, "Score Update Failed", f"Could not save your new score due to an error: {e}")

    def run_custom_algorithm(self):
        print("Show custom algorithm dialog")
        UserAlgorithmDialog(self.MainWindow).exec_()

    def force_mode(self):
        """Schimba valoare modului de forte si sterge conexiunile dintre noduri sau le
        reseteaza in cazul in care modul de forte a fost pornit"""

        self.MainWindow.view.engine.force_mode = not self.MainWindow.view.engine.force_mode
        self.MainWindow.view.engine.remove_all_connections()

    def select_directed(self):
        """Se schimba orientarea grafului ca fiind orientat

        Butonul de graf orientat se seteaza ca fiind selectat, in timp ce
        butonul de graf neorientat se seteaza ca fiind deselectat cu ajutorul
        clasei de Styles
        """

        self.MainWindow.view.engine.directed = True
        self.MainWindow.pushButton_directed.setStyleSheet(Styles.btn_directed_undirected_non_clicked)
        self.MainWindow.pushButton_undirected.setStyleSheet(Styles.btn_directed_undirected_clicked)

    def select_undirected(self):
        """Se schimba orientarea grafului ca fiind neorientat

        Butonul de graf orientat se seteaza ca fiind deselectat, in timp ce
        butonul de graf neorientat se seteaza ca fiind selectat cu ajutorul
        clasei de Styles
        """

        self.MainWindow.view.engine.directed = False
        self.MainWindow.pushButton_undirected.setStyleSheet(Styles.btn_directed_undirected_non_clicked)
        self.MainWindow.pushButton_directed.setStyleSheet(Styles.btn_directed_undirected_clicked)

    def save_graph(self):
        """Salveaza un screenshot al grafului"""

        option = QFileDialog.Options()
        option |= QFileDialog.DontUseNativeDialog
        file = QFileDialog.getSaveFileName(self.MainWindow, 'Save File',
                                           'graph.png', 'All Files (*)', options=option)
        if file[0]:
            final_file = file[0].split('.')
            pixmap = self.MainWindow.view.grab()
            pixmap.save(file[0], final_file[1].upper(), 0)

    def change_theme(self):
        """Schimba tema grafului

        Cu ajutorul clasei Styles se aleg style-urile potrivite, iar
        mai apoi se seteaza style sheet-urile corespunzatoare fiacuri
        element care trebuie modificat.
        """

        self.dark_theme = not self.dark_theme

        if self.dark_theme:
            theme = [Styles.dark_central_widget_style, Styles.dark_frames_style, Styles.dark_graphics_view_style]
        else:
            theme = [Styles.light_central_widget_style, Styles.light_frames_style, Styles.light_graphics_view_style]

        self.MainWindow.centralwidget.setStyleSheet(theme[0])
        self.MainWindow.frame_node_data.setStyleSheet(theme[1])
        self.MainWindow.frame_change_settings.setStyleSheet(theme[1])
        self.MainWindow.frame_leaderboard.setStyleSheet(theme[1])
        self.MainWindow.frame_central_top.setStyleSheet(theme[1])
        self.MainWindow.view.setStyleSheet(theme[2])

    def DFS_clear(self):
        """Reseteaza animatiile daca acestea contin o animatie DFS"""

        if self.MainWindow.lineEdit_DFS.text() == '':
            return

        self.MainWindow.view.engine.clear_result_text()
        self.MainWindow.lineEdit_DFS.clear()
        self.reset_items_color()

    def BFS_clear(self):
        """Reseteaza animatiile daca acestea contin o animatie BFS"""

        if self.MainWindow.lineEdit_BFS.text() == '':
            return

        self.MainWindow.view.engine.clear_result_text()
        self.MainWindow.lineEdit_BFS.clear()
        self.reset_items_color()

    def DIJKSTRA_clear(self):
        """Reseteaza animatiile daca acestea contin o animatie DIJKSTRA"""

        if self.MainWindow.lineEdit_DIJKSTRA_src.text() + self.MainWindow.lineEdit_DIJKSTRA_end.text() == '':
            return

        self.MainWindow.view.engine.clear_result_text()
        self.MainWindow.lineEdit_DIJKSTRA_src.clear()
        self.MainWindow.lineEdit_DIJKSTRA_end.clear()
        self.reset_items_color()

    def reset_items_color(self):
        """Reseteaza culorile si animatiile nodurilor si muchilor inpoi la alb, respectiv la fara animatii"""

        self.MainWindow.view.engine.DFS_sequential.clear()
        self.MainWindow.view.engine.BFS_sequential.clear()
        self.MainWindow.view.engine.DIJKSTRA_sequential.clear()

        for node in self.MainWindow.view.engine.nodes:
            node.pen = QPen(Qt.white, node.thickness, Qt.SolidLine)

        for edge in self.MainWindow.view.engine.edges:
            edge.setPen(QPen(Qt.white, 1.5, Qt.SolidLine))

