from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QMainWindow


class LoginScreen(QMainWindow):
    login_attempt = pyqtSignal(str, str)
    register_attempt = pyqtSignal(str, str)

    def __init__(self):
        super().__init__()
        self.setup_ui()
        self.pushButton_login.clicked.connect(self._on_login_clicked)
        self.pushButton_register.clicked.connect(self._on_register_clicked)
        self.show()
    
    def setup_ui(self):
        self.setObjectName("self")
        self.resize(400, 300)
        self.setMinimumSize(QtCore.QSize(400, 300))

        # Frameless dark window
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)

        self.centralwidget = QtWidgets.QWidget(self)
        self.centralwidget.setObjectName("centralwidget")
        self.centralwidget.setStyleSheet("background-color: #1e2124;")

        self.verticalLayout_main = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout_main.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_main.setSpacing(0)

        # Custom Title Bar
        self.frame_actions_btns = QtWidgets.QFrame(self.centralwidget)
        self.frame_actions_btns.setMinimumSize(QtCore.QSize(0, 25))
        self.frame_actions_btns.setMaximumSize(QtCore.QSize(16777215, 25))
        self.frame_actions_btns.setStyleSheet("background-color: transparent;")
        self.frame_actions_btns.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_actions_btns.setFrameShadow(QtWidgets.QFrame.Raised)

        self.horizontalLayout_actions = QtWidgets.QHBoxLayout(self.frame_actions_btns)
        self.horizontalLayout_actions.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_actions.setSpacing(0)

        spacer = QtWidgets.QSpacerItem(10, 10, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_actions.addItem(spacer)

        self.frame_btns = QtWidgets.QFrame(self.frame_actions_btns)
        self.frame_btns.setMinimumSize(QtCore.QSize(75, 25))
        self.frame_btns.setMaximumSize(QtCore.QSize(75, 25))
        self.frame_btns.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_btns.setFrameShadow(QtWidgets.QFrame.Raised)
        self.horizontalLayout_btns = QtWidgets.QHBoxLayout(self.frame_btns)
        self.horizontalLayout_btns.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_btns.setSpacing(0)

        self.pushButton_minimize = QtWidgets.QPushButton(self.frame_btns)
        self.pushButton_minimize.setIcon(QtGui.QIcon("icons/cil-minus.png"))
        self.pushButton_minimize.setMinimumSize(QtCore.QSize(25, 25))
        self.pushButton_minimize.setMaximumSize(QtCore.QSize(25, 25))
        self.pushButton_minimize.setStyleSheet("""
            QPushButton { background-color: transparent; border: none; }
            QPushButton:hover { background-color: rgb(55, 56, 59); }
            QPushButton:pressed { background-color: rgb(86, 87, 89); }
        """)
        self.horizontalLayout_btns.addWidget(self.pushButton_minimize)

        self.pushButton_maximize = QtWidgets.QPushButton(self.frame_btns)
        self.pushButton_maximize.setIcon(QtGui.QIcon("icons/cil-window-maximize.png"))
        self.pushButton_maximize.setMinimumSize(QtCore.QSize(25, 25))
        self.pushButton_maximize.setMaximumSize(QtCore.QSize(25, 25))
        self.pushButton_maximize.setStyleSheet("""
            QPushButton { background-color: transparent; border: none; }
            QPushButton:hover { background-color: rgb(55, 56, 59); }
            QPushButton:pressed { background-color: rgb(86, 87, 89); }
        """)
        self.horizontalLayout_btns.addWidget(self.pushButton_maximize)

        self.pushButton_close = QtWidgets.QPushButton(self.frame_btns)
        self.pushButton_close.setIcon(QtGui.QIcon("icons/cil-x.png"))
        self.pushButton_close.setMinimumSize(QtCore.QSize(25, 25))
        self.pushButton_close.setMaximumSize(QtCore.QSize(25, 25))
        self.pushButton_close.setStyleSheet("""
            QPushButton { background-color: transparent; border: none; }
            QPushButton:hover { background-color: red; }
            QPushButton:pressed { background-color: rgb(148, 52, 52); }
        """)
        self.horizontalLayout_btns.addWidget(self.pushButton_close)

        self.horizontalLayout_actions.addWidget(self.frame_btns)
        self.verticalLayout_main.addWidget(self.frame_actions_btns)

        # Login Form Frame (light grey container)
        self.dropShadowFrame = QtWidgets.QFrame(self.centralwidget)
        self.dropShadowFrame.setStyleSheet("""
            QFrame {
                background-color: #63676e;
                border-radius: 15px;
            }
        """)
        self.dropShadowFrame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.dropShadowFrame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.dropShadowFrame.setMinimumSize(QtCore.QSize(280, 250))
        self.dropShadowFrame.setMaximumSize(QtCore.QSize(400, 350))
        self.dropShadowFrame.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)

        self.verticalLayout = QtWidgets.QVBoxLayout(self.dropShadowFrame)
        self.verticalLayout.setSpacing(10)
        self.verticalLayout.setContentsMargins(30, 30, 30, 30)

        self.lineEdit_email = QtWidgets.QLineEdit(self.dropShadowFrame)
        self.lineEdit_email.setPlaceholderText("Email")
        self.lineEdit_email.setStyleSheet("""
            QLineEdit {
                background-color: transparent;
                border: none;
                border-bottom: 2px solid white;
                color: white;
                font: 63 14pt "Segoe UI Semibold";
            }
        """)
        self.verticalLayout.addWidget(self.lineEdit_email)

        self.lineEdit_password = QtWidgets.QLineEdit(self.dropShadowFrame)
        self.lineEdit_password.setPlaceholderText("Password")
        self.lineEdit_password.setEchoMode(QtWidgets.QLineEdit.Password)
        self.lineEdit_password.setStyleSheet("""
            QLineEdit {
                background-color: transparent;
                border: none;
                border-bottom: 2px solid white;
                color: white;
                font: 63 14pt "Segoe UI Semibold";
            }
        """)
        self.verticalLayout.addWidget(self.lineEdit_password)

        # Login Button
        self.pushButton_login = QtWidgets.QPushButton(self.dropShadowFrame)
        self.pushButton_login.setText("Login")
        self.pushButton_login.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.pushButton_login.setIcon(QtGui.QIcon("icons/cil-login.png"))
        self.pushButton_login.setIconSize(QtCore.QSize(20, 20))
        self.pushButton_login.setStyleSheet("""
            QPushButton {
                background-color: transparent;
                border-radius: 10px;
                color: white;
                font: 63 14pt "Segoe UI Semibold";
            }
            QPushButton:hover {
                background-color: rgb(44, 47, 51);
            }
            QPushButton:pressed {
                background-color: rgb(66, 69, 74);
            }
        """)
        self.verticalLayout.addWidget(self.pushButton_login)

        # Register Button
        self.pushButton_register = QtWidgets.QPushButton(self.dropShadowFrame)
        self.pushButton_register.setText("Register")
        self.pushButton_register.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.pushButton_register.setIcon(QtGui.QIcon("icons/cil-register.png"))
        self.pushButton_register.setIconSize(QtCore.QSize(20, 20))
        self.pushButton_register.setStyleSheet("""
            QPushButton {
                background-color: transparent;
                border-radius: 10px;
                color: white;
                font: 63 14pt "Segoe UI Semibold";
            }
            QPushButton:hover {
                background-color: rgb(44, 47, 51);
            }
            QPushButton:pressed {
                background-color: rgb(66, 69, 74);
            }
        """)
        self.verticalLayout.addWidget(self.pushButton_register)

        self.label_error = QtWidgets.QLabel(self.dropShadowFrame)
        self.label_error.setText("")
        self.label_error.setStyleSheet("color: red; font: 10pt 'Segoe UI';")
        self.label_error.setAlignment(QtCore.Qt.AlignCenter)
        self.verticalLayout.addWidget(self.label_error)

        self.label_icons = QtWidgets.QLabel(self.dropShadowFrame)
        self.label_icons.setAlignment(QtCore.Qt.AlignCenter)
        #self.label_icons.setStyleSheet("color: white; font: 10pt 'Segoe UI';")
        self.label_icons.setText('<span style="color:white; font: 10pt \'Segoe UI\';">'
                                'Icons by <a href="https://icons8.com" style="color:white; text-decoration: underline;">Icons8</a>'
                                '</span>')
        self.label_icons.setOpenExternalLinks(True)
        self.verticalLayout.addWidget(self.label_icons)

        # Center the login frame in both directions
        self.wrapper_layout = QtWidgets.QVBoxLayout()
        self.wrapper_layout.setContentsMargins(0, 0, 0, 0)
        self.wrapper_layout.setSpacing(0)

        spacer_top = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        spacer_bottom = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.wrapper_layout.addItem(spacer_top)

        horizontal_wrapper = QtWidgets.QHBoxLayout()
        horizontal_wrapper.setContentsMargins(0, 0, 0, 0)
        horizontal_wrapper.setSpacing(0)
        spacer_left = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        spacer_right = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        horizontal_wrapper.addItem(spacer_left)
        horizontal_wrapper.addWidget(self.dropShadowFrame, stretch=1)
        horizontal_wrapper.addItem(spacer_right)

        self.wrapper_layout.addLayout(horizontal_wrapper)
        self.wrapper_layout.addItem(spacer_bottom)

        self.verticalLayout_main.addLayout(self.wrapper_layout)
        self.setCentralWidget(self.centralwidget)

        self.retranslateUi()
        QtCore.QMetaObject.connectSlotsByName(self)

        # Button behaviors
        self.pushButton_close.clicked.connect(self.close)
        self.pushButton_minimize.clicked.connect(self.showMinimized)
        self.pushButton_maximize.clicked.connect(self.toggle_max_restore)

        self.is_maximized = False
        self.self = self

        self.old_pos = None
        self.frame_actions_btns.mousePressEvent = self.mouse_press_event
        self.frame_actions_btns.mouseMoveEvent = self.mouse_move_event

    def _on_login_clicked(self):
        email = self.lineEdit_email.text()
        password = self.lineEdit_password.text()
        self.login_attempt.emit(email, password)

    def _on_register_clicked(self):
        email = self.lineEdit_email.text()
        password = self.lineEdit_password.text()
        self.register_attempt.emit(email, password)

    def toggle_max_restore(self):
        if self.is_maximized:
            self.self.showNormal()
            self.is_maximized = False
        else:
            self.self.showMaximized()
            self.is_maximized = True

    def mouse_press_event(self, event):
        if event.button() == QtCore.Qt.LeftButton:
            self.old_pos = event.globalPos()

    def mouse_move_event(self, event):
        if self.old_pos:
            delta = event.globalPos() - self.old_pos
            self.self.move(self.self.pos() + delta)
            self.old_pos = event.globalPos()

    def retranslateUi(self):
        _translate = QtCore.QCoreApplication.translate
        self.setWindowTitle(_translate("self", "Login"))