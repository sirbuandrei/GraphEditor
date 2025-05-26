from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_LoginScreen(object):
    def setupUi(self, LoginScreen):
        LoginScreen.setObjectName("LoginScreen")
        LoginScreen.resize(400, 300)
        LoginScreen.setWindowTitle("Login")

        self.centralwidget = QtWidgets.QWidget(LoginScreen)
        self.centralwidget.setObjectName("centralwidget")

        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName("verticalLayout")

        self.lineEdit_email = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_email.setObjectName("lineEdit_email")
        self.lineEdit_email.setPlaceholderText("Email")
        self.verticalLayout.addWidget(self.lineEdit_email)

        self.lineEdit_password = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_password.setObjectName("lineEdit_password")
        self.lineEdit_password.setPlaceholderText("Password")
        self.lineEdit_password.setEchoMode(QtWidgets.QLineEdit.Password)
        self.verticalLayout.addWidget(self.lineEdit_password)

        self.pushButton_login = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_login.setObjectName("pushButton_login")
        self.verticalLayout.addWidget(self.pushButton_login)

        self.label_error = QtWidgets.QLabel(self.centralwidget)
        self.label_error.setObjectName("label_error")
        self.label_error.setText("")  # Initially empty
        self.label_error.setStyleSheet("color: red") # Style for error messages
        self.verticalLayout.addWidget(self.label_error)
        
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem)

        LoginScreen.setCentralWidget(self.centralwidget)

        self.retranslateUi(LoginScreen)
        QtCore.QMetaObject.connectSlotsByName(LoginScreen)

    def retranslateUi(self, LoginScreen):
        _translate = QtCore.QCoreApplication.translate
        LoginScreen.setWindowTitle(_translate("LoginScreen", "Login"))
        self.pushButton_login.setText(_translate("LoginScreen", "Login"))
        # self.label_error text will be set dynamically

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    LoginScreen = QtWidgets.QMainWindow()
    ui = Ui_LoginScreen()
    ui.setupUi(LoginScreen)
    LoginScreen.show()
    sys.exit(app.exec_())
