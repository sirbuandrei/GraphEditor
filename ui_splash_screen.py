from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_SplashScreen(object):

    def setupUi(self, SplashScreen):
        SplashScreen.setObjectName("SplashScreen")
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
                                           "    background-color: rgb(56,58,89);\n"
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
                                       "    color: rgb(0, 225, 0);\n"
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
                                       "    color: rgb(200.200.200);\n"
                                       "    background-color: rgb(98, 114, 164);\n"
                                       "    border-style: none;\n"
                                       "    border-radius: 10px;\n"
                                       "    text-align: center;\n"
                                       "}\n"
                                       "QProgressBar::chunk{\n"
                                       "    border-radius: 10px;\n"
                                       "    background-color: qlineargradient(spread:pad, x1:0, y1:0.506, x2:0.960227, y2:0.54, stop:0 rgba(0, 225, 0, 255), stop:1 rgba(0, 170, 0, 255));\n"
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


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    SplashScreen = QtWidgets.QMainWindow()
    ui = Ui_SplashScreen()
    ui.setupUi(SplashScreen)
    SplashScreen.show()
    sys.exit(app.exec_())
