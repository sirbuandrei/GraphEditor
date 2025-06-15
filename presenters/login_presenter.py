class LoginPresenter:
    def __init__(self, login_screen, user_model, on_login_success):
        self.login_screen = login_screen
        self.user_model = user_model
        self.on_login_success = on_login_success

        self.login_screen.login_attempt.connect(self.handle_login)
        self.login_screen.register_attempt.connect(self.handle_register)

    def handle_login(self, email, password):
        if not email or not password:
            self.login_screen.label_error.setStyleSheet("color: red; font: 10pt 'Segoe UI';")
            self.login_screen.label_error.setText("Please enter the password and email")
            return

        success, result = self.user_model.login(email, password)

        if success:
            self.on_login_success(result)
            self.login_screen.close()
        else:
            self.login_screen.label_error.setStyleSheet("color: red; font: 10pt 'Segoe UI';")
            self.login_screen.label_error.setText(result)

    def handle_register(self, email, password):
        if not email or not password:
            self.login_screen.label_error.setStyleSheet("color: red; font: 10pt 'Segoe UI';")
            self.login_screen.label_error.setText("Please enter the password and email")
            return

        if len(password) < 6:
            self.login_screen.label_error.setStyleSheet("color: red; font: 10pt 'Segoe UI';")
            self.login_screen.label_error.setText("Password must be at least 6 characters.")
            return

        success, error = self.user_model.register(email, password)

        if success:
            self.login_screen.label_error.setStyleSheet("color: lightgreen; font: 10pt 'Segoe UI';")
            self.login_screen.label_error.setText("Registration successful. You can now login!")
            self.login_screen.lineEdit_password.setText("")
        else:
            self.login_screen.label_error.setStyleSheet("color: red; font: 10pt 'Segoe UI';")
            self.login_screen.label_error.setText(error)