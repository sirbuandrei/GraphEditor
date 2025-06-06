# class SplashScreen(QMainWindow):
#     """SpalshScreen-ul de inceput"""
#
#     def __init__(self):
#         QMainWindow.__init__(self)
#         self.login_win = LoginScreen() # Instantiating LoginScreen
#         self.ui = Ui_SplashScreen()
#         self.ui.setupUi(self)
#
#         # REMOVE TITLE BAR
#         self.setWindowFlag(Qt.FramelessWindowHint)
#         self.setAttribute(Qt.WA_TranslucentBackground)
#
#         # DROP SHADOW EFFECT
#         self.shadow = QGraphicsDropShadowEffect(self)
#         self.shadow.setBlurRadius(40)
#         self.shadow.setXOffset(0)
#         self.shadow.setYOffset(0)
#         self.shadow.setColor(QColor(0, 0, 0, 60))
#         self.ui.dropShadowFrame.setGraphicsEffect(self.shadow)
#
#         # INITIAL TEXT
#         self.ui.label_loading.setText("loading...")
#
#         # CHANGE LOADING DOTS
#         QTimer.singleShot(750, lambda: self.ui.label_loading.setText("loading."))
#         QTimer.singleShot(1500, lambda: self.ui.label_loading.setText("loading.."))
#         QTimer.singleShot(2250, lambda: self.ui.label_loading.setText("loading..."))
#         QTimer.singleShot(3000, lambda: self.ui.label_loading.setText("loading."))
#         QTimer.singleShot(3750, lambda: self.ui.label_loading.setText("loading.."))
#         QTimer.singleShot(4500, lambda: self.ui.label_loading.setText("loading..."))
#
#         # PROGRESS BAR TIMER
#         self.time = QTimer()
#         self.time.timeout.connect(self.progress)
#         self.time.start(75)
#
#         self.show()
#
#     def progress(self):
#         global counter
#
#         # UPDATE PROGRESS BAR
#         self.ui.progressBar.setValue(counter)
#
#         # STOP THE TIMER
#         if counter > 100:
#             self.time.stop()
#             self.login_win.show() # Show LoginScreen instead of MainWindow
#             self.close()
#
#         counter += 5
