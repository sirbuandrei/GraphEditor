from PyQt5 import QtWidgets, QtCore, QtGui


class UserInputDialog(QtWidgets.QDialog):
    def __init__(self, label=""):
        super().__init__()
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)

        self.setMinimumSize(400, 200)
        self.setObjectName("StyledInputDialog")

        # Main layout
        self.mainLayout = QtWidgets.QVBoxLayout(self)
        self.mainLayout.setContentsMargins(0, 0, 0, 0)
        self.mainLayout.setSpacing(0)

        # Top bar (matches frame color)
        self.titleBar = QtWidgets.QFrame(self)
        self.titleBar.setFixedHeight(25)
        self.titleBar.setStyleSheet("background-color: #2c2f33;")
        self.titleLayout = QtWidgets.QHBoxLayout(self.titleBar)
        self.titleLayout.setContentsMargins(0, 0, 0, 0)
        self.titleLayout.setSpacing(0)

        spacer = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.titleLayout.addItem(spacer)

        self.closeButton = QtWidgets.QPushButton(self.titleBar)
        self.closeButton.setIcon(QtGui.QIcon("icons/cil-x.png"))
        self.closeButton.setIconSize(QtCore.QSize(25, 25))
        self.closeButton.setFixedSize(25, 25)
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
        self.ok_button.setMaximumHeight(40)
        self.ok_button.setStyleSheet("""
            QPushButton {
                background-color: #7289da;
                border: none;
                border-radius: 8px;
                color: white;
                font: 63 12pt "Segoe UI Semibold";
                margin-top: 10px;
            }
            QPushButton:hover {
                background-color: #95a5de;
            }
            QPushButton:pressed {
                background-color: #5b6eae;
            }
        """)
        buttonLayout.addWidget(self.ok_button)

        self.cancel_button = QtWidgets.QPushButton("Cancel")
        self.cancel_button.setMaximumHeight(40)
        self.cancel_button.setStyleSheet("""
            QPushButton {
                background-color: #6c757d;
                border: none;
                border-radius: 8px;
                color: white;
                font: 63 12pt "Segoe UI Semibold";
                margin-top: 10px;
            }
            QPushButton:hover {
                background-color: #7c868d;
            }
        """)
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