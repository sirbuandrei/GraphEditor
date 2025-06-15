from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtCore import pyqtSignal
from qtwidgets import AnimatedToggle


class ConfigPage(QtWidgets.QFrame):
    force_mode_toggled = pyqtSignal(bool)
    radius_changed = pyqtSignal(int)
    directed = pyqtSignal()
    undirected = pyqtSignal()
    run_algorithm = pyqtSignal()
    edit_algorithm = pyqtSignal()
    create_custom_algorithm = pyqtSignal()
    save_graph = pyqtSignal()
    clear_algorithm = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()
        self.setup_button_signals()
        self.setup_initial_settings()

    def setup_initial_settings(self):
        self.spinBox_node_radius.setRange(12, 22)
        self.spinBox_node_radius.setValue(15)

    def setup_button_signals(self):
        self.pushButton_force_mode.clicked.connect(self.on_force_mode_clicked)
        self.spinBox_node_radius.valueChanged.connect(self.on_node_radius_changed)
        self.pushButton_directed.clicked.connect(self.on_directed_clicked)
        self.pushButton_undirected.clicked.connect(self.on_undirected_clicked)
        self.pushButton_run_commands.clicked.connect(self.on_run_algorithm_clicked)
        self.pushButton_user_algorithm.clicked.connect(self.on_user_algorithm_clicked)
        self.pushButton_save_graph.clicked.connect(self.on_save_graph_clicked)
        self.pushButton_clear.clicked.connect(self.on_clear_clicked)
        self.pushButton_edit_algorithm.clicked.connect(self.on_edit_algorithm_clicked)

    def on_force_mode_clicked(self):
        is_enabled = self.pushButton_force_mode.isChecked()  # If it's a toggle button
        self.force_mode_toggled.emit(is_enabled)

    def on_node_radius_changed(self):
        value = self.spinBox_node_radius.value()
        self.radius_changed.emit(value)

    def on_directed_clicked(self):
        self.directed.emit()

    def on_undirected_clicked(self):
        self.undirected.emit()

    def on_run_algorithm_clicked(self):
        self.run_algorithm.emit()

    def on_user_algorithm_clicked(self):
        self.create_custom_algorithm.emit()

    def on_save_graph_clicked(self):
        self.save_graph.emit()

    def on_clear_clicked(self):
        self.clear_algorithm.emit()

    def on_edit_algorithm_clicked(self):
        self.edit_algorithm.emit()

    def get_algorithm_type(self):
        return self.combo_box.currentText()

    def get_algorithm_input(self):
        return self.lineEdit_input.text()

    def add_custom_algorithm(self, custom_algorithm):
        self.combo_box.addItem(custom_algorithm)

    def clear_algorithm_input(self):
        self.lineEdit_input.clear()

    def setup_ui(self):
        self.setObjectName("ConfigPage")
        self.setGeometry(QtCore.QRect(250, 140, 250, 481))
        self.setMinimumSize(QtCore.QSize(250, 0))
        self.setMaximumSize(QtCore.QSize(250, 16777215))
        self.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.setFrameShadow(QtWidgets.QFrame.Raised)
        self.setStyleSheet("""
                    QFrame {
                        background-color: #63676e;
                        border-radius: 15px;
                    }
                """)

        self.verticalLayout_0 = QtWidgets.QVBoxLayout(self)
        self.verticalLayout_0.setObjectName("verticalLayout_0")
        self.verticalLayout_0.setSpacing(2)
        self.verticalLayout_0.setContentsMargins(15, 15, 15, 15)

        # Force Mode Section
        self.frame_force_mode = QtWidgets.QFrame(self)
        self.frame_force_mode.setMinimumSize(QtCore.QSize(0, 55))  # Slightly taller
        self.frame_force_mode.setMaximumSize(QtCore.QSize(16777215, 55))
        self.frame_force_mode.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_force_mode.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_force_mode.setObjectName("frame_force_mode")
        self.horizontalLayout_3_0 = QtWidgets.QHBoxLayout(self.frame_force_mode)
        self.horizontalLayout_3_0.setObjectName("horizontalLayout_3_0")
        self.horizontalLayout_3_0.setContentsMargins(10, 5, 10, 5)

        self.label_force_mode = QtWidgets.QLabel(self.frame_force_mode)
        self.label_force_mode.setMinimumSize(QtCore.QSize(0, 0))
        font = QtGui.QFont()
        font.setFamily("Happy School")
        font.setPointSize(14)
        self.label_force_mode.setFont(font)
        self.label_force_mode.setStyleSheet("QLabel{ color: white; }")
        self.label_force_mode.setAlignment(QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter)  # Left align
        self.label_force_mode.setObjectName("label_force_mode")
        self.horizontalLayout_3_0.addWidget(self.label_force_mode)

        self.pushButton_force_mode = AnimatedToggle((self.frame_force_mode), pulse_checked_color="#95a5de",
                                                    checked_color="#7289da")
        self.pushButton_force_mode.setMinimumSize(QtCore.QSize(55, 30))
        self.pushButton_force_mode.setMaximumSize(QtCore.QSize(55, 30))
        self.pushButton_force_mode.setObjectName("pushButton_force_mode")
        self.horizontalLayout_3_0.addWidget(self.pushButton_force_mode)
        self.verticalLayout_0.addWidget(self.frame_force_mode)

        # Node Radius Section
        self.frame_node_radius = QtWidgets.QFrame(self)
        self.frame_node_radius.setMinimumSize(QtCore.QSize(0, 55))  # Slightly taller
        self.frame_node_radius.setMaximumSize(QtCore.QSize(16777215, 55))
        self.frame_node_radius.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_node_radius.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_node_radius.setObjectName("frame_node_radius")

        self.horizontalLayout_4_0 = QtWidgets.QHBoxLayout(self.frame_node_radius)
        self.horizontalLayout_4_0.setObjectName("horizontalLayout_4_0")
        self.horizontalLayout_4_0.setContentsMargins(10, 5, 10, 5)

        self.label_node_radius = QtWidgets.QLabel(self.frame_node_radius)
        self.label_node_radius.setMinimumSize(QtCore.QSize(0, 0))
        font = QtGui.QFont()
        font.setFamily("Happy School")
        font.setPointSize(14)
        self.label_node_radius.setFont(font)
        self.label_node_radius.setStyleSheet("QLabel{ color: white; }")
        self.label_node_radius.setAlignment(QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter)  # Left align
        self.label_node_radius.setObjectName("label_node_radius")
        self.horizontalLayout_4_0.addWidget(self.label_node_radius)

        self.spinBox_node_radius = QtWidgets.QSpinBox(self.frame_node_radius)
        self.spinBox_node_radius.setMinimumSize(QtCore.QSize(60, 25))  # Slightly bigger
        self.spinBox_node_radius.setMaximumSize(QtCore.QSize(60, 25))
        self.spinBox_node_radius.setStyleSheet("""
            QSpinBox{ 
                background-color: transparent;
                border: none; border-bottom: 2px solid white;
                border-bottom-style: solid;
                color: white;
                font: 63 14pt "Segoe UI Semibold"; 
            }
            
            QSpinBox:hover {
                border-color: #95a5de;
            }
        """)
        self.spinBox_node_radius.setAlignment(QtCore.Qt.AlignCenter)
        self.spinBox_node_radius.setObjectName("spinBox_node_radius")
        self.horizontalLayout_4_0.addWidget(self.spinBox_node_radius)
        self.verticalLayout_0.addWidget(self.frame_node_radius)

        self.frame_algorithm = QtWidgets.QFrame(self)
        self.frame_algorithm.setMinimumSize(QtCore.QSize(0, 55))  # Slightly taller
        self.frame_algorithm.setMaximumSize(QtCore.QSize(16777215, 55))
        self.frame_algorithm.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_algorithm.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_algorithm.setObjectName("frame_node_radius")

        self.horizontalLayout_5 = QtWidgets.QHBoxLayout(self.frame_algorithm)
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.horizontalLayout_5.setContentsMargins(10, 5, 10, 5)

        # Algorithm Selection - Simplified ComboBox
        self.combo_box = QtWidgets.QComboBox(self.frame_algorithm)
        font = QtGui.QFont()
        font.setFamily("Happy School")
        font.setPointSize(12)
        self.combo_box.setFont(font)
        self.combo_box.setMinimumHeight(42)
        self.combo_box.setStyleSheet("""
            QComboBox {
                background-color: transparent; 
                border: none; 
                border-bottom: 2px solid white; 
                border-bottom-style: solid;
                color: white;
                text-align: center;
            }

            QComboBox:hover {
                border-color: #95a5de;
            }
            
            QComboBox QAbstractItemView {
                background-color: #63676e;
                border-radius: 0px;
                color: white;
                selection-background-color: #7289da;
            }
        
            QComboBox QAbstractItemView::item {
                padding: 8px 12px;
                border: none;
                border-radius: 0px;
            }

            QComboBox QAbstractItemView::item:selected {
                background-color: #7289da;
            }
        """)
        self.combo_box.setEditable(True)
        self.combo_box.lineEdit().setAlignment(QtCore.Qt.AlignCenter)
        self.combo_box.lineEdit().setFont(font)
        self.combo_box.lineEdit().setReadOnly(True)
        self.combo_box.insertItem(0, "Breadth First Search")
        self.combo_box.insertItem(1, "Depth First Search")
        self.combo_box.insertItem(2, "Shortest Path")
        self.horizontalLayout_5.addWidget(self.combo_box)

        self.pushButton_edit_algorithm = QtWidgets.QPushButton(self.frame_algorithm)
        self.pushButton_edit_algorithm.setMaximumSize(QtCore.QSize(35, 35))  # Slightly bigger
        self.pushButton_edit_algorithm.setMinimumSize(QtCore.QSize(35, 35))
        self.pushButton_edit_algorithm.setStyleSheet("""
                QPushButton{
                    background-color: transparent;
                    border-radius: 6px;
                }
                QPushButton:hover{
                    background-color: rgba(44, 47, 51, 150);
                }
            """)
        self.pushButton_edit_algorithm.setIcon(QtGui.QIcon("icons/cil-pencil.png"))
        self.pushButton_edit_algorithm.setObjectName("pushButton_clear")
        self.horizontalLayout_5.addWidget(self.pushButton_edit_algorithm)

        self.verticalLayout_0.addWidget(self.frame_algorithm)

        # Algorithm Input Section
        self.frame_algorithm_input = QtWidgets.QFrame(self)
        self.frame_algorithm_input.setMinimumSize(QtCore.QSize(0, 55))
        self.frame_algorithm_input.setMaximumSize(QtCore.QSize(16777215, 55))
        self.frame_algorithm_input.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_algorithm_input.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_algorithm_input.setObjectName("frame_algorithm_input")
        self.horizontalLayout_algorithm_input = QtWidgets.QHBoxLayout(self.frame_algorithm_input)
        self.horizontalLayout_algorithm_input.setObjectName("horizontalLayout_algorithm_input")
        self.horizontalLayout_algorithm_input.setContentsMargins(10, 5, 10, 5)

        self.label_algorithm_input = QtWidgets.QLabel(self.frame_algorithm_input)
        font = QtGui.QFont()
        font.setFamily("Happy School")
        font.setPointSize(14)
        self.label_algorithm_input.setFont(font)
        self.label_algorithm_input.setStyleSheet("QLabel{ color: white; }")
        self.label_algorithm_input.setAlignment(QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter)
        self.label_algorithm_input.setObjectName("label_algorithm_input")
        self.horizontalLayout_algorithm_input.addWidget(self.label_algorithm_input)
        self.verticalLayout_0.addWidget(self.frame_algorithm_input)

        self.lineEdit_input = QtWidgets.QLineEdit(self.frame_algorithm_input)
        self.lineEdit_input.setMinimumSize(QtCore.QSize(80, 35))  # Bigger input field
        self.lineEdit_input.setMaximumSize(QtCore.QSize(80, 35))
        self.lineEdit_input.setStyleSheet(
            'QLineEdit{ background-color: transparent; border: none; border-bottom: 2px solid white; border-bottom-style: solid; color: white; font: 63 14pt "Segoe UI Semibold"; }')
        self.lineEdit_input.setAlignment(QtCore.Qt.AlignCenter)
        self.lineEdit_input.setObjectName("lineEdit_input")
        self.horizontalLayout_algorithm_input.addWidget(self.lineEdit_input)

        self.pushButton_clear = QtWidgets.QPushButton(self.frame_algorithm_input)
        self.pushButton_clear.setMaximumSize(QtCore.QSize(35, 35))  # Slightly bigger
        self.pushButton_clear.setMinimumSize(QtCore.QSize(35, 35))
        self.pushButton_clear.setStyleSheet("""
            QPushButton{
                background-color: transparent;
                border-radius: 6px;
            }
            QPushButton:hover{
                background-color: rgba(44, 47, 51, 150);
            }
        """)
        self.pushButton_clear.setIcon(QtGui.QIcon("icons/cil-clear.png"))
        self.pushButton_clear.setObjectName("pushButton_clear")
        self.horizontalLayout_algorithm_input.addWidget(self.pushButton_clear)

        # Graph Type Selection
        self.frame_directed_undirected = QtWidgets.QFrame(self)
        self.frame_directed_undirected.setMinimumSize(QtCore.QSize(0, 45))  # Taller
        self.frame_directed_undirected.setMaximumSize(QtCore.QSize(16777215, 45))
        self.frame_directed_undirected.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_directed_undirected.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_directed_undirected.setObjectName("frame_directed_undirected")
        self.horizontalLayout_6_0 = QtWidgets.QHBoxLayout(self.frame_directed_undirected)
        self.horizontalLayout_6_0.setObjectName("horizontalLayout_6_0")
        self.horizontalLayout_6_0.setSpacing(8)
        self.horizontalLayout_6_0.setContentsMargins(10, 5, 10, 5)

        # Button style for directed/undirected
        button_style = """
            QPushButton {
                background-color: #36393f;
                border: 2px solid #7289da;
                border-radius: 8px;
                color: white;
                font-weight: bold;
                padding: 5px;
            }
            QPushButton:hover {
                background-color: #7289da;
            }
            QPushButton:pressed {
                background-color: #5b6eae;
            }
            QPushButton:checked {
                background-color: #7289da;
                border-color: #95a5de;
            }
        """

        self.pushButton_directed = QtWidgets.QPushButton(self.frame_directed_undirected)
        self.pushButton_directed.setMinimumSize(QtCore.QSize(0, 35))  # Taller buttons
        self.pushButton_directed.setMaximumSize(QtCore.QSize(16777215, 35))
        font = QtGui.QFont()
        font.setFamily("Happy School")
        font.setPointSize(13)  # Slightly smaller font
        self.pushButton_directed.setFont(font)
        self.pushButton_directed.setStyleSheet(button_style)
        self.pushButton_directed.setCheckable(True)
        self.pushButton_directed.setObjectName("pushButton_directed")
        self.horizontalLayout_6_0.addWidget(self.pushButton_directed)

        self.pushButton_undirected = QtWidgets.QPushButton(self.frame_directed_undirected)
        self.pushButton_undirected.setMinimumSize(QtCore.QSize(0, 35))
        self.pushButton_undirected.setMaximumSize(QtCore.QSize(16777215, 35))
        font = QtGui.QFont()
        font.setFamily("Happy School")
        font.setPointSize(13)
        self.pushButton_undirected.setFont(font)
        self.pushButton_undirected.setStyleSheet(button_style)
        self.pushButton_undirected.setCheckable(True)
        self.pushButton_undirected.setObjectName("pushButton_undirected")
        self.horizontalLayout_6_0.addWidget(self.pushButton_undirected)
        self.verticalLayout_0.addWidget(self.frame_directed_undirected)

        # Action Buttons - Improved styling and bigger height
        action_button_style = """
            QPushButton {
                background-color: #7289da;
                border: none;
                border-radius: 10px;
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
        """

        # Run Algorithm Button
        self.pushButton_run_commands = QtWidgets.QPushButton(self)
        self.pushButton_run_commands.setMinimumSize(QtCore.QSize(0, 40))  # Taller
        self.pushButton_run_commands.setMaximumSize(QtCore.QSize(16777215, 40))
        font = QtGui.QFont()
        font.setFamily("Happy School")
        font.setPointSize(13)
        self.pushButton_run_commands.setFont(font)
        self.pushButton_run_commands.setIcon(QtGui.QIcon("icons/cil-terminal.png"))
        self.pushButton_run_commands.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.pushButton_run_commands.setStyleSheet(action_button_style)
        self.pushButton_run_commands.setObjectName("pushButton_run_commands")
        self.verticalLayout_0.addWidget(self.pushButton_run_commands)

        # Add Custom Algorithm Button
        self.pushButton_user_algorithm = QtWidgets.QPushButton(self)
        self.pushButton_user_algorithm.setMinimumSize(QtCore.QSize(0, 40))
        self.pushButton_user_algorithm.setMaximumSize(QtCore.QSize(16777215, 40))
        font = QtGui.QFont()
        font.setFamily("Happy School")
        font.setPointSize(13)
        self.pushButton_user_algorithm.setFont(font)
        self.pushButton_user_algorithm.setIcon(QtGui.QIcon("icons/cil-plus.png"))
        self.pushButton_user_algorithm.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.pushButton_user_algorithm.setStyleSheet(action_button_style)
        self.pushButton_user_algorithm.setObjectName("pushButton_user_algorithm")
        self.verticalLayout_0.addWidget(self.pushButton_user_algorithm)

        # Save Button
        self.pushButton_save_graph = QtWidgets.QPushButton(self)
        self.pushButton_save_graph.setMinimumSize(QtCore.QSize(0, 40))
        self.pushButton_save_graph.setMaximumSize(QtCore.QSize(16777215, 40))
        font = QtGui.QFont()
        font.setFamily("Happy School")
        font.setPointSize(13)
        self.pushButton_save_graph.setFont(font)
        self.pushButton_save_graph.setIcon(QtGui.QIcon("icons/cil-save.png"))
        self.pushButton_save_graph.setText("Save")
        self.pushButton_save_graph.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.pushButton_save_graph.setStyleSheet(action_button_style)
        self.pushButton_save_graph.setObjectName("pushButton_save_graph")
        self.verticalLayout_0.addWidget(self.pushButton_save_graph)

        # Spacer
        spacerItem = QtWidgets.QSpacerItem(17, 88, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_0.addItem(spacerItem)

        # Set up translations
        _translate = QtCore.QCoreApplication.translate
        self.label_force_mode.setText(_translate("ConfigPage", "Force mode"))
        self.pushButton_force_mode.setText(_translate("ConfigPage", "PushButton"))
        self.label_node_radius.setText(_translate("ConfigPage", "Node radius"))
        self.label_algorithm_input.setText(_translate("ConfigPage", "Input:"))
        self.pushButton_directed.setText(_translate("ConfigPage", "Directed"))
        self.pushButton_undirected.setText(_translate("ConfigPage", "Undirected"))
        self.pushButton_run_commands.setText(_translate("ConfigPage", "Run Algorithm"))
        self.pushButton_user_algorithm.setText(_translate("ConfigPage", "Add Custom Algorithm"))


