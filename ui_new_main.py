#
from PyQt5 import QtCore, QtGui, QtWidgets
from qtwidgets import AnimatedToggle
from view import GraphicsView
import source


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(900, 600)
        MainWindow.setMinimumSize(QtCore.QSize(900, 600))
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        #self.centralwidget.setStyleSheet('background-color: rgb(35, 39, 42);')
        #self.centralwidget.setAutoFillBackground(True)
        #self.centralwidget.setPalette(self.dark_palette_main)
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.frame_actions_btns = QtWidgets.QFrame(self.centralwidget)
        self.frame_actions_btns.setMinimumSize(QtCore.QSize(0, 25))
        self.frame_actions_btns.setMaximumSize(QtCore.QSize(16777215, 25))
        self.frame_actions_btns.setStyleSheet("background-color: transparent;")
        self.frame_actions_btns.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_actions_btns.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_actions_btns.setObjectName("frame_actions_btns")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.frame_actions_btns)
        self.horizontalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        spacerItem = QtWidgets.QSpacerItem(809, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem)
        self.frame_btns = QtWidgets.QFrame(self.frame_actions_btns)
        self.frame_btns.setMinimumSize(QtCore.QSize(75, 25))
        self.frame_btns.setMaximumSize(QtCore.QSize(75, 25))
        # self.frame_btns.setStyleSheet("")
        self.frame_btns.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_btns.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_btns.setObjectName("frame_btns")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout(self.frame_btns)
        self.horizontalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_3.setSpacing(0)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.pushButton_minimize = QtWidgets.QPushButton(self.frame_btns)
        self.pushButton_minimize.setIcon(QtGui.QIcon(r"icons\cil-minus.png"))
        self.pushButton_minimize.setMinimumSize(QtCore.QSize(25, 25))
        self.pushButton_minimize.setMaximumSize(QtCore.QSize(25, 25))
        self.pushButton_minimize.setStyleSheet("QPushButton{\n"
                                      "    background-color: transparent;\n"
                                      "    border: none;\n"
                                      "}\n"
                                      "QPushButton::hover{\n"
                                      "    background-color:  rgb(55, 56, 59);\n"
                                      "}\n"
                                      "QPushButton::pressed{\n"
                                      "    background-color:  rgb(86, 87, 89);\n"
                                      "}")
        self.pushButton_minimize.setText("")
        self.pushButton_minimize.setObjectName("pushButton_minimize")
        self.horizontalLayout_3.addWidget(self.pushButton_minimize)
        self.pushButton_maximize = QtWidgets.QPushButton(self.frame_btns)
        self.pushButton_maximize.setIcon(QtGui.QIcon(r'icons\cil-window-maximize.png'))
        self.pushButton_maximize.setMinimumSize(QtCore.QSize(24, 24))
        self.pushButton_maximize.setMaximumSize(QtCore.QSize(24, 24))
        self.pushButton_maximize.setStyleSheet("QPushButton{\n"
                                               "    background-color: transparent;\n"
                                               "    border: none;\n"
                                               "}\n"
                                               "QPushButton::hover{\n"
                                               "    background-color:  rgb(55, 56, 59);\n"
                                               "}\n"
                                               "QPushButton::pressed{\n"
                                               "    background-color:  rgb(86, 87, 89);\n"
                                               "}")
        self.pushButton_maximize.setText("")
        self.pushButton_maximize.setObjectName("pushButton_maximize")
        self.horizontalLayout_3.addWidget(self.pushButton_maximize)
        self.pushButton_close = QtWidgets.QPushButton(self.frame_btns)
        self.pushButton_close.setIcon(QtGui.QIcon(r'icons\cil-x.png'))
        self.pushButton_close.setMinimumSize(QtCore.QSize(25, 25))
        self.pushButton_close.setMaximumSize(QtCore.QSize(25, 25))
        self.pushButton_close.setStyleSheet("QPushButton{\n"
                                            "    background-color: transparent;\n"
                                            "    border: none;\n"
                                            "}\n"
                                            "QPushButton::hover{\n"
                                            "    background-color: red;\n"
                                            "}\n"
                                            "QPushButton::pressed{\n"
                                            "    background-color: rgb(148, 52, 52);\n"
                                            "}")
        self.pushButton_close.setText("")
        self.pushButton_close.setObjectName("pushButton_close")
        self.horizontalLayout_3.addWidget(self.pushButton_close)
        self.horizontalLayout_2.addWidget(self.frame_btns)
        self.verticalLayout.addWidget(self.frame_actions_btns)
        self.frame_central = QtWidgets.QFrame(self.centralwidget)
        self.frame_central.setStyleSheet("background-color: transparent;")
        self.frame_central.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_central.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_central.setObjectName("frame_central")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.frame_central)
        self.verticalLayout_2.setSpacing(15)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.frame_central_top = QtWidgets.QFrame(self.frame_central)
        self.frame_central_top.setMinimumSize(QtCore.QSize(0, 50))
        self.frame_central_top.setMaximumSize(QtCore.QSize(16777215, 50))
        self.frame_central_top.setAutoFillBackground(True)
        # self.frame_central_top.setStyleSheet("QFrame{\n"
        #                                      "    background-color: rgb(99, 103, 110);\n"
        #                                      "    border-radius: 10px;\n"
        #                                      "}")
        self.frame_central_top.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_central_top.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_central_top.setObjectName("frame_central_top")
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout(self.frame_central_top)
        self.horizontalLayout_4.setContentsMargins(0, 0, -1, 0)
        self.horizontalLayout_4.setSpacing(0)
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.frame_settings = QtWidgets.QFrame(self.frame_central_top)
        # self.frame_settings.setStyleSheet("QFrame{\n"
        #                                   "    background-color: rgb(99, 103, 110);\n"
        #                                   "    border-radius: 20px;\n"
        #                                   "}")
        self.frame_settings.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_settings.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_settings.setObjectName("frame_settings")

        self.pushButton_settings = QtWidgets.QPushButton(self.frame_settings)
        self.pushButton_settings.setGeometry(QtCore.QRect(0, 0, 50, 50))
        self.pushButton_settings.setMinimumSize(QtCore.QSize(50, 50))
        self.pushButton_settings.setMaximumSize(QtCore.QSize(50, 50))
        self.pushButton_settings.setStyleSheet("QPushButton{\n"
                                        "    background-color: transparent;\n"
                                        "    border-radius: 10px;\n"
                                        "    image: url(:/icons/icons/cil-settings.png);\n"
                                        "}\n"
                                        "QPushButton::hover{\n"
                                        "    background-color: rgb(44, 47, 51);\n"
                                        "}")
        self.pushButton_settings.setText("")
        self.pushButton_settings.setObjectName("pushButton_settings")
        self.horizontalLayout_4.addWidget(self.frame_settings)
        self.frame_title = QtWidgets.QFrame(self.frame_central_top)
        # self.frame_title.setStyleSheet("QFrame{\n"
        #                                "    background-color: rgb(99, 103, 110);\n"
        #                                "}")
        self.frame_title.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_title.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_title.setObjectName("frame_title")
        self.horizontalLayout_6 = QtWidgets.QHBoxLayout(self.frame_title)
        self.horizontalLayout_6.setObjectName("horizontalLayout_6")
        self.label_title = QtWidgets.QLabel(self.frame_title)
        self.label_title.setMinimumSize(QtCore.QSize(50, 0))
        font = QtGui.QFont()
        font.setFamily("Happy School")
        font.setPointSize(22)
        self.label_title.setFont(font)
        self.label_title.setStyleSheet("QLabel{\n"
                                       "    color: white;\n"
                                       "}")
        self.label_title.setAlignment(QtCore.Qt.AlignCenter)
        self.label_title.setObjectName("label_title")
        self.horizontalLayout_6.addWidget(self.label_title)
        self.horizontalLayout_4.addWidget(self.frame_title)
        self.frame_mode = QtWidgets.QFrame(self.frame_central_top)
        # self.frame_mode.setStyleSheet("QFrame{\n"
        #                               "    background-color: rgb(99, 103, 110);\n"
        #                               "}")
        self.frame_mode.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_mode.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_mode.setObjectName("frame_mode")
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout(self.frame_mode)
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.label_mode = QtWidgets.QLabel(self.frame_mode)
        font = QtGui.QFont()
        font.setFamily("Happy School")
        font.setPointSize(10)
        self.label_mode.setFont(font)
        self.label_mode.setStyleSheet("QLabel{\n"
                                      "    color: white;\n"
                                      "}")
        self.label_mode.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignTrailing | QtCore.Qt.AlignVCenter)
        self.label_mode.setObjectName("label_mode")
        self.horizontalLayout_5.addWidget(self.label_mode)

        self.pushButton_mode = AnimatedToggle(self.frame_mode, pulse_checked_color='#95a5de', checked_color='#7289da')
        self.pushButton_mode.setMinimumSize(QtCore.QSize(55, 30))
        self.pushButton_mode.setMaximumSize(QtCore.QSize(55, 30))
        self.pushButton_mode.setObjectName("pushButton_mode")
        self.horizontalLayout_5.addWidget(self.pushButton_mode)

        self.horizontalLayout_4.addWidget(self.frame_mode)
        self.verticalLayout_2.addWidget(self.frame_central_top)
        self.frame_graph = QtWidgets.QFrame(self.frame_central)
        self.frame_graph.setStyleSheet("")
        self.frame_graph.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_graph.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_graph.setObjectName("frame_graph")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.frame_graph)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setSpacing(20)
        self.horizontalLayout.setObjectName("horizontalLayout")

        self.frame_container = QtWidgets.QFrame(self.frame_graph)
        self.frame_container.setMinimumSize(QtCore.QSize(255, 0))
        self.frame_container.setMaximumSize(QtCore.QSize(255, 16777215))
        self.frame_container.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_container.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_container.setObjectName("frame_container")
        self.horizontalLayout_9 = QtWidgets.QHBoxLayout(self.frame_container)
        self.horizontalLayout_9.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_9.setSpacing(0)
        self.horizontalLayout_9.setObjectName("horizontalLayout_9")

        self.frame_change_settings = QtWidgets.QFrame(self.frame_container)
        self.frame_change_settings.setGeometry(QtCore.QRect(250, 140, 250, 481))
        self.frame_change_settings.setMinimumSize(QtCore.QSize(250, 0))
        self.frame_change_settings.setMaximumSize(QtCore.QSize(250, 16777215))
        # self.frame_change_settings.setStyleSheet("QFrame{\n"
        #                                          "    background-color: rgb(99, 103, 110);\n"
        #                                          "    border-radius: 15px;\n"
        #                                          "}")
        self.frame_change_settings.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_change_settings.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_change_settings.setObjectName("frame_change_settings")
        self.verticalLayout_0 = QtWidgets.QVBoxLayout(self.frame_change_settings)
        self.verticalLayout_0.setObjectName("verticalLayout_0")
        self.frame_force_mode = QtWidgets.QFrame(self.frame_change_settings)
        self.frame_force_mode.setMinimumSize(QtCore.QSize(0, 50))
        self.frame_force_mode.setMaximumSize(QtCore.QSize(16777215, 50))
        self.frame_force_mode.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_force_mode.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_force_mode.setObjectName("frame_force_mode")
        self.horizontalLayout_3_0 = QtWidgets.QHBoxLayout(self.frame_force_mode)
        self.horizontalLayout_3_0.setObjectName("horizontalLayout_3_0")
        self.label_force_mode = QtWidgets.QLabel(self.frame_force_mode)
        self.label_force_mode.setMinimumSize(QtCore.QSize(0, 0))
        font = QtGui.QFont()
        font.setFamily("Happy School")
        font.setPointSize(14)
        self.label_force_mode.setFont(font)
        self.label_force_mode.setStyleSheet("QLabel{\n"
                                            "    color: white;\n"
                                            "}")
        self.label_force_mode.setAlignment(QtCore.Qt.AlignCenter)
        self.label_force_mode.setObjectName("label_force_mode")
        self.horizontalLayout_3_0.addWidget(self.label_force_mode)
        self.pushButton_force_mode = AnimatedToggle(self.frame_force_mode, pulse_checked_color='#95a5de', checked_color='#7289da')
        self.pushButton_force_mode.setMinimumSize(QtCore.QSize(55, 30))
        self.pushButton_force_mode.setMaximumSize(QtCore.QSize(55, 30))
        self.pushButton_force_mode.setObjectName("pushButton_force_mode")
        self.horizontalLayout_3_0.addWidget(self.pushButton_force_mode)
        self.verticalLayout_0.addWidget(self.frame_force_mode)
        # self.frame_edge_indeal_length = QtWidgets.QFrame(self.frame_change_settings)
        # self.frame_edge_indeal_length.setMinimumSize(QtCore.QSize(0, 50))
        # self.frame_edge_indeal_length.setMaximumSize(QtCore.QSize(16777215, 50))
        # self.frame_edge_indeal_length.setFrameShape(QtWidgets.QFrame.StyledPanel)
        # self.frame_edge_indeal_length.setFrameShadow(QtWidgets.QFrame.Raised)
        # self.frame_edge_indeal_length.setObjectName("frame_edge_indeal_length")
        # self.horizontalLayout_5_0 = QtWidgets.QHBoxLayout(self.frame_edge_indeal_length)
        # self.horizontalLayout_5_0.setContentsMargins(0, 0, 0, 0)
        # self.horizontalLayout_5_0.setSpacing(6)
        # self.horizontalLayout_5_0.setObjectName("horizontalLayout_5_0")
        # self.label_force_mode_edge_ideal_length = QtWidgets.QLabel(self.frame_edge_indeal_length)
        # self.label_force_mode_edge_ideal_length.setMinimumSize(QtCore.QSize(0, 0))
        # font = QtGui.QFont()
        # font.setFamily("Happy School")
        # font.setPointSize(14)
        # self.label_force_mode_edge_ideal_length.setFont(font)
        # self.label_force_mode_edge_ideal_length.setStyleSheet("QLabel{\n"
        #                                                       "    color: white;\n"
        #                                                       "}")
        # self.label_force_mode_edge_ideal_length.setAlignment(QtCore.Qt.AlignCenter)
        # self.label_force_mode_edge_ideal_length.setObjectName("label_force_mode_edge_ideal_length")
        # self.horizontalLayout_5_0.addWidget(self.label_force_mode_edge_ideal_length)
        # self.spinBox_edge_ideal_length = QtWidgets.QSpinBox(self.frame_edge_indeal_length)
        # self.spinBox_edge_ideal_length.setMinimumSize(QtCore.QSize(50, 20))
        # self.spinBox_edge_ideal_length.setMaximumSize(QtCore.QSize(50, 20))
        # self.spinBox_edge_ideal_length.setStyleSheet("QSpinBox{\n"
        #                                              "    background-color: transparent;\n"
        #                                              "    border: none;\n"
        #                                              "    border-bottom: 2px solid white;\n"
        #                                              "    border-bottom-style: solid; \n"
        #                                              "    color:  white;\n"
        #                                              "    font: 63 14pt \"Segoe UI Semibold\";\n"
        #                                              "}")
        # self.spinBox_edge_ideal_length.setAlignment(QtCore.Qt.AlignCenter)
        # self.spinBox_edge_ideal_length.setObjectName("spinBox_edge_ideal_length")
        # self.horizontalLayout_5_0.addWidget(self.spinBox_edge_ideal_length)
        # self.verticalLayout_0.addWidget(self.frame_edge_indeal_length)
        self.frame_node_radius = QtWidgets.QFrame(self.frame_change_settings)
        self.frame_node_radius.setMinimumSize(QtCore.QSize(0, 50))
        self.frame_node_radius.setMaximumSize(QtCore.QSize(16777215, 50))
        self.frame_node_radius.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_node_radius.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_node_radius.setObjectName("frame_node_radius")
        self.horizontalLayout_4_0 = QtWidgets.QHBoxLayout(self.frame_node_radius)
        self.horizontalLayout_4_0.setObjectName("horizontalLayout_4_0")
        self.label_node_radius = QtWidgets.QLabel(self.frame_node_radius)
        self.label_node_radius.setMinimumSize(QtCore.QSize(0, 0))
        font = QtGui.QFont()
        font.setFamily("Happy School")
        font.setPointSize(14)
        self.label_node_radius.setFont(font)
        self.label_node_radius.setStyleSheet("QLabel{\n"
                                             "    color: white;\n"
                                             "}")
        self.label_node_radius.setAlignment(QtCore.Qt.AlignCenter)
        self.label_node_radius.setObjectName("label_node_radius")
        self.horizontalLayout_4_0.addWidget(self.label_node_radius)
        self.spinBox_node_radius = QtWidgets.QSpinBox(self.frame_node_radius)
        self.spinBox_node_radius.setMinimumSize(QtCore.QSize(50, 20))
        self.spinBox_node_radius.setMaximumSize(QtCore.QSize(50, 20))
        self.spinBox_node_radius.setStyleSheet("QSpinBox{\n"
                                               "    background-color: transparent;\n"
                                               "    border: none;\n"
                                               "    border-bottom: 2px solid white;\n"
                                               "    border-bottom-style: solid; \n"
                                               "    color:  white;\n"
                                               "    font: 63 14pt \"Segoe UI Semibold\";\n"
                                               "}")
        self.spinBox_node_radius.setAlignment(QtCore.Qt.AlignCenter)
        self.spinBox_node_radius.setObjectName("spinBox_node_radius")
        self.horizontalLayout_4_0.addWidget(self.spinBox_node_radius)
        self.verticalLayout_0.addWidget(self.frame_node_radius)
        self.frame_DFS = QtWidgets.QFrame(self.frame_change_settings)
        self.frame_DFS.setMinimumSize(QtCore.QSize(0, 50))
        self.frame_DFS.setMaximumSize(QtCore.QSize(16777215, 50))
        self.frame_DFS.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_DFS.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_DFS.setObjectName("frame_DFS")
        self.horizontalLayout_2_0 = QtWidgets.QHBoxLayout(self.frame_DFS)
        self.horizontalLayout_2_0.setObjectName("horizontalLayout_2_0")
        self.label_DFS = QtWidgets.QLabel(self.frame_DFS)
        font = QtGui.QFont()
        font.setFamily("Happy School")
        font.setPointSize(14)
        self.label_DFS.setFont(font)
        self.label_DFS.setStyleSheet("QLabel{\n"
                                     "    color: white;\n"
                                     "}")
        self.label_DFS.setAlignment(QtCore.Qt.AlignCenter)
        self.label_DFS.setObjectName("label_DFS")
        self.horizontalLayout_2_0.addWidget(self.label_DFS)

        self.lineEdit_DFS = QtWidgets.QLineEdit(self.frame_DFS)
        self.lineEdit_DFS.setMinimumSize(QtCore.QSize(55, 30))
        self.lineEdit_DFS.setMaximumSize(QtCore.QSize(55, 30))
        self.lineEdit_DFS.setStyleSheet("QLineEdit{\n"
                                        "    background-color: transparent;\n"
                                        "    border: none;\n"
                                        "    border-bottom: 2px solid white;\n"
                                        "    border-bottom-style: solid; \n"
                                        "    color:  white;\n"
                                        "    font: 63 14pt \"Segoe UI Semibold\";\n"
                                        "}")
        self.lineEdit_DFS.setAlignment(QtCore.Qt.AlignCenter)
        self.lineEdit_DFS.setObjectName("lineEdit_DFS")
        self.horizontalLayout_2_0.addWidget(self.lineEdit_DFS)

        self.pushButton_clear_DFS = QtWidgets.QPushButton(self.frame_DFS)
        self.pushButton_clear_DFS.setMaximumSize(QtCore.QSize(30, 30))
        self.pushButton_clear_DFS.setMinimumSize(QtCore.QSize(30, 30))
        self.pushButton_clear_DFS.setStyleSheet("""QPushButton{
                                                    background-color: transparent;
                                                    border-radius: 5px;
                                                    }
                                                    QPushButton::hover{
                                                    background-color: rgb(44, 47, 51);
                                                    }""")
        self.pushButton_clear_DFS.setIcon(QtGui.QIcon(r"icons/cil-remove.png"))
        self.pushButton_clear_DFS.setObjectName("pushButton_clear_DFS")
        self.horizontalLayout_2_0.addWidget(self.pushButton_clear_DFS)

        self.verticalLayout_0.addWidget(self.frame_DFS)
        self.frame_BFS = QtWidgets.QFrame(self.frame_change_settings)
        self.frame_BFS.setMinimumSize(QtCore.QSize(0, 50))
        self.frame_BFS.setMaximumSize(QtCore.QSize(16777215, 50))
        self.frame_BFS.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_BFS.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_BFS.setObjectName("frame_BFS")
        self.horizontalLayout_0 = QtWidgets.QHBoxLayout(self.frame_BFS)
        self.horizontalLayout_0.setObjectName("horizontalLayout_0")
        self.label_BFS = QtWidgets.QLabel(self.frame_BFS)
        font = QtGui.QFont()
        font.setFamily("Happy School")
        font.setPointSize(14)
        self.label_BFS.setFont(font)
        self.label_BFS.setStyleSheet("QLabel{\n"
                                     "    color: white;\n"
                                     "}")
        self.label_BFS.setAlignment(QtCore.Qt.AlignCenter)
        self.label_BFS.setObjectName("label_BFS")
        self.horizontalLayout_0.addWidget(self.label_BFS)
        self.lineEdit_BFS = QtWidgets.QLineEdit(self.frame_BFS)
        self.lineEdit_BFS.setMinimumSize(QtCore.QSize(55, 30))
        self.lineEdit_BFS.setMaximumSize(QtCore.QSize(55, 30))
        self.lineEdit_BFS.setStyleSheet("QLineEdit{\n"
                                        "    background-color: transparent;\n"
                                        "    border: none;\n"
                                        "    border-bottom: 2px solid white;\n"
                                        "    border-bottom-style: solid; \n"
                                        "    color:  white;\n"
                                        "    font: 63 14pt \"Segoe UI Semibold\";\n"
                                        "}")
        self.lineEdit_BFS.setAlignment(QtCore.Qt.AlignCenter)
        self.lineEdit_BFS.setObjectName("lineEdit_BFS")
        self.horizontalLayout_0.addWidget(self.lineEdit_BFS)

        self.pushButton_clear_BFS = QtWidgets.QPushButton(self.frame_BFS)
        self.pushButton_clear_BFS.setMaximumSize(QtCore.QSize(30, 30))
        self.pushButton_clear_BFS.setMinimumSize(QtCore.QSize(30, 30))
        self.pushButton_clear_BFS.setStyleSheet("""QPushButton{
                                                    background-color: transparent;
                                                    border-radius: 5px;
                                                    }
                                                    QPushButton::hover{
                                                    background-color: rgb(44, 47, 51);
                                                    }""")
        self.pushButton_clear_BFS.setIcon(QtGui.QIcon(r"icons/cil-remove.png"))
        self.pushButton_clear_BFS.setObjectName("pushButton_clear_DFS")
        self.horizontalLayout_0.addWidget(self.pushButton_clear_BFS)

        self.verticalLayout_0.addWidget(self.frame_BFS)
        self.frame_directed_undirected = QtWidgets.QFrame(self.frame_change_settings)
        self.frame_directed_undirected.setMinimumSize(QtCore.QSize(0, 50))
        self.frame_directed_undirected.setMaximumSize(QtCore.QSize(16777215, 50))
        self.frame_directed_undirected.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_directed_undirected.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_directed_undirected.setObjectName("frame_directed_undirected")
        self.horizontalLayout_6_0 = QtWidgets.QHBoxLayout(self.frame_directed_undirected)
        self.horizontalLayout_6_0.setObjectName("horizontalLayout_6_0")
        self.pushButton_directed = QtWidgets.QPushButton(self.frame_directed_undirected)
        self.pushButton_directed.setMinimumSize(QtCore.QSize(0, 30))
        self.pushButton_directed.setMaximumSize(QtCore.QSize(16777215, 30))
        font = QtGui.QFont()
        font.setFamily("Happy School")
        font.setPointSize(14)
        self.pushButton_directed.setFont(font)
        self.pushButton_directed.setObjectName("pushButton_directed")
        self.horizontalLayout_6_0.addWidget(self.pushButton_directed)
        self.pushButton_undirected = QtWidgets.QPushButton(self.frame_directed_undirected)
        self.pushButton_undirected.setMinimumSize(QtCore.QSize(0, 30))
        self.pushButton_undirected.setMaximumSize(QtCore.QSize(16777215, 30))
        font = QtGui.QFont()
        font.setFamily("Happy School")
        font.setPointSize(14)
        self.pushButton_undirected.setFont(font)
        self.pushButton_undirected.setObjectName("pushButton_undirected")
        self.horizontalLayout_6_0.addWidget(self.pushButton_undirected)
        self.verticalLayout_0.addWidget(self.frame_directed_undirected)
        self.pushButton_run_commands = QtWidgets.QPushButton(self.frame_change_settings)
        self.pushButton_run_commands.setMinimumSize(QtCore.QSize(0, 30))
        self.pushButton_run_commands.setMaximumSize(QtCore.QSize(16777215, 30))
        font = QtGui.QFont()
        font.setFamily("Happy School")
        font.setPointSize(14)
        self.pushButton_run_commands.setFont(font)
        self.pushButton_run_commands.setIcon(QtGui.QIcon(r'icons/cil-terminal.png'))
        self.pushButton_run_commands.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.pushButton_run_commands.setStyleSheet("QPushButton{\n"
                                                   "    background-color: transparent;\n"
                                                   "    border-radius: 10px;\n"
                                                   "    color: white;\n"   
                                                   "}\n"
                                                   "QPushButton::hover{\n"
                                                   "    background-color: rgb(44, 47, 51);\n"
                                                   "}"
                                                   "QPushButton::pressed{\n"
                                                   "    background-color: rgb(66, 69, 74);\n"
                                                   "}")
        self.pushButton_run_commands.setObjectName("pushButton_run_commands")
        self.verticalLayout_0.addWidget(self.pushButton_run_commands)

        self.pushButton_save_graph = QtWidgets.QPushButton(self.frame_change_settings)
        self.pushButton_save_graph.setMinimumSize(QtCore.QSize(0, 30))
        self.pushButton_save_graph.setMaximumSize(QtCore.QSize(16777215, 30))
        font = QtGui.QFont()
        font.setFamily("Happy School")
        font.setPointSize(14)
        self.pushButton_save_graph.setFont(font)
        self.pushButton_save_graph.setIcon(QtGui.QIcon(r'icons/cil-save.png'))
        self.pushButton_save_graph.setText('Save')
        self.pushButton_save_graph.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.pushButton_save_graph.setStyleSheet("QPushButton{\n"
                                                   "    background-color: transparent;\n"
                                                   "    border-radius: 10px;\n"
                                                   "    color: white;\n"
                                                   "}\n"
                                                   "QPushButton::hover{\n"
                                                   "    background-color: rgb(44, 47, 51);\n"
                                                   "}"
                                                   "QPushButton::pressed{\n"
                                                   "    background-color: rgb(66, 69, 74);\n"
                                                   "}")
        self.pushButton_save_graph.setObjectName("pushButton_save_graph")
        self.verticalLayout_0.addWidget(self.pushButton_save_graph)

        spacerItem = QtWidgets.QSpacerItem(17, 88, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_0.addItem(spacerItem)
        self.horizontalLayout_9.addWidget(self.frame_change_settings)

        self.frame_node_data = QtWidgets.QFrame(self.frame_container)
        self.frame_node_data.setMinimumSize(QtCore.QSize(250, 0))
        self.frame_node_data.setMaximumSize(QtCore.QSize(250, 16777215))
        # self.frame_node_data.setStyleSheet("QFrame{\n"
        #                                    "    background-color: rgb(99, 103, 110);\n"
        #                                    "    border-radius: 15px;\n"
        #                                    "}")
        self.frame_node_data.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_node_data.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_node_data.setObjectName("frame_node_data")

        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.frame_node_data)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.label_node_count = QtWidgets.QLabel(self.frame_node_data)
        font = QtGui.QFont()
        font.setFamily("Happy School")
        font.setPointSize(14)
        self.label_node_count.setFont(font)
        self.label_node_count.setStyleSheet("QLabel{\n"
                                            "    color: white;\n"
                                            "}")
        self.label_node_count.setObjectName("label_node_count")
        self.verticalLayout_3.addWidget(self.label_node_count)
        self.lineEdit_node_count = QtWidgets.QLineEdit(self.frame_node_data)
        self.lineEdit_node_count.setStyleSheet("QLineEdit{\n"
                                               "    background-color: transparent;\n"
                                               "    border: none;\n"
                                               "    border-bottom: 2px solid white;\n"
                                               "    border-bottom-style: solid; \n"
                                               "    color:  white;\n"
                                               "    font: 63 14pt \"Segoe UI Semibold\";\n"
                                               "}")
        self.lineEdit_node_count.setObjectName("lineEdit_node_count")
        self.verticalLayout_3.addWidget(self.lineEdit_node_count)
        self.label_node_data = QtWidgets.QLabel(self.frame_node_data)
        font = QtGui.QFont()
        font.setFamily("Happy School")
        font.setPointSize(14)
        self.label_node_data.setFont(font)
        self.label_node_data.setStyleSheet("QLabel{\n"
                                           "    color: white;\n"
                                           "}")
        self.label_node_data.setObjectName("label_node_data")
        self.verticalLayout_3.addWidget(self.label_node_data)
        self.textEdit_node_data = QtWidgets.QTextEdit(self.frame_node_data)
        self.textEdit_node_data.setStyleSheet("QTextEdit{\n"
                                              "    background-color: transparent;\n"
                                              "    border: none;\n"
                                              "    border-radius: 0px;\n"
                                              "    border-left:2px solid white;\n"
                                              "    border-left-style: solid;\n"
                                              "    color: white;\n"
                                              "    font: 63 14pt \"Segoe UI Semibold\";\n"
                                              "}")
        self.textEdit_node_data.setObjectName("textEdit_node_data")
        self.verticalLayout_3.addWidget(self.textEdit_node_data)
        self.horizontalLayout_9.addWidget(self.frame_node_data)

        self.view = GraphicsView(self.frame_graph)
        self.view.setObjectName("graphicsView")

        self.gripper = QtWidgets.QSizeGrip(MainWindow)
        self.gripper.setMaximumSize(QtCore.QSize(20, 20))
        self.gripper.setMinimumSize(QtCore.QSize(20, 20))
        self.gripper.setStyleSheet("""
            QSizeGrip {
	            background-image: url(:/icons/cil-size-grip.png);
	            background-position: center;
	            background-repeat: no-repeat;
            }
        """)
        self.gripper.setObjectName('gripper')

        self.horizontalLayout.addWidget(self.frame_container)
        self.horizontalLayout.addWidget(self.view)
        self.verticalLayout_2.addWidget(self.frame_graph)
        self.verticalLayout.addWidget(self.frame_central)
        self.verticalLayout.addWidget(self.gripper, 0, QtCore.Qt.AlignRight | QtCore.Qt.AlignBottom)

        MainWindow.setCentralWidget(self.centralwidget)
        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.label_title.setText(_translate("MainWindow", "GRAPH EDITOR"))
        self.label_mode.setText(_translate("MainWindow", "DARK MODE"))
        self.label_node_count.setText(_translate("MainWindow", "Node count"))
        self.label_node_data.setText(_translate("MainWindow", "Node data"))
        self.label_force_mode.setText(_translate("MainWindow", "Force mode"))
        self.pushButton_force_mode.setText(_translate("MainWindow", "PushButton"))
        # self.label_force_mode_edge_ideal_length.setText(_translate("MainWindow", "Edge ideal length"))
        self.label_node_radius.setText(_translate("MainWindow", "Node radius"))
        self.label_DFS.setText(_translate("MainWindow", "DFS"))
        self.label_BFS.setText(_translate("MainWindow", "BFS"))
        self.pushButton_directed.setText(_translate("MainWindow", "Directed"))
        self.pushButton_undirected.setText(_translate("MainWindow", "Undirected"))
        self.pushButton_run_commands.setText(_translate("MainWindow", "Run Commands"))


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
