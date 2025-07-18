from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QColor
from PyQt5.QtWidgets import QGraphicsDropShadowEffect, QMainWindow

counter = 0

class SplashScreen(QMainWindow):
    def __init__(self, on_finished):
        QMainWindow.__init__(self)
        self.on_finished = on_finished
        self.setupUi(self)

        # REMOVE TITLE BAR
        self.setWindowFlag(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)

        # DROP SHADOW EFFECT
        self.shadow = QGraphicsDropShadowEffect(self)
        self.shadow.setBlurRadius(40)
        self.shadow.setXOffset(0)
        self.shadow.setYOffset(0)
        self.shadow.setColor(QColor(0, 0, 0, 60))
        self.dropShadowFrame.setGraphicsEffect(self.shadow)

        # INITIAL TEXT
        self.label_loading.setText("loading...")

        # CHANGE LOADING DOTS
        QTimer.singleShot(750, lambda: self.label_loading.setText("loading."))
        QTimer.singleShot(1500, lambda: self.label_loading.setText("loading.."))
        QTimer.singleShot(2250, lambda: self.label_loading.setText("loading..."))
        QTimer.singleShot(3000, lambda: self.label_loading.setText("loading."))
        QTimer.singleShot(3750, lambda: self.label_loading.setText("loading.."))
        QTimer.singleShot(4500, lambda: self.label_loading.setText("loading..."))

        # PROGRESS BAR TIMER
        self.time = QTimer()
        self.time.timeout.connect(self.progress)
        self.time.start(75)

    def progress(self):
        global counter

        # UPDATE PROGRESS BAR
        self.progressBar.setValue(counter)

        # STOP THE TIMER
        if counter > 100:
            self.time.stop()
            self.on_finished()
            self.close()

        counter += 5

    def setupUi(self, SplashScreen):
        SplashScreen.setObjectName("Graph Editor")
        SplashScreen.resize(550, 350)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(68)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(SplashScreen.sizePolicy().hasHeightForWidth())
        SplashScreen.setSizePolicy(sizePolicy)
        SplashScreen.setMinimumSize(QtCore.QSize(550, 350))
        SplashScreen.setMaximumSize(QtCore.QSize(550, 350))
        self.centralwidget = QtWidgets.QWidget(SplashScreen)
        self.centralwidget.setObjectName("centralwidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.centralwidget)
        self.horizontalLayout.setContentsMargins(10, 10, 10, 10)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.dropShadowFrame = QtWidgets.QFrame(self.centralwidget)
        self.dropShadowFrame.setStyleSheet("QFrame{\n"
                                           "    background-color: #1e2124;\n"
                                           "    border-radius: 15px;\n"
                                           "}")
        self.dropShadowFrame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.dropShadowFrame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.dropShadowFrame.setObjectName("dropShadowFrame")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.dropShadowFrame)
        self.verticalLayout.setObjectName("verticalLayout")
        spacerItem = QtWidgets.QSpacerItem(20, 66, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem)
        self.label_title = QtWidgets.QLabel(self.dropShadowFrame)
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(36)
        self.label_title.setFont(font)
        self.label_title.setStyleSheet("QLabel{\n"
                                       "    color: #63676e;\n"
                                       "}")
        self.label_title.setAlignment(QtCore.Qt.AlignCenter)
        self.label_title.setObjectName("label_title")
        self.verticalLayout.addWidget(self.label_title)
        self.label_description = QtWidgets.QLabel(self.dropShadowFrame)
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(12)
        self.label_description.setFont(font)
        self.label_description.setStyleSheet("QLabel{\n"
                                             "    color: rgb(98, 114, 164);\n"
                                             "}")
        self.label_description.setAlignment(QtCore.Qt.AlignCenter)
        self.label_description.setObjectName("label_description")
        self.verticalLayout.addWidget(self.label_description)
        spacerItem1 = QtWidgets.QSpacerItem(20, 65, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem1)
        self.progressBar = QtWidgets.QProgressBar(self.dropShadowFrame)
        self.progressBar.setStyleSheet("QProgressBar{\n"
                                       "    color: #63676e;\n"
                                       "    background-color: rgb(98, 114, 164);\n"
                                       "    border-style: none;\n"
                                       "    border-radius: 10px;\n"
                                       "    text-align: center;\n"
                                       "}\n"
                                       "QProgressBar::chunk{\n"
                                       "    border-radius: 10px;\n"
                                       "    background-color: qlineargradient(spread:pad, x1:0, y1:0.506, x2:0.960227, y2:0.54, stop:0 rgba(99, 103, 110, 255), stop:1 rgba(103, 115, 135, 255));\n"
                                       "}")
        self.progressBar.setProperty("value", 24)
        self.progressBar.setObjectName("progressBar")
        self.verticalLayout.addWidget(self.progressBar)
        self.label_loading = QtWidgets.QLabel(self.dropShadowFrame)
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(8)
        self.label_loading.setFont(font)
        self.label_loading.setStyleSheet("QLabel{\n"
                                         "    color: rgb(98, 114, 164);\n"
                                         "}")
        self.label_loading.setAlignment(QtCore.Qt.AlignCenter)
        self.label_loading.setObjectName("label_loading")
        self.verticalLayout.addWidget(self.label_loading)
        spacerItem2 = QtWidgets.QSpacerItem(20, 66, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem2)
        self.horizontalLayout.addWidget(self.dropShadowFrame)
        SplashScreen.setCentralWidget(self.centralwidget)

        self.retranslateUi(SplashScreen)
        QtCore.QMetaObject.connectSlotsByName(SplashScreen)

    def retranslateUi(self, SplashScreen):
        _translate = QtCore.QCoreApplication.translate
        SplashScreen.setWindowTitle(_translate("SplashScreen", "MainWindow"))
        self.label_title.setText(_translate("SplashScreen", "<strong>GRAPH</strong> EDITOR"))
        self.label_description.setText(_translate("SplashScreen", "<strong>DESIGN </strong> YOUR GRAPHS"))
        self.label_loading.setText(_translate("SplashScreen", "loading..."))


