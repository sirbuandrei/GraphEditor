"""Fisierul contine clasa care raspunde de funtiile interfatei"""

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon, QPen
from PyQt5.QtWidgets import QFileDialog, QInputDialog, QMessageBox
from styles import Styles


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

    def settings_page(self):
        """Arata sau ascunde pagina de setari ale aplicatiei"""

        if self.MainWindow.frame_change_settings.isHidden():
            self.MainWindow.frame_node_data.hide()
            self.MainWindow.frame_change_settings.show()
        else:
            self.MainWindow.frame_change_settings.hide()
            self.MainWindow.frame_node_data.show()

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
                text, ok = QInputDialog.getText(self.MainWindow, prompt_title, prompt_label)
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
                QMessageBox.information(self.MainWindow, "Result", "You are correct!")
            else:
                QMessageBox.warning(self.MainWindow, "Result",
                                    f"Wrong answer. Actual path was: {' '.join(actual_path)}")
        elif user_guess_list is not None and actual_path is None and algorithm_for_guess:
            QMessageBox.warning(self.MainWindow, "Result",
                                f"Wrong answer or no path found by the algorithm. Engine returned no path.")

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
        self.MainWindow.frame_central_top.setStyleSheet(theme[1])
        self.MainWindow.view.setStyleSheet(theme[2])

    def DFS_clear(self):
        """Reseteaza animatiile daca acestea contin o animatie DFS"""

        if self.MainWindow.lineEdit_DFS.text() == '':
            return

        self.MainWindow.lineEdit_DFS.clear()
        self.reset_items_color()

    def BFS_clear(self):
        """Reseteaza animatiile daca acestea contin o animatie BFS"""

        if self.MainWindow.lineEdit_BFS.text() == '':
            return

        self.MainWindow.lineEdit_BFS.clear()
        self.reset_items_color()

    def DIJKSTRA_clear(self):
        """Reseteaza animatiile daca acestea contin o animatie DIJKSTRA"""

        if self.MainWindow.lineEdit_DIJKSTRA_src.text() + self.MainWindow.lineEdit_DIJKSTRA_end.text() == '':
            return

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

