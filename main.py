"""Fisierul principal al aplicatiei

Aplicatia incepe prin a arata un splash-screen care
are o animatie de loading..., dupa terminarea animatiei
se proneste window-ul principal ce corespunde aplicatiei
efective.
"""

import sys

from PyQt5.QtCore import (Qt, QEvent, QTimer)
from PyQt5.QtWidgets import (QMainWindow, QGraphicsDropShadowEffect, QApplication)
from PyQt5.QtGui import QColor

from ui_new_main import Ui_MainWindow
from ui_splash_screen import Ui_SplashScreen
from ui_functions import Ui_Functions
from login_screen import LoginScreen

counter = 0  # PROGRESS BAR COUNTER


class MainWindow(QMainWindow, Ui_MainWindow):
    """Clasa principala a aplicatiei

    Atribute
    --------
    funtions : Ui_Functions
        funtiile window-ului
    Restul de atribute sunt mostenite
    de la clasa Ui_MainWindow

    Metode
    ------
    setup_ui_functions()
        atribuirea de functii
    setup_initial_settings()
        setarile initiale
    setup_key_timer()
        crearea unui timer
    eventFilter(obj, event)
        manipuleaza eventurile aplicatiei
    """

    def __init__(self):
        super(MainWindow, self).__init__()
        self.setupUi(self)
        self.functions = Ui_Functions(self)
        self.setup_ui_functions()
        self.setup_initial_settings()
        self.setup_key_timer()

        # Insaland un event filter se vor putea manipula mai
        # bine eventurile care provin de la aceste atribute
        self.textEdit_node_data.installEventFilter(self)
        self.frame_actions_btns.installEventFilter(self)

    def setup_ui_functions(self):
        """Atribuirea functilor specifice fiecarui buton"""

        self.pushButton_close.clicked.connect(lambda: self.close())
        self.pushButton_minimize.clicked.connect(lambda: self.showMinimized())
        self.pushButton_maximize.clicked.connect(self.functions.maximize_restore)
        self.pushButton_mode.clicked.connect(self.functions.change_theme)
        self.pushButton_settings.clicked.connect(self.functions.settings_page)
        self.pushButton_run_commands.clicked.connect(self.functions.run_commands)
        self.pushButton_save_graph.clicked.connect(self.functions.save_graph)
        self.pushButton_force_mode.clicked.connect(self.functions.force_mode)
        self.pushButton_directed.clicked.connect(self.functions.select_directed)
        self.pushButton_undirected.clicked.connect(self.functions.select_undirected)
        self.pushButton_clear_DFS.clicked.connect(self.functions.DFS_clear)
        self.pushButton_clear_BFS.clicked.connect(self.functions.BFS_clear)
        self.pushButton_clear_DIJKSTRA.clicked.connect(self.functions.DIJKSTRA_clear)

    def setup_initial_settings(self):
        """Setarile intiale ale aplicatiei"""

        self.setAttribute(Qt.WA_DeleteOnClose)
        self.setWindowFlag(Qt.FramelessWindowHint)

        self.frame_change_settings.hide()

        self.spinBox_node_radius.setRange(10, 30)
        self.spinBox_node_radius.setValue(15)

        self.pushButton_mode.click()
        self.pushButton_force_mode.click()
        self.pushButton_undirected.click()

    def setup_key_timer(self):
        """Creearea unui timer pentru taste

        Pentru a optimiza trimiterea datelor grafului catre engine, se
        implementeaza un key timer pentru a impiedica trimiterea datelor la
        fiecare tasta apasata. Datele vor fi trimise la 0.8 secude dupa oprirea
        din tastat, in cazul in care se apasa o tasta inainte de 0.8 secunde
        de la ultima apasare timer-ul se va reseta. Astfel se vor operatiile
        de manipulare a datelor grafului se vor efectua de mai putine ori.
        """

        self.keyTimer = QTimer()
        self.keyTimer.setSingleShot(True)
        self.keyTimer.setInterval(800)
        self.keyTimer.timeout.connect(self.functions.send_data)

    def eventFilter(self, obj, event):
        """Filtrarea event-urilor aplicatiei

        Event-urile importante provin de la 2 atribute : textEdit_node_data
        si frame_actions_btns.
        De la textEdit_node_data se va manipula event-ul de KeyPress, de
        fiecare data cand o tasta este apasata in interiorul textEdit_node_data
        se va reseta timer-ul pentru tastat. Alte event-uri de KeyPress nu sunt
        relevante.
        De la frame_actions_btns se vor manipula event-urile : MouseButtonDblClick,
        MouseButtonPress, MouseMove . Primul event va maximiza / micsora aplicatia
        in cazul unui dublu click pe frame-ul superior. Cel de-al doilea event tine
        minte pozitia in care se apasa frame-ul superior pentru ca mai apoi sa fie
        folosita de event-ul MouseMove puntru a muta window-ul aplicatiei, in cazul
        miscarii de mouse-ului.

        Parametrii
        ----------
        obj : QObject
            obiectul care trimite eventul
        event : QEvent
            tipul de event
        """

        if obj == self.textEdit_node_data and event.type() == QEvent.KeyPress:
            self.keyTimer.start()

        elif obj == self.frame_actions_btns:

            if event.type() == QEvent.MouseButtonDblClick:
                self.functions.maximize_restore()

            elif event.type() == QEvent.MouseButtonPress:
                self.drag_pos = event.pos()

            elif event.type() == QEvent.MouseMove:
                if not self.isMaximized():
                    self.move(event.globalPos() - self.drag_pos)
                # else:
                #     self.functions.maximize_restore()
                #     #self.move(self.drag_pos)
                #     #print(ratio)
                #     # TODO: check bug

        return super(MainWindow, self).eventFilter(obj, event)


class SplashScreen(QMainWindow):
    """SpalshScreen-ul de inceput"""

    def __init__(self):
        QMainWindow.__init__(self)
        self.login_win = LoginScreen() # Instantiating LoginScreen
        self.ui = Ui_SplashScreen()
        self.ui.setupUi(self)

        # REMOVE TITLE BAR
        self.setWindowFlag(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)

        # DROP SHADOW EFFECT
        self.shadow = QGraphicsDropShadowEffect(self)
        self.shadow.setBlurRadius(40)
        self.shadow.setXOffset(0)
        self.shadow.setYOffset(0)
        self.shadow.setColor(QColor(0, 0, 0, 60))
        self.ui.dropShadowFrame.setGraphicsEffect(self.shadow)

        # INITIAL TEXT
        self.ui.label_loading.setText("loading...")

        # CHANGE LOADING DOTS
        QTimer.singleShot(750, lambda: self.ui.label_loading.setText("loading."))
        QTimer.singleShot(1500, lambda: self.ui.label_loading.setText("loading.."))
        QTimer.singleShot(2250, lambda: self.ui.label_loading.setText("loading..."))
        QTimer.singleShot(3000, lambda: self.ui.label_loading.setText("loading."))
        QTimer.singleShot(3750, lambda: self.ui.label_loading.setText("loading.."))
        QTimer.singleShot(4500, lambda: self.ui.label_loading.setText("loading..."))

        # PROGRESS BAR TIMER
        self.time = QTimer()
        self.time.timeout.connect(self.progress)
        self.time.start(35)

        self.show()

    def progress(self):
        global counter

        # UPDATE PROGRESS BAR
        self.ui.progressBar.setValue(counter)

        # STOP THE TIMER
        if counter > 100:
            self.time.stop()
            self.login_win.show() # Show LoginScreen instead of MainWindow
            self.close()

        counter += 5


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = SplashScreen()
    sys.exit(app.exec_())
