from PyQt5 import QtCore, QtWidgets, QtGui
from PyQt5.QtCore import Qt, QEvent
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QMainWindow
from numpy import integer

from utils.styles import Styles


class MainWindow(QMainWindow):
    MINIMUM_WIDTH: int = 900
    MINIMUM_HEIGHT: int  = 600

    def __init__(self):
        super().__init__()
        self._graph_view = None
        self._config_page = None
        self._input_page = None
        self._leaderboard_page = None

        self.setup_ui()
        self.setup_button_functions()
        self.setup_initial_settings()

    def setup_initial_settings(self):
        self.setAttribute(Qt.WA_DeleteOnClose)
        self.setWindowFlag(Qt.FramelessWindowHint)
        self.frame_actions_btns.installEventFilter(self)
        self.centralwidget.setStyleSheet(Styles.dark_central_widget_style)
        self.frame_central_top.setStyleSheet(Styles.dark_frames_style)

    def setup_button_functions(self):
        self.pushButton_close.clicked.connect(lambda: self.close())
        self.pushButton_minimize.clicked.connect(lambda: self.showMinimized())
        self.pushButton_maximize.clicked.connect(self.maximize_restore)
        self.pushButton_home.clicked.connect(self.show_input_page)
        self.pushButton_leaderboard.clicked.connect(self.show_leaderboard_page)
        self.pushButton_settings.clicked.connect(self.show_settings_page)

    def set_pages(self, input_page, config_page, leaderboard_page, graph_view):
        self._leaderboard_page = leaderboard_page
        self._input_page = input_page
        self._config_page = config_page
        self._graph_view = graph_view

        self._input_page.setParent(self.page_container)
        self._config_page.setParent(self.page_container)
        self._leaderboard_page.setParent(self.page_container)

        self.page_container.addWidget(self._input_page)
        self.page_container.addWidget(self._config_page)
        self.page_container.addWidget(self._leaderboard_page)

        self._input_page.setStyleSheet(Styles.dark_frames_style)
        self._config_page.setStyleSheet(Styles.dark_frames_style)
        self._leaderboard_page.setStyleSheet(Styles.dark_frames_style)

        self._graph_view.setParent(self.frame_graph)
        self.horizontalLayout.addWidget(self._graph_view)
        self._graph_view.setStyleSheet(Styles.dark_graphics_view_style)
        self._graph_view.show()

        self._config_page.spinBox_node_radius.setValue(15)

    def show_input_page(self):
        self.page_container.setCurrentWidget(self._input_page)

    def show_leaderboard_page(self):
        self.page_container.setCurrentWidget(self._leaderboard_page)

    def show_settings_page(self):
        self.page_container.setCurrentWidget(self._config_page)

    def change_theme(self):
        self.dark_theme = not self.dark_theme

        if self.dark_theme:
            theme = [Styles.dark_central_widget_style, Styles.dark_frames_style, Styles.dark_graphics_view_style]
        else:
            theme = [Styles.light_central_widget_style, Styles.light_frames_style, Styles.light_graphics_view_style]

        self.centralwidget.setStyleSheet(theme[0])
        self.frame_central_top.setStyleSheet(theme[1])

        self._input_page.setStyleSheet(theme[1]) if self._input_page is not None else ...
        self._leaderboard_page.setStyleSheet(theme[1]) if self._input_page is not None else ...
        self._config_page.setStyleSheet(theme[1]) if self._input_page is not None else ...
        self._graph_view.setStyleSheet(theme[2]) if self._graph_view is not None else ...

    def maximize_restore(self):
        if not self.isMaximized():
            self.pushButton_maximize.setIcon(QIcon(r"icons\cil-window-restore.png"))
            self.showMaximized()
        else:
            self.pushButton_maximize.setIcon(QIcon(r"icons\cil-window-maximize.png"))
            self.showNormal()

    def eventFilter(self, obj, event):
        if obj == self.frame_actions_btns:
            if event.type() == QEvent.MouseButtonDblClick:
                self.maximize_restore()

            elif event.type() == QEvent.MouseButtonPress:
                self.drag_pos = event.pos()

            elif event.type() == QEvent.MouseMove and not self.isMaximized():
                    self.move(event.globalPos() - self.drag_pos)

        return super().eventFilter(obj, event)

    def setup_ui(self):
        self.setObjectName("Graph Editor")
        self.resize(900, 600)
        self.setMinimumSize(QtCore.QSize(self.MINIMUM_WIDTH, self.MINIMUM_HEIGHT))
        self.centralwidget = QtWidgets.QWidget(self)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.frame_actions_btns = QtWidgets.QFrame(self.centralwidget)
        self.frame_actions_btns.setMinimumSize(QtCore.QSize(0, 25))
        self.frame_actions_btns.setMaximumSize(QtCore.QSize(16777215, 25))
        self.frame_actions_btns.setStyleSheet("background-color: transparent;")
        self.frame_actions_btns.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_actions_btns.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_actions_btns.setObjectName("frame_actions_btns")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.frame_actions_btns)
        self.horizontalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        spacerItem = QtWidgets.QSpacerItem(809, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem)
        self.frame_btns = QtWidgets.QFrame(self.frame_actions_btns)
        self.frame_btns.setMinimumSize(QtCore.QSize(75, 25))
        self.frame_btns.setMaximumSize(QtCore.QSize(75, 25))
        self.frame_btns.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_btns.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_btns.setObjectName("frame_btns")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout(self.frame_btns)
        self.horizontalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_3.setSpacing(0)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.pushButton_minimize = QtWidgets.QPushButton(self.frame_btns)
        self.pushButton_minimize.setIcon(QtGui.QIcon("icons\\cil-minus.png"))
        self.pushButton_minimize.setMinimumSize(QtCore.QSize(25, 25))
        self.pushButton_minimize.setMaximumSize(QtCore.QSize(25, 25))
        self.pushButton_minimize.setStyleSheet(
            "QPushButton{\n    background-color: transparent;\n    border: none;\n}\nQPushButton::hover{\n    background-color:  rgb(55, 56, 59);\n}\nQPushButton::pressed{\n    background-color:  rgb(86, 87, 89);\n}")
        self.pushButton_minimize.setText("")
        self.pushButton_minimize.setObjectName("pushButton_minimize")
        self.horizontalLayout_3.addWidget(self.pushButton_minimize)
        self.pushButton_maximize = QtWidgets.QPushButton(self.frame_btns)
        self.pushButton_maximize.setIcon(QtGui.QIcon("icons\\cil-window-maximize.png"))
        self.pushButton_maximize.setMinimumSize(QtCore.QSize(25, 25))
        self.pushButton_maximize.setMaximumSize(QtCore.QSize(25, 25))
        self.pushButton_maximize.setStyleSheet(
            "QPushButton{\n    background-color: transparent;\n    border: none;\n}\nQPushButton::hover{\n    background-color:  rgb(55, 56, 59);\n}\nQPushButton::pressed{\n    background-color:  rgb(86, 87, 89);\n}")
        self.pushButton_maximize.setText("")
        self.pushButton_maximize.setObjectName("pushButton_maximize")
        self.horizontalLayout_3.addWidget(self.pushButton_maximize)
        self.pushButton_close = QtWidgets.QPushButton(self.frame_btns)
        self.pushButton_close.setIcon(QtGui.QIcon("icons\\cil-x.png"))
        self.pushButton_close.setMinimumSize(QtCore.QSize(25, 25))
        self.pushButton_close.setMaximumSize(QtCore.QSize(25, 25))
        self.pushButton_close.setStyleSheet(
            "QPushButton{\n    background-color: transparent;\n    border: none;\n}\nQPushButton::hover{\n    background-color: red;\n}\nQPushButton::pressed{\n    background-color: rgb(148, 52, 52);\n}")
        self.pushButton_close.setText("")
        self.pushButton_close.setObjectName("pushButton_close")
        self.horizontalLayout_3.addWidget(self.pushButton_close)
        self.horizontalLayout_2.addWidget(self.frame_btns)
        self.verticalLayout.addWidget(self.frame_actions_btns)
        self.frame_central = QtWidgets.QFrame(self.centralwidget)
        self.frame_central.setStyleSheet("background-color: transparent;")
        self.frame_central.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_central.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_central.setObjectName("frame_central")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.frame_central)
        self.verticalLayout_2.setSpacing(15)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.frame_central_top = QtWidgets.QFrame(self.frame_central)
        self.frame_central_top.setMinimumSize(QtCore.QSize(0, 50))
        self.frame_central_top.setMaximumSize(QtCore.QSize(16777215, 50))
        self.frame_central_top.setAutoFillBackground(True)
        self.frame_central_top.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_central_top.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_central_top.setObjectName("frame_central_top")
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout(self.frame_central_top)
        self.horizontalLayout_4.setContentsMargins(0, 0, -1, 0)
        self.horizontalLayout_4.setSpacing(0)
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.frame_settings = QtWidgets.QFrame(self.frame_central_top)
        self.frame_settings.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_settings.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_settings.setObjectName("frame_settings")
        self.pushButton_settings = QtWidgets.QPushButton(self.frame_settings)
        self.pushButton_settings.setGeometry(QtCore.QRect(50, 0, 50, 50))
        self.pushButton_settings.setMinimumSize(QtCore.QSize(50, 50))
        self.pushButton_settings.setMaximumSize(QtCore.QSize(50, 50))
        self.pushButton_settings.setStyleSheet(
            "QPushButton{\n    background-color: transparent;\n    border-radius: 10px;\n}\nQPushButton::hover{\n    background-color: rgb(44, 47, 51);\n}")
        self.pushButton_settings.setText("")
        self.pushButton_settings.setIcon(QtGui.QIcon("icons/cil-settings.png"))
        self.pushButton_settings.setIconSize(QtCore.QSize(35, 35))
        self.pushButton_settings.setObjectName("pushButton_settings")
        self.horizontalLayout_4.addWidget(self.frame_settings)
        self.pushButton_leaderboard = QtWidgets.QPushButton(self.frame_settings)
        self.pushButton_leaderboard.setGeometry(QtCore.QRect(100, 0, 50, 50))
        self.pushButton_leaderboard.setMinimumSize(QtCore.QSize(50, 50))
        self.pushButton_leaderboard.setMaximumSize(QtCore.QSize(50, 50))
        self.pushButton_leaderboard.setStyleSheet(
            "QPushButton{\n    background-color: transparent;\n    border-radius: 10px;\n}\nQPushButton::hover{\n    background-color: rgb(44, 47, 51);\n}")
        self.pushButton_leaderboard.setText("")
        self.pushButton_leaderboard.setIcon(QtGui.QIcon("icons/cil-leaderboard.png"))
        self.pushButton_leaderboard.setIconSize(QtCore.QSize(30, 35))
        self.pushButton_leaderboard.setObjectName("pushButton_leaderboard")

        self.pushButton_home = QtWidgets.QPushButton(self.frame_settings)
        self.pushButton_home.setGeometry(QtCore.QRect(0, 0, 50, 50))
        self.pushButton_home.setMinimumSize(QtCore.QSize(50, 50))
        self.pushButton_home.setMaximumSize(QtCore.QSize(50, 50))
        self.pushButton_home.setStyleSheet(
            "QPushButton{\n    background-color: transparent;\n    border-radius: 10px;\n}\nQPushButton::hover{\n    background-color: rgb(44, 47, 51);\n}")
        self.pushButton_home.setText("")
        self.pushButton_home.setIcon(QtGui.QIcon("icons/cil-home.png"))
        self.pushButton_home.setIconSize(QtCore.QSize(30, 30))
        self.pushButton_home.setObjectName("pushButton_home")

        # self.horizontalLayout_4.addWidget(self.frame_settings)
        self.frame_title = QtWidgets.QFrame(self.frame_central_top)
        self.frame_title.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_title.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_title.setObjectName("frame_title")
        self.horizontalLayout_6 = QtWidgets.QHBoxLayout(self.frame_title)
        self.horizontalLayout_6.setObjectName("horizontalLayout_6")
        self.label_title = QtWidgets.QLabel(self.frame_title)
        self.label_title.setMinimumSize(QtCore.QSize(50, 0))
        font = QtGui.QFont()
        font.setFamily("Happy School")
        font.setPointSize(22)
        self.label_title.setFont(font)
        self.label_title.setStyleSheet("QLabel{\n    color: white;\n}")
        self.label_title.setAlignment(QtCore.Qt.AlignCenter)
        self.label_title.setObjectName("label_title")
        self.horizontalLayout_6.addWidget(self.label_title)
        self.horizontalLayout_4.addWidget(self.frame_title)
        self.frame_mode = QtWidgets.QFrame(self.frame_central_top)
        self.frame_mode.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_mode.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_mode.setObjectName("frame_mode")
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout(self.frame_mode)
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.label_mode = QtWidgets.QLabel(self.frame_mode)
        font = QtGui.QFont()
        font.setFamily("Happy School")
        font.setPointSize(10)
        self.label_mode.setFont(font)
        self.label_mode.setStyleSheet("QLabel{\n    color: white;\n}")
        self.label_mode.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignTrailing | QtCore.Qt.AlignVCenter)
        self.label_mode.setObjectName("label_mode")
        # self.horizontalLayout_5.addWidget(self.label_mode)
        # self.pushButton_theme = AnimatedToggle((self.frame_mode), pulse_checked_color="#95a5de", checked_color="#7289da")
        # self.pushButton_theme.setMinimumSize(QtCore.QSize(55, 30))
        # self.pushButton_theme.setMaximumSize(QtCore.QSize(55, 30))
        # self.pushButton_theme.setObjectName("pushButton_theme")
        # self.horizontalLayout_5.addWidget(self.pushButton_theme)
        self.horizontalLayout_4.addWidget(self.frame_mode)
        self.verticalLayout_2.addWidget(self.frame_central_top)
        self.frame_graph = QtWidgets.QFrame(self.frame_central)
        self.frame_graph.setStyleSheet("")
        self.frame_graph.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_graph.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_graph.setObjectName("frame_graph")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.frame_graph)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setSpacing(20)
        self.horizontalLayout.setObjectName("horizontalLayout")

        self.page_container = QtWidgets.QStackedWidget(self.frame_graph)
        self.page_container.setMinimumSize(QtCore.QSize(255, 0))
        self.page_container.setMaximumSize(QtCore.QSize(255, 16777215))
        self.page_container.setObjectName("page_container")
        self.horizontalLayout_9 = QtWidgets.QHBoxLayout(self.page_container)
        self.horizontalLayout_9.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_9.setSpacing(0)
        self.horizontalLayout_9.setObjectName("horizontalLayout_9")

        self.gripper = QtWidgets.QSizeGrip(self)
        self.gripper.setMaximumSize(QtCore.QSize(20, 20))
        self.gripper.setMinimumSize(QtCore.QSize(20, 20))
        self.gripper.setObjectName("gripper")
        self.horizontalLayout.addWidget(self.page_container)
        #self.horizontalLayout.addWidget(self.view_container)
        self.verticalLayout_2.addWidget(self.frame_graph)
        self.verticalLayout.addWidget(self.frame_central)
        self.verticalLayout.addWidget(self.gripper, 0, QtCore.Qt.AlignRight | QtCore.Qt.AlignBottom)
        self.setCentralWidget(self.centralwidget)
        self.retranslateUi()
        QtCore.QMetaObject.connectSlotsByName(self)

    def retranslateUi(self):
        _translate = QtCore.QCoreApplication.translate
        self.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.label_title.setText(_translate("MainWindow", "GRAPH EDITOR"))
