from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtCore import pyqtSignal


class InputPage(QtWidgets.QFrame):
    show_page = pyqtSignal()
    send_data = pyqtSignal(str)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("InputPage")
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

        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self)
        self.verticalLayout_3.setObjectName("verticalLayout_3")

        # Node data label and text area
        self.label_node_data = QtWidgets.QLabel(self)
        font = QtGui.QFont()
        font.setFamily("Happy School")
        font.setPointSize(14)
        self.label_node_data.setFont(font)
        self.label_node_data.setStyleSheet("QLabel{\n    color: white;\n}")
        self.label_node_data.setObjectName("label_node_data")
        self.verticalLayout_3.addWidget(self.label_node_data)

        self.textEdit_node_data = QtWidgets.QTextEdit(self)
        self.textEdit_node_data.setStyleSheet(
            'QTextEdit{\n    background-color: transparent;\n    border: none;\n    border-radius: 0px;\n    border-left:2px solid white;\n    border-left-style: solid;\n    color: white;\n    font: 63 14pt "Segoe UI Semibold";\n}')
        self.textEdit_node_data.setObjectName("textEdit_node_data")
        self.verticalLayout_3.addWidget(self.textEdit_node_data)

        # Generate Graph Button
        self.pushButton_generate = QtWidgets.QPushButton(self)
        self.pushButton_generate.setMinimumSize(QtCore.QSize(0, 40))
        self.pushButton_generate.setMaximumSize(QtCore.QSize(16777215, 40))
        self.pushButton_generate.setIcon(QtGui.QIcon("icons/icons8-enter.png"))
        self.pushButton_generate.setStyleSheet("""
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
        """)
        self.pushButton_generate.clicked.connect(self.generate_graph)
        self.verticalLayout_3.addWidget(self.pushButton_generate)

        # Set labels
        _translate = QtCore.QCoreApplication.translate
        self.label_node_data.setText(_translate("InputPage", "Graph Data"))
        self.pushButton_generate.setText(_translate("InputPage", "Generate Graph"))

    def generate_graph(self):
        try:
            text = self.textEdit_node_data.toPlainText()
            self.send_data.emit(text)
        except Exception as e:
            print(f"ERROR in generate_graph: {e}")
            import traceback
            traceback.print_exc()

    # def showEvent(self, event):
    #     try:
    #         super().showEvent(event)
    #         self.show_page.emit()
    #     except RuntimeError:
    #         pass