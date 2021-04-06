#
from PyQt5.QtGui import QIcon


class Ui_Functions(object):

    def __init__(self, MainWindow):
        self.MainWindow = MainWindow

    def send_data(self):
        self.MainWindow.view.engine.receive_data(self.MainWindow.textEdit_node_data.toPlainText())

    def maximize_restore(self):
        if not self.MainWindow.isMaximized():
            self.MainWindow.pushButton_maximize.setIcon(QIcon(r"icons\cil-window-restore.png"))
            self.MainWindow.showMaximized()
        else:
            self.MainWindow.pushButton_maximize.setIcon(QIcon(r"icons\cil-window-maximize.png"))
            self.MainWindow.showNormal()

    def settings_page(self):
        if self.MainWindow.frame_change_settings.isHidden():
            self.MainWindow.frame_node_data.hide()
            self.MainWindow.frame_change_settings.show()
        else:
            self.MainWindow.frame_change_settings.hide()
            self.MainWindow.frame_node_data.show()

    def run_commands(self):
        self.MainWindow.view.engine.edge_ideal_length = self.MainWindow.spinBox_edge_ideal_length.value()
        self.MainWindow.view.engine.node_radius = self.MainWindow.spinBox_node_radius.value()

        text_BFS = self.MainWindow.lineEdit_BFS.text()
        self.MainWindow.view.engine.start_BFS(text_BFS)

        text_DFS = self.MainWindow.lineEdit_DFS.text()
        self.MainWindow.view.engine.start_DFS(text_DFS)

    def force_mode(self):
        self.MainWindow.view.engine.force_mode = not self.MainWindow.view.engine.force_mode

    def select_directed(self):
        self.MainWindow.view.engine.directed = True
        self.MainWindow.pushButton_directed.setStyleSheet("border: 2px solid white;\n"
                                                          "border-radius: 15px;")
        self.MainWindow.pushButton_undirected.setStyleSheet("QPushButton{\n"
                                                            "    background-color: transparent;\n"
                                                            "    border-radius: 10px;\n"
                                                            "    color: white;\n"
                                                            "}\n"
                                                            "QPushButton::hover{\n"
                                                            "    background-color: rgb(44, 47, 51);\n"
                                                            "}")

    def select_undirected(self):
        self.MainWindow.view.engine.directed = False
        self.MainWindow.pushButton_undirected.setStyleSheet("border: 2px solid white;\n"
                                                            "border-radius: 15px;")
        self.MainWindow.pushButton_directed.setStyleSheet("QPushButton{\n"
                                                          "    background-color: transparent;\n"
                                                          "    border-radius: 10px;\n"
                                                          "    color: white;\n"
                                                          "}\n"
                                                          "QPushButton::hover{\n"
                                                          "    background-color: rgb(44, 47, 51);\n"
                                                          "}")

    def change_theme(self):

        pass
