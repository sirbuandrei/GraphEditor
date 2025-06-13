from PyQt5 import QtWidgets, QtCore, QtGui

from views.code_editor import PythonEditor

class CustomAlgorithmDialog(QtWidgets.QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        self.setMinimumSize(600, 500)
        self.setStyleSheet("background-color: #2c2f33;")
        self.setSizeGripEnabled(True)

        # Main layout
        main_layout = QtWidgets.QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # Title bar
        self.titleBar = QtWidgets.QFrame(self)
        self.titleBar.setFixedHeight(30)
        self.titleBar.setStyleSheet("background-color: transparent;")
        title_layout = QtWidgets.QHBoxLayout(self.titleBar)
        title_layout.setContentsMargins(0, 0, 0, 0)
        title_layout.setSpacing(0)

        # Spacer to push close button to right
        spacer = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        title_layout.addItem(spacer)

        # Close button
        self.closeButton = QtWidgets.QPushButton()
        self.closeButton.setIcon(QtGui.QIcon("icons/cil-x.png"))
        self.closeButton.setIconSize(QtCore.QSize(25, 25))
        self.closeButton.setFixedSize(25, 25)
        self.closeButton.setStyleSheet("""
            QPushButton {
                background-color: transparent;
                border: none;
                color: white;
                font: 14pt;
            }
            QPushButton:hover {
                background-color: red;
            }
        """)
        self.closeButton.clicked.connect(self.reject)
        title_layout.addWidget(self.closeButton)

        # Content frame
        content_frame = QtWidgets.QFrame(self)
        content_frame.setStyleSheet("background-color: transparent;")
        content_layout = QtWidgets.QVBoxLayout(content_frame)
        content_layout.setContentsMargins(20, 20, 20, 20)
        content_layout.setSpacing(15)

        # Function name
        self.function_name_label = QtWidgets.QLineEdit(self)
        self.function_name_label.setPlaceholderText("Enter the algorithm name")
        self.function_name_label.setStyleSheet("""
            QLineEdit {
                background-color: #36393f;
                border: 2px solid #7289da;
                border-radius: 8px;
                padding: 10px;
                color: white;
                font: 11pt "Segoe UI";
            }
        """)
        content_layout.addWidget(self.function_name_label)

        # Code input area
        self.code_edit = PythonEditor(self)
        self.code_edit.setStyleSheet("""
            QsciScintilla {
                border: 2px solid #7289da;
            }
            
            QScrollBar:vertical {
                background: #3c3c3c;
                width: 12px;
                border-radius: 6px;
                margin: 0px;
            }
            
            QScrollBar::handle:vertical {
                background: #7289da;
                border-radius: 6px;
                min-height: 30px;
                margin: 2px;
            }
            
            QScrollBar::handle:vertical:hover {
                background: #8ea1e1;
            }
            
            QScrollBar::handle:vertical:pressed {
                background: #5b6eae;
            }
            
            QScrollBar::add-line:vertical,
            QScrollBar::sub-line:vertical {
                height: 0px;
                background: none;
            }
            
            QScrollBar::add-page:vertical,
            QScrollBar::sub-page:vertical {
                background: none;
            }
            
            QScrollBar:horizontal {
                background: #3c3c3c;
                height: 12px;
                border-radius: 6px;
                margin: 0px;
            }
            
            QScrollBar::handle:horizontal {
                background: #7289da;
                border-radius: 6px;
                min-width: 30px;
                margin: 2px;
            }
            
            QScrollBar::handle:horizontal:hover {
                background: #8ea1e1;
            }
            
            QScrollBar::handle:horizontal:pressed {
                background: #5b6eae;
            }
            
            QScrollBar::add-line:horizontal,
            QScrollBar::sub-line:horizontal {
                width: 0px;
                background: none;
            }
            
            QScrollBar::add-page:horizontal,
            QScrollBar::sub-page:horizontal {
                background: none;
            }
        """)
        content_layout.addWidget(self.code_edit)

        # Button layout
        button_layout = QtWidgets.QHBoxLayout()
        button_layout.addStretch()

        self.cancel_button = QtWidgets.QPushButton("Cancel", self)
        self.cancel_button.setStyleSheet("""
            QPushButton {
                background-color: #6c757d;
                border: none;
                border-radius: 8px;
                color: white;
                font: 12pt "Segoe UI Semibold";
                padding: 10px 20px;
            }
            QPushButton:hover {
                background-color: #7c868d;
            }
        """)
        self.cancel_button.clicked.connect(self.reject)
        button_layout.addWidget(self.cancel_button)

        self.execute_button = QtWidgets.QPushButton("Execute", self)
        self.execute_button.setStyleSheet("""
            QPushButton {
                background-color: #7289da;
                border: none;
                border-radius: 8px;
                color: white;
                font: 12pt "Segoe UI Semibold";
                padding: 10px 20px;
            }
            QPushButton:hover {
                background-color: #8ea1e1;
            }
        """)
        self.execute_button.clicked.connect(self.accept)
        button_layout.addWidget(self.execute_button)

        content_layout.addLayout(button_layout)

        # Add to main layout
        main_layout.addWidget(self.titleBar)
        main_layout.addWidget(content_frame)

        # Drag support
        self.old_pos = None
        self.titleBar.mousePressEvent = self.mouse_press_event
        self.titleBar.mouseMoveEvent = self.mouse_move_event

    def get_algorithm_name(self):
        return self.function_name_label.text()

    def get_full_code(self):
        return self.code_edit.text()

    def mouse_press_event(self, event):
        if event.button() == QtCore.Qt.LeftButton:
            self.old_pos = event.globalPos()

    def mouse_move_event(self, event):
        if self.old_pos:
            delta = event.globalPos() - self.old_pos
            self.move(self.pos() + delta)
            self.old_pos = event.globalPos()

