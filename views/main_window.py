from PyQt5 import QtCore, QtWidgets, QtGui
from PyQt5.QtCore import Qt, QEvent
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QMainWindow
from qtwidgets import AnimatedToggle

from utils.styles import Styles


class MainWindow(QMainWindow):
    MINIMUM_WIDTH = 900
    MINIMUM_HEIGHT = 600

    def __init__(self):
        super().__init__()
        self.user_id = None
        self._graph_view = None
        self._config_page = None
        self._input_page = None
        self._leaderboard_page = None

        self.dark_theme = None

        self.setup_ui()
        self.setup_button_functions()
        self.setup_initial_settings()

    def set_user_id(self, user_id):
        self.user_id = user_id

    def setup_initial_settings(self):
        self.setAttribute(Qt.WA_DeleteOnClose)
        self.setWindowFlag(Qt.FramelessWindowHint)

        self.frame_actions_btns.installEventFilter(self)

        self.centralwidget.setStyleSheet(Styles.dark_central_widget_style)
        self.frame_central_top.setStyleSheet(Styles.dark_frames_style)
        #self.dark_theme = False
        #self.pushButton_theme.click()

    def setup_button_functions(self):
        self.pushButton_close.clicked.connect(lambda: self.close())
        self.pushButton_minimize.clicked.connect(lambda: self.showMinimized())
        self.pushButton_maximize.clicked.connect(self.maximize_restore)
        #self.pushButton_theme.clicked.connect(self.change_theme)
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
                print('Double Click')
                self.maximize_restore()

            elif event.type() == QEvent.MouseButtonPress:
                self.drag_pos = event.pos()

            elif event.type() == QEvent.MouseMove and not self.isMaximized():
                    self.move(event.globalPos() - self.drag_pos)

        return super().eventFilter(obj, event)

    def setup_ui(self):
        self.setObjectName("MainWindow")
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
        #self.page_container.setStyleSheet("background-color: white;")
        # self.page_container.setFrameShape(QtWidgets.QFrame.StyledPanel)
        # self.page_container.setFrameShadow(QtWidgets.QFrame.Raised)
        self.page_container.setObjectName("page_container")
        self.horizontalLayout_9 = QtWidgets.QHBoxLayout(self.page_container)
        self.horizontalLayout_9.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_9.setSpacing(0)
        self.horizontalLayout_9.setObjectName("horizontalLayout_9")

        # self.frame_container = QtWidgets.QFrame(self.frame_graph)
        # self.frame_container.setMinimumSize(QtCore.QSize(255, 0))
        # self.frame_container.setMaximumSize(QtCore.QSize(255, 16777215))
        # self.frame_container.setFrameShape(QtWidgets.QFrame.StyledPanel)
        # self.frame_container.setFrameShadow(QtWidgets.QFrame.Raised)
        # self.frame_container.setObjectName("frame_container")
        # self.horizontalLayout_9 = QtWidgets.QHBoxLayout(self.frame_container)
        # self.horizontalLayout_9.setContentsMargins(0, 0, 0, 0)
        # self.horizontalLayout_9.setSpacing(0)
        # self.horizontalLayout_9.setObjectName("horizontalLayout_9")


        # self.frame_change_settings = QtWidgets.QFrame(self.frame_container)
        # self.frame_change_settings.setGeometry(QtCore.QRect(250, 140, 250, 481))
        # self.frame_change_settings.setMinimumSize(QtCore.QSize(250, 0))
        # self.frame_change_settings.setMaximumSize(QtCore.QSize(250, 16777215))
        # self.frame_change_settings.setFrameShape(QtWidgets.QFrame.StyledPanel)
        # self.frame_change_settings.setFrameShadow(QtWidgets.QFrame.Raised)
        # self.frame_change_settings.setObjectName("frame_change_settings")
        # self.verticalLayout_0 = QtWidgets.QVBoxLayout(self.frame_change_settings)
        # self.verticalLayout_0.setObjectName("verticalLayout_0")

        # Create leaderboard container frame (matches frame_change_settings)
        # self.frame_leaderboard = LeaderboardPage(self.frame_container)


        # self.frame_leaderboard = QtWidgets.QFrame(self.frame_container)
        # self.frame_leaderboard.setMinimumSize(QtCore.QSize(250, 0))
        # self.frame_leaderboard.setMaximumSize(QtCore.QSize(250, 16777215))
        # self.frame_leaderboard.setStyleSheet("""
        #             QFrame {
        #                 background-color: #63676e;
        #                 border-radius: 15px;
        #             }
        #         """)
        # self.frame_leaderboard.setFrameShape(QtWidgets.QFrame.StyledPanel)
        # self.frame_leaderboard.setFrameShadow(QtWidgets.QFrame.Raised)
        #
        # # Layout inside leaderboard frame
        # self.verticalLayout_leaderboard = QtWidgets.QVBoxLayout(self.frame_leaderboard)
        # self.verticalLayout_leaderboard.setContentsMargins(10, 10, 10, 10)
        #
        # # Table widget
        # self.tableWidget_leaderboard = QtWidgets.QTableWidget(self.frame_leaderboard)
        # self.tableWidget_leaderboard.setColumnCount(2)
        # self.tableWidget_leaderboard.setHorizontalHeaderLabels(["Email", "Points"])
        # self.tableWidget_leaderboard.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        # self.tableWidget_leaderboard.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        # self.tableWidget_leaderboard.setShowGrid(False)
        #
        # # Stretch last column
        # self.tableWidget_leaderboard.horizontalHeader().setStretchLastSection(True)
        #
        # # Make table + header transparent
        # self.tableWidget_leaderboard.setStyleSheet("""
        #             QTableWidget {
        #                 background-color: transparent;
        #                 color: white;
        #                 border: none;
        #                 font: 12pt 'Segoe UI';
        #                 selection-background-color: #7289da;
        #                 selection-color: white;
        #             }
        #             QHeaderView::section {
        #                 background-color: transparent;
        #                 color: white;
        #                 padding: 6px;
        #                 border: none;
        #                 font-weight: bold;
        #             }
        #             QTableCornerButton::section {
        #                 background-color: transparent;
        #                 border: none;
        #             }
        #             QScrollBar:vertical {
        #                 background: transparent;
        #                 width: 12px;
        #                 margin: 0px;
        #             }
        #             QScrollBar::handle:vertical {
        #                 background: #7289da;
        #                 border-radius: 6px;
        #             }
        #             QScrollBar::add-line:vertical,
        #             QScrollBar::sub-line:vertical {
        #                 background: none;
        #                 height: 0px;
        #             }
        #             QScrollBar:horizontal {
        #                 background: transparent;
        #                 height: 12px;
        #                 margin: 0px;
        #             }
        #             QScrollBar::handle:horizontal {
        #                 background: #7289da;
        #                 border-radius: 6px;
        #             }
        #             QScrollBar::add-line:horizontal,
        #             QScrollBar::sub-line:horizontal {
        #                 background: none;
        #                 width: 0px;
        #             }
        #         """)
        #
        # # Add table to frame
        # self.verticalLayout_leaderboard.addWidget(self.tableWidget_leaderboard)
        #
        # # Add to layout (but keep it hidden by default)
        # self.horizontalLayout_9.addWidget(self.frame_leaderboard)
        # self.frame_leaderboard.hide()

        # self.frame_force_mode = QtWidgets.QFrame(self.frame_change_settings)
        # self.frame_force_mode.setMinimumSize(QtCore.QSize(0, 50))
        # self.frame_force_mode.setMaximumSize(QtCore.QSize(16777215, 50))
        # self.frame_force_mode.setFrameShape(QtWidgets.QFrame.StyledPanel)
        # self.frame_force_mode.setFrameShadow(QtWidgets.QFrame.Raised)
        # self.frame_force_mode.setObjectName("frame_force_mode")
        # self.horizontalLayout_3_0 = QtWidgets.QHBoxLayout(self.frame_force_mode)
        # self.horizontalLayout_3_0.setObjectName("horizontalLayout_3_0")
        # self.label_force_mode = QtWidgets.QLabel(self.frame_force_mode)
        # self.label_force_mode.setMinimumSize(QtCore.QSize(0, 0))
        # font = QtGui.QFont()
        # font.setFamily("Happy School")
        # font.setPointSize(14)
        # self.label_force_mode.setFont(font)
        # self.label_force_mode.setStyleSheet("QLabel{\n    color: white;\n}")
        # self.label_force_mode.setAlignment(QtCore.Qt.AlignCenter)
        # self.label_force_mode.setObjectName("label_force_mode")
        # self.horizontalLayout_3_0.addWidget(self.label_force_mode)
        # self.pushButton_force_mode = AnimatedToggle((self.frame_force_mode), pulse_checked_color="#95a5de",
        #                                             checked_color="#7289da")
        # self.pushButton_force_mode.setMinimumSize(QtCore.QSize(55, 30))
        # self.pushButton_force_mode.setMaximumSize(QtCore.QSize(55, 30))
        # self.pushButton_force_mode.setObjectName("pushButton_force_mode")
        # self.horizontalLayout_3_0.addWidget(self.pushButton_force_mode)
        # self.verticalLayout_0.addWidget(self.frame_force_mode)
        # self.frame_node_radius = QtWidgets.QFrame(self.frame_change_settings)
        # self.frame_node_radius.setMinimumSize(QtCore.QSize(0, 50))
        # self.frame_node_radius.setMaximumSize(QtCore.QSize(16777215, 50))
        # self.frame_node_radius.setFrameShape(QtWidgets.QFrame.StyledPanel)
        # self.frame_node_radius.setFrameShadow(QtWidgets.QFrame.Raised)
        # self.frame_node_radius.setObjectName("frame_node_radius")
        # self.horizontalLayout_4_0 = QtWidgets.QHBoxLayout(self.frame_node_radius)
        # self.horizontalLayout_4_0.setObjectName("horizontalLayout_4_0")
        # self.label_node_radius = QtWidgets.QLabel(self.frame_node_radius)
        # self.label_node_radius.setMinimumSize(QtCore.QSize(0, 0))
        # font = QtGui.QFont()
        # font.setFamily("Happy School")
        # font.setPointSize(14)
        # self.label_node_radius.setFont(font)
        # self.label_node_radius.setStyleSheet("QLabel{\n    color: white;\n}")
        # self.label_node_radius.setAlignment(QtCore.Qt.AlignCenter)
        # self.label_node_radius.setObjectName("label_node_radius")
        # self.horizontalLayout_4_0.addWidget(self.label_node_radius)
        # self.spinBox_node_radius = QtWidgets.QSpinBox(self.frame_node_radius)
        # self.spinBox_node_radius.setMinimumSize(QtCore.QSize(50, 20))
        # self.spinBox_node_radius.setMaximumSize(QtCore.QSize(50, 20))
        # self.spinBox_node_radius.setStyleSheet(
        #     'QSpinBox{\n    background-color: transparent;\n    border: none;\n    border-bottom: 2px solid white;\n    border-bottom-style: solid; \n    color:  white;\n    font: 63 14pt "Segoe UI Semibold";\n}')
        # self.spinBox_node_radius.setAlignment(QtCore.Qt.AlignCenter)
        # self.spinBox_node_radius.setObjectName("spinBox_node_radius")
        # self.horizontalLayout_4_0.addWidget(self.spinBox_node_radius)
        # self.verticalLayout_0.addWidget(self.frame_node_radius)
        # self.frame_DFS = QtWidgets.QFrame(self.frame_change_settings)
        # self.frame_DFS.setMinimumSize(QtCore.QSize(0, 50))
        # self.frame_DFS.setMaximumSize(QtCore.QSize(16777215, 50))
        # self.frame_DFS.setFrameShape(QtWidgets.QFrame.StyledPanel)
        # self.frame_DFS.setFrameShadow(QtWidgets.QFrame.Raised)
        # self.frame_DFS.setObjectName("frame_DFS")
        # self.horizontalLayout_2_0 = QtWidgets.QHBoxLayout(self.frame_DFS)
        # self.horizontalLayout_2_0.setObjectName("horizontalLayout_2_0")
        # self.label_DFS = QtWidgets.QLabel(self.frame_DFS)
        # font = QtGui.QFont()
        # font.setFamily("Happy School")
        # font.setPointSize(14)
        # self.label_DFS.setFont(font)
        # self.label_DFS.setStyleSheet("QLabel{\n    color: white;\n}")
        # self.label_DFS.setAlignment(QtCore.Qt.AlignCenter)
        # self.label_DFS.setObjectName("label_DFS")
        # self.horizontalLayout_2_0.addWidget(self.label_DFS)
        # self.lineEdit_DFS = QtWidgets.QLineEdit(self.frame_DFS)
        # self.lineEdit_DFS.setMinimumSize(QtCore.QSize(55, 30))
        # self.lineEdit_DFS.setMaximumSize(QtCore.QSize(55, 30))
        # self.lineEdit_DFS.setStyleSheet(
        #     'QLineEdit{\n    background-color: transparent;\n    border: none;\n    border-bottom: 2px solid white;\n    border-bottom-style: solid; \n    color:  white;\n    font: 63 14pt "Segoe UI Semibold";\n}')
        # self.lineEdit_DFS.setAlignment(QtCore.Qt.AlignCenter)
        # self.lineEdit_DFS.setObjectName("lineEdit_DFS")
        # self.horizontalLayout_2_0.addWidget(self.lineEdit_DFS)
        # self.pushButton_clear_DFS = QtWidgets.QPushButton(self.frame_DFS)
        # self.pushButton_clear_DFS.setMaximumSize(QtCore.QSize(30, 30))
        # self.pushButton_clear_DFS.setMinimumSize(QtCore.QSize(30, 30))
        # self.pushButton_clear_DFS.setStyleSheet("QPushButton{\nbackground-color: transparent;\nborder-radius: 5px;\n}"
        #                                         "QPushButton::hover{\nbackground-color: rgb(44, 47, 51);\n}")
        # self.pushButton_clear_DFS.setIcon(QtGui.QIcon("icons/cil-remove.png"))
        # self.pushButton_clear_DFS.setObjectName("pushButton_clear_DFS")
        # self.horizontalLayout_2_0.addWidget(self.pushButton_clear_DFS)
        # self.verticalLayout_0.addWidget(self.frame_DFS)
        # self.frame_BFS = QtWidgets.QFrame(self.frame_change_settings)
        # self.frame_BFS.setMinimumSize(QtCore.QSize(0, 50))
        # self.frame_BFS.setMaximumSize(QtCore.QSize(16777215, 50))
        # self.frame_BFS.setFrameShape(QtWidgets.QFrame.StyledPanel)
        # self.frame_BFS.setFrameShadow(QtWidgets.QFrame.Raised)
        # self.frame_BFS.setObjectName("frame_BFS")
        # self.horizontalLayout_0 = QtWidgets.QHBoxLayout(self.frame_BFS)
        # self.horizontalLayout_0.setObjectName("horizontalLayout_0")
        # self.label_BFS = QtWidgets.QLabel(self.frame_BFS)
        # font = QtGui.QFont()
        # font.setFamily("Happy School")
        # font.setPointSize(14)
        # self.label_BFS.setFont(font)
        # self.label_BFS.setStyleSheet("QLabel{\n    color: white;\n}")
        # self.label_BFS.setAlignment(QtCore.Qt.AlignCenter)
        # self.label_BFS.setObjectName("label_BFS")
        # self.horizontalLayout_0.addWidget(self.label_BFS)
        # self.lineEdit_BFS = QtWidgets.QLineEdit(self.frame_BFS)
        # self.lineEdit_BFS.setMinimumSize(QtCore.QSize(55, 30))
        # self.lineEdit_BFS.setMaximumSize(QtCore.QSize(55, 30))
        # self.lineEdit_BFS.setStyleSheet(
        #     'QLineEdit{\n    background-color: transparent;\n    border: none;\n    border-bottom: 2px solid white;\n    border-bottom-style: solid; \n    color:  white;\n    font: 63 14pt "Segoe UI Semibold";\n}')
        # self.lineEdit_BFS.setAlignment(QtCore.Qt.AlignCenter)
        # self.lineEdit_BFS.setObjectName("lineEdit_BFS")
        # self.horizontalLayout_0.addWidget(self.lineEdit_BFS)
        # self.pushButton_clear_BFS = QtWidgets.QPushButton(self.frame_BFS)
        # self.pushButton_clear_BFS.setMaximumSize(QtCore.QSize(30, 30))
        # self.pushButton_clear_BFS.setMinimumSize(QtCore.QSize(30, 30))
        # self.pushButton_clear_BFS.setStyleSheet(
        #     "QPushButton{\nbackground-color: transparent;\nborder-radius: 5px;\n                                                    }\n                                                    QPushButton::hover{\n                                                    background-color: rgb(44, 47, 51);\n}")
        # self.pushButton_clear_BFS.setIcon(QtGui.QIcon("icons/cil-remove.png"))
        # self.pushButton_clear_BFS.setObjectName("pushButton_clear_DFS")
        # self.horizontalLayout_0.addWidget(self.pushButton_clear_BFS)
        # self.verticalLayout_0.addWidget(self.frame_BFS)
        # self.frame_DIJKSTRA = QtWidgets.QFrame(self.frame_change_settings)
        # self.frame_DIJKSTRA.setMinimumSize(QtCore.QSize(0, 50))
        # self.frame_DIJKSTRA.setMaximumSize(QtCore.QSize(16777215, 50))
        # self.frame_DIJKSTRA.setFrameShape(QtWidgets.QFrame.StyledPanel)
        # self.frame_DIJKSTRA.setFrameShadow(QtWidgets.QFrame.Raised)
        # self.frame_DIJKSTRA.setObjectName("frame_DIJKSTRA")
        # self.horizontalLayout_10 = QtWidgets.QHBoxLayout(self.frame_DIJKSTRA)
        # self.horizontalLayout_10.setObjectName("horizontalLayout_10")
        # self.label_DIJKSTRA = QtWidgets.QLabel(self.frame_DIJKSTRA)
        # font = QtGui.QFont()
        # font.setFamily("Happy School")
        # font.setPointSize(14)
        # self.label_DIJKSTRA.setFont(font)
        # self.label_DIJKSTRA.setStyleSheet("QLabel{\n    color: white;\n}")
        # self.label_DIJKSTRA.setAlignment(QtCore.Qt.AlignCenter)
        # self.label_DIJKSTRA.setObjectName("label_DIJKSTRA")
        # self.horizontalLayout_10.addWidget(self.label_DIJKSTRA)
        # self.lineEdit_DIJKSTRA_src = QtWidgets.QLineEdit(self.frame_DIJKSTRA)
        # self.lineEdit_DIJKSTRA_src.setMinimumSize(QtCore.QSize(35, 30))
        # self.lineEdit_DIJKSTRA_src.setMaximumSize(QtCore.QSize(35, 30))
        # self.lineEdit_DIJKSTRA_src.setStyleSheet(
        #     'QLineEdit{\n    background-color: transparent;\n    border: none;\n    border-bottom: 2px solid white;\n    border-bottom-style: solid; \n    color:  white;\n    font: 63 14pt "Segoe UI Semibold";\n}')
        # self.lineEdit_DIJKSTRA_src.setAlignment(QtCore.Qt.AlignCenter)
        # self.lineEdit_DIJKSTRA_src.setObjectName("lineEdit_DIJKSTRA_src")
        # self.horizontalLayout_10.addWidget(self.lineEdit_DIJKSTRA_src)
        # self.lineEdit_DIJKSTRA_end = QtWidgets.QLineEdit(self.frame_DIJKSTRA)
        # self.lineEdit_DIJKSTRA_end.setMinimumSize(QtCore.QSize(35, 30))
        # self.lineEdit_DIJKSTRA_end.setMaximumSize(QtCore.QSize(35, 30))
        # self.lineEdit_DIJKSTRA_end.setStyleSheet(
        #     'QLineEdit{\n    background-color: transparent;\n    border: none;\n    border-bottom: 2px solid white;\n    border-bottom-style: solid; \n    color:  white;\n    font: 63 14pt "Segoe UI Semibold";\n}')
        # self.lineEdit_DIJKSTRA_end.setAlignment(QtCore.Qt.AlignCenter)
        # self.lineEdit_DIJKSTRA_end.setObjectName("lineEdit_DIJKSTRA_end")
        # self.horizontalLayout_10.addWidget(self.lineEdit_DIJKSTRA_end)
        # self.pushButton_clear_DIJKSTRA = QtWidgets.QPushButton(self.frame_DIJKSTRA)
        # self.pushButton_clear_DIJKSTRA.setMaximumSize(QtCore.QSize(30, 30))
        # self.pushButton_clear_DIJKSTRA.setMinimumSize(QtCore.QSize(30, 30))
        # self.pushButton_clear_DIJKSTRA.setStyleSheet("QPushButton{"
        #                                              "background-color: transparent;\nborder-radius: 5px;\n}"
        #                                              "QPushButton::hover{\nbackground-color: rgb(44, 47, 51);\n}")
        # self.pushButton_clear_DIJKSTRA.setIcon(QtGui.QIcon("icons/cil-remove.png"))
        # self.pushButton_clear_DIJKSTRA.setObjectName("pushButton_clear_DIJKSTRA")
        # self.horizontalLayout_10.addWidget(self.pushButton_clear_DIJKSTRA)
        # self.verticalLayout_0.addWidget(self.frame_DIJKSTRA)
        # self.frame_directed_undirected = QtWidgets.QFrame(self.frame_change_settings)
        # self.frame_directed_undirected.setMinimumSize(QtCore.QSize(0, 50))
        # self.frame_directed_undirected.setMaximumSize(QtCore.QSize(16777215, 50))
        # self.frame_directed_undirected.setFrameShape(QtWidgets.QFrame.StyledPanel)
        # self.frame_directed_undirected.setFrameShadow(QtWidgets.QFrame.Raised)
        # self.frame_directed_undirected.setObjectName("frame_directed_undirected")
        # self.horizontalLayout_6_0 = QtWidgets.QHBoxLayout(self.frame_directed_undirected)
        # self.horizontalLayout_6_0.setObjectName("horizontalLayout_6_0")
        # self.pushButton_directed = QtWidgets.QPushButton(self.frame_directed_undirected)
        # self.pushButton_directed.setMinimumSize(QtCore.QSize(0, 30))
        # self.pushButton_directed.setMaximumSize(QtCore.QSize(16777215, 30))
        # font = QtGui.QFont()
        # font.setFamily("Happy School")
        # font.setPointSize(14)
        # self.pushButton_directed.setFont(font)
        # self.pushButton_directed.setObjectName("pushButton_directed")
        # self.horizontalLayout_6_0.addWidget(self.pushButton_directed)
        # self.pushButton_undirected = QtWidgets.QPushButton(self.frame_directed_undirected)
        # self.pushButton_undirected.setMinimumSize(QtCore.QSize(0, 30))
        # self.pushButton_undirected.setMaximumSize(QtCore.QSize(16777215, 30))
        # font = QtGui.QFont()
        # font.setFamily("Happy School")
        # font.setPointSize(14)
        # self.pushButton_undirected.setFont(font)
        # self.pushButton_undirected.setObjectName("pushButton_undirected")
        # self.horizontalLayout_6_0.addWidget(self.pushButton_undirected)
        # self.verticalLayout_0.addWidget(self.frame_directed_undirected)
        # self.pushButton_run_commands = QtWidgets.QPushButton(self.frame_change_settings)
        # self.pushButton_run_commands.setMinimumSize(QtCore.QSize(0, 30))
        # self.pushButton_run_commands.setMaximumSize(QtCore.QSize(16777215, 30))
        # font = QtGui.QFont()
        # font.setFamily("Happy School")
        # font.setPointSize(14)
        # self.pushButton_run_commands.setFont(font)
        # self.pushButton_run_commands.setIcon(QtGui.QIcon("icons/cil-terminal.png"))
        # self.pushButton_run_commands.setLayoutDirection(QtCore.Qt.LeftToRight)
        # self.pushButton_run_commands.setStyleSheet(
        #     "QPushButton{\n    background-color: transparent;\n    border-radius: 10px;\n    color: white;\n}\nQPushButton::hover{\n    background-color: rgb(44, 47, 51);\n}QPushButton::pressed{\n    background-color: rgb(66, 69, 74);\n}")
        # self.pushButton_run_commands.setObjectName("pushButton_run_commands")
        # self.verticalLayout_0.addWidget(self.pushButton_run_commands)
        #
        # self.pushButton_user_algorithm = QtWidgets.QPushButton(self.frame_change_settings)
        # self.pushButton_user_algorithm.setMinimumSize(QtCore.QSize(0, 30))
        # self.pushButton_user_algorithm.setMaximumSize(QtCore.QSize(16777215, 30))
        # font = QtGui.QFont()
        # font.setFamily("Happy School")
        # font.setPointSize(14)
        # self.pushButton_user_algorithm.setFont(font)
        # self.pushButton_user_algorithm.setIcon(QtGui.QIcon("icons/cil-terminal.png"))  # Optional: Add an icon
        # self.pushButton_user_algorithm.setLayoutDirection(QtCore.Qt.LeftToRight)
        # self.pushButton_user_algorithm.setStyleSheet(
        #     "QPushButton{\n    background-color: transparent;\n    border-radius: 10px;\n    color: white;\n}\nQPushButton::hover{\n    background-color: rgb(44, 47, 51);\n}QPushButton::pressed{\n    background-color: rgb(66, 69, 74);\n}")
        # self.pushButton_user_algorithm.setObjectName("pushButton_user_algorithm")
        # self.verticalLayout_0.addWidget(self.pushButton_user_algorithm)
        #
        # self.pushButton_save_graph = QtWidgets.QPushButton(self.frame_change_settings)
        # self.pushButton_save_graph.setMinimumSize(QtCore.QSize(0, 30))
        # self.pushButton_save_graph.setMaximumSize(QtCore.QSize(16777215, 30))
        # font = QtGui.QFont()
        # font.setFamily("Happy School")
        # font.setPointSize(14)
        # self.pushButton_save_graph.setFont(font)
        # self.pushButton_save_graph.setIcon(QtGui.QIcon("icons/cil-save.png"))
        # self.pushButton_save_graph.setText("Save")
        # self.pushButton_save_graph.setLayoutDirection(QtCore.Qt.LeftToRight)
        # self.pushButton_save_graph.setStyleSheet(
        #     "QPushButton{\n    background-color: transparent;\n    border-radius: 10px;\n    color: white;\n}\nQPushButton::hover{\n    background-color: rgb(44, 47, 51);\n}QPushButton::pressed{\n    background-color: rgb(66, 69, 74);\n}")
        # self.pushButton_save_graph.setObjectName("pushButton_save_graph")
        # self.verticalLayout_0.addWidget(self.pushButton_save_graph)
        # spacerItem = QtWidgets.QSpacerItem(17, 88, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        # self.verticalLayout_0.addItem(spacerItem)
        # self.horizontalLayout_9.addWidget(self.frame_change_settings)
        # self.frame_node_data = QtWidgets.QFrame(self.frame_container)
        # self.frame_node_data.setMinimumSize(QtCore.QSize(250, 0))
        # self.frame_node_data.setMaximumSize(QtCore.QSize(250, 16777215))
        # self.frame_node_data.setFrameShape(QtWidgets.QFrame.StyledPanel)
        # self.frame_node_data.setFrameShadow(QtWidgets.QFrame.Raised)
        # self.frame_node_data.setObjectName("frame_node_data")
        # self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.frame_node_data)
        # self.verticalLayout_3.setObjectName("verticalLayout_3")
        # self.label_node_count = QtWidgets.QLabel(self.frame_node_data)
        # font = QtGui.QFont()
        # font.setFamily("Happy School")
        # font.setPointSize(14)
        # self.label_node_count.setFont(font)
        # self.label_node_count.setStyleSheet("QLabel{\n    color: white;\n}")
        # self.label_node_count.setObjectName("label_node_count")
        # self.verticalLayout_3.addWidget(self.label_node_count)
        # self.lineEdit_node_count = QtWidgets.QLineEdit(self.frame_node_data)
        # self.lineEdit_node_count.setStyleSheet(
        #     'QLineEdit{\n    background-color: transparent;\n    border: none;\n    border-bottom: 2px solid white;\n    border-bottom-style: solid; \n    color:  white;\n    font: 63 14pt "Segoe UI Semibold";\n}')
        # self.lineEdit_node_count.setObjectName("lineEdit_node_count")
        # self.verticalLayout_3.addWidget(self.lineEdit_node_count)
        # self.label_node_data = QtWidgets.QLabel(self.frame_node_data)
        # font = QtGui.QFont()
        # font.setFamily("Happy School")
        # font.setPointSize(14)
        # self.label_node_data.setFont(font)
        # self.label_node_data.setStyleSheet("QLabel{\n    color: white;\n}")
        # self.label_node_data.setObjectName("label_node_data")
        # self.verticalLayout_3.addWidget(self.label_node_data)
        # self.textEdit_node_data = QtWidgets.QTextEdit(self.frame_node_data)
        # self.textEdit_node_data.setStyleSheet(
        #     'QTextEdit{\n    background-color: transparent;\n    border: none;\n    border-radius: 0px;\n    border-left:2px solid white;\n    border-left-style: solid;\n    color: white;\n    font: 63 14pt "Segoe UI Semibold";\n}')
        # self.textEdit_node_data.setObjectName("textEdit_node_data")
        # self.verticalLayout_3.addWidget(self.textEdit_node_data)
        # self.horizontalLayout_9.addWidget(self.frame_node_data)
        #self.view = GraphicsView(self.frame_graph)
        #self.view.setObjectName("graphicsView")

        #self.view_container = QtWidgets.QFrame(self.frame_container)
        #self.view_container.setStyleSheet("background-color: white;")

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
        #self.label_mode.setText(_translate("MainWindow", "DARK MODE"))
