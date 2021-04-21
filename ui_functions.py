#
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon, QPen
from PyQt5.QtWidgets import QFileDialog
from styles import Styles


class Ui_Functions(object):

    def __init__(self, MainWindow):
        self.MainWindow = MainWindow
        self.dark_theme = False

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
        self.MainWindow.view.engine.node_radius = self.MainWindow.spinBox_node_radius.value()

        text_BFS = self.MainWindow.lineEdit_BFS.text()
        text_DFS = self.MainWindow.lineEdit_DFS.text()
        self.MainWindow.view.engine.start_animations(text_DFS, text_BFS)

    def force_mode(self):
        self.MainWindow.view.engine.force_mode = not self.MainWindow.view.engine.force_mode
        self.MainWindow.view.engine.remove_all_connections()

    def select_directed(self):
        self.MainWindow.view.engine.directed = True
        self.MainWindow.pushButton_directed.setStyleSheet(Styles.btn_directed_undirected_non_clicked)
        self.MainWindow.pushButton_undirected.setStyleSheet(Styles.btn_directed_undirected_clicked)

    def select_undirected(self):
        self.MainWindow.view.engine.directed = False
        self.MainWindow.pushButton_undirected.setStyleSheet(Styles.btn_directed_undirected_non_clicked)
        self.MainWindow.pushButton_directed.setStyleSheet(Styles.btn_directed_undirected_clicked)

    def save_graph(self):
        option = QFileDialog.Options()
        option |= QFileDialog.DontUseNativeDialog
        file = QFileDialog.getSaveFileName(self.MainWindow, 'Save File',
                                           'graph.png', 'All Files (*)', options=option)
        if file[0]:
            final_file = file[0].split('.')
            pixmap = self.MainWindow.view.grab()
            pixmap.save(file[0], final_file[1].upper(), 0)

    def change_theme(self):
        self.dark_theme = not self.dark_theme

        if self.dark_theme:
            theme = [Styles.dark_central_widget_style, Styles.dark_frames_style, Styles.dark_graphics_view_style]
        else:
            theme = [Styles.light_central_widget_style, Styles.light_frames_style, Styles.light_graphics_view_style]

        self.MainWindow.centralwidget.setStyleSheet(theme[0])
        self.MainWindow.frame_node_data.setStyleSheet(theme[1])
        self.MainWindow.frame_change_settings.setStyleSheet(theme[1])
        self.MainWindow.frame_central_top.setStyleSheet(theme[1])
        self.MainWindow.view.setStyleSheet(theme[2])

    def DFS_clear(self):
        if self.MainWindow.lineEdit_DFS.text() == '':
            return
        self.MainWindow.lineEdit_DFS.clear()
        self.reset_items_color()

    def BFS_clear(self):
        if self.MainWindow.lineEdit_BFS.text() == '':
            return
        self.MainWindow.lineEdit_BFS.clear()
        self.reset_items_color()

    def reset_items_color(self):
        self.MainWindow.view.engine.DFS_sequential.clear()
        self.MainWindow.view.engine.BFS_sequential.clear()

        for node in self.MainWindow.view.engine.nodes:
            node.pen = QPen(Qt.white, node.thickness, Qt.SolidLine)

        for edge in self.MainWindow.view.engine.edges:
            edge.setPen(QPen(Qt.white, 1.5, Qt.SolidLine))

