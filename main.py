#
import sys

from PyQt5.QtCore import Qt, QEvent, QTimer
from PyQt5.QtWidgets import QMainWindow, QGraphicsDropShadowEffect, QApplication
from PyQt5.QtGui import QColor, QIcon

from ui_new_main import Ui_MainWindow
from ui_splash_screen import Ui_SplashScreen
from ui_functions import Ui_Functions

counter = 0  # PROGRESS BAR COUNTER


class MainWindow(QMainWindow, Ui_MainWindow):

    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.setAttribute(Qt.WA_DeleteOnClose)
        self.setWindowFlag(Qt.FramelessWindowHint)
        self.setupUi(self)
        self.functions = Ui_Functions(self)
        self.setup_ui_functions()
        self.setup_initial_settings()
        self.setup_key_timer()
        self.textEdit_node_data.installEventFilter(self)
        self.frame_actions_btns.installEventFilter(self)

    def setup_ui_functions(self):
        self.pushButton_close.clicked.connect(lambda: self.close())
        self.pushButton_minimize.clicked.connect(lambda: self.showMinimized())
        self.pushButton_maximize.clicked.connect(self.functions.maximize_restore)
        self.pushButton_mode.clicked.connect(self.functions.change_theme)
        self.pushButton_settings.clicked.connect(self.functions.settings_page)
        self.pushButton_run_commands.clicked.connect(self.functions.run_commands)
        self.pushButton_force_mode.clicked.connect(self.functions.force_mode)
        self.pushButton_directed.clicked.connect(self.functions.select_directed)
        self.pushButton_undirected.clicked.connect(self.functions.select_undirected)

    def setup_initial_settings(self):
        self.frame_change_settings.hide()

        self.spinBox_edge_ideal_length.setRange(10, 300)
        self.spinBox_edge_ideal_length.setValue(150)

        self.spinBox_node_radius.setRange(20, 50)
        self.spinBox_node_radius.setValue(30)

        self.pushButton_mode.click()
        self.pushButton_force_mode.click()
        self.pushButton_undirected.click()

    def setup_key_timer(self):
        self.keyTimer = QTimer()
        self.keyTimer.setSingleShot(True)
        self.keyTimer.setInterval(800)
        self.keyTimer.timeout.connect(self.functions.send_data)

    def eventFilter(self, _object, _event):
        if _object == self.textEdit_node_data and _event.type() == QEvent.KeyPress:
            self.keyTimer.start()

        elif _object == self.frame_actions_btns:
            if _event.type() == QEvent.MouseButtonDblClick:
                self.functions.maximize_restore()
            elif _event.type() == QEvent.MouseButtonPress:
                self.drag_pos = _event.pos()
            elif _event.type() == QEvent.MouseMove:
                if not self.isMaximized():
                    self.move(_event.globalPos() - self.drag_pos)
                else:
                    self.functions.maximize_restore()
                    #self.move(_event.globalPos() - self.mapFromGlobal(self.drag_pos))
                    # TODO: check bug

        return super(MainWindow, self).eventFilter(_object, _event)


class SplashScreen(QMainWindow):

    def __init__(self):
        QMainWindow.__init__(self)
        self.main_win = MainWindow()
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

        # SHOW
        self.show()

    def progress(self):
        global counter
        # UPDATE PROGRESS BAR
        self.ui.progressBar.setValue(counter)

        if counter > 100:
            # STOP TIMER
            self.time.stop()

            # SHOW MAIN WINDOW
            self.main_win.show()

            # CLOSE SPLASH SCREEN
            self.close()

        counter += 5


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = SplashScreen()
    sys.exit(app.exec_())
