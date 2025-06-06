from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtCore import pyqtSignal, QTimer
from PyQt5.QtWidgets import QWidget


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
        self.label_node_count = QtWidgets.QLabel(self)
        font = QtGui.QFont()
        font.setFamily("Happy School")
        font.setPointSize(14)
        self.label_node_count.setFont(font)
        self.label_node_count.setStyleSheet("QLabel{\n    color: white;\n}")
        self.label_node_count.setObjectName("label_node_count")
        self.verticalLayout_3.addWidget(self.label_node_count)
        self.lineEdit_node_count = QtWidgets.QLineEdit(self)
        self.lineEdit_node_count.setStyleSheet(
            'QLineEdit{\n    background-color: transparent;\n    border: none;\n    border-bottom: 2px solid white;\n    border-bottom-style: solid; \n    color:  white;\n    font: 63 14pt "Segoe UI Semibold";\n}')
        self.lineEdit_node_count.setObjectName("lineEdit_node_count")
        self.verticalLayout_3.addWidget(self.lineEdit_node_count)
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

        # self.label_node_count.setText("Node count")
        # self.label_node_data.setText("Node data")

        _translate = QtCore.QCoreApplication.translate
        self.label_node_count.setText(_translate("InputPage", "Enter node count"))
        self.label_node_data.setText(_translate("InputPage", "Enter node data"))
        #self.horizontalLayout_9.addWidget(self)

        self.textEdit_node_data.installEventFilter(self)
        self.setup_key_timer()

    def setup_key_timer(self):
        self.keyTimer = QTimer()
        self.keyTimer.setSingleShot(True)
        self.keyTimer.setInterval(800)
        self.keyTimer.timeout.connect(lambda: self.send_data.emit(self.textEdit_node_data.toPlainText()))

    def showEvent(self, event):
        super().showEvent(event)
        self.show_page.emit()

    def eventFilter(self, source: QWidget, event: QtCore.QEvent) -> bool:
        if source is self.textEdit_node_data and event.type() == QtCore.QEvent.KeyPress:
            self.keyTimer.start()

        return super(InputPage, self).eventFilter(source, event)
