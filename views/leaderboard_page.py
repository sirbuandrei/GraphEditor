from PyQt5 import QtWidgets, QtCore
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QProgressBar, QWidget, QHBoxLayout


class LeaderboardPage(QtWidgets.QFrame):
    show_page = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setMinimumSize(QtCore.QSize(250, 0))
        self.setMaximumSize(QtCore.QSize(250, 16777215))
        self.setStyleSheet("""
                    QFrame {
                        background-color: #63676e;
                        border-radius: 15px;
                    }
                """)
        self.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.setFrameShadow(QtWidgets.QFrame.Raised)

        # Layout inside leaderboard frame
        self.verticalLayout_leaderboard = QtWidgets.QVBoxLayout(self)
        self.verticalLayout_leaderboard.setContentsMargins(10, 10, 10, 10)

        # Table widget
        self.tableWidget_leaderboard = QtWidgets.QTableWidget(self)
        self.tableWidget_leaderboard.setColumnCount(2)
        self.tableWidget_leaderboard.setHorizontalHeaderLabels(["Email", "Points"])
        self.tableWidget_leaderboard.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.tableWidget_leaderboard.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self.tableWidget_leaderboard.setShowGrid(False)

        # Stretch last column
        self.tableWidget_leaderboard.horizontalHeader().setStretchLastSection(True)

        # Make table + header transparent
        self.tableWidget_leaderboard.setStyleSheet("""
                    QTableWidget {
                        background-color: transparent;
                        color: white;
                        border: none;
                        font: 12pt 'Segoe UI';
                        selection-background-color: #7289da;
                        selection-color: white;
                    }
                    QHeaderView::section {
                        background-color: transparent;
                        color: white;
                        padding: 6px;
                        border: none;
                        font-weight: bold;
                    }
                    QTableCornerButton::section {
                        background-color: transparent;
                        border: none;
                    }
                    QScrollBar:vertical {
                        background: transparent;
                        width: 12px;
                        margin: 0px;
                    }
                    QScrollBar::handle:vertical {
                        background: #7289da;
                        border-radius: 6px;
                    }
                    QScrollBar::add-line:vertical,
                    QScrollBar::sub-line:vertical {
                        background: none;
                        height: 0px;
                    }
                    QScrollBar:horizontal {
                        background: transparent;
                        height: 12px;
                        margin: 0px;
                    }
                    QScrollBar::handle:horizontal {
                        background: #7289da;
                        border-radius: 6px;
                    }
                    QScrollBar::add-line:horizontal,
                    QScrollBar::sub-line:horizontal {
                        background: none;
                        width: 0px;
                    }
                """)

        self.loading_container = QWidget(self)
        self.loading_layout = QHBoxLayout(self.loading_container)
        self.loading_layout.setAlignment(QtCore.Qt.AlignCenter)

        # Progress bar
        self.progress_bar = QProgressBar(self.loading_container)
        self.progress_bar.setFixedSize(120, 8)
        self.progress_bar.setRange(0, 0)  # Indeterminate
        self.progress_bar.setTextVisible(False)
        self.progress_bar.setStyleSheet("""
            QProgressBar {
                border: none;
                border-radius: 4px;
                background-color: #d3d3d3;
            }
            QProgressBar::chunk {
                background-color: #7289da;
                border-radius: 4px;
            }
        """)

        self.loading_layout.addWidget(self.progress_bar)
        self.verticalLayout_leaderboard.addWidget(self.loading_container)
        self.loading_container.hide()

        self.verticalLayout_leaderboard.addWidget(self.tableWidget_leaderboard)

    def set_loading(self, loading: bool):
        self.loading_container.setVisible(loading)
        self.tableWidget_leaderboard.setVisible(not loading)

    def update_leaderboard(self, data):
        self.tableWidget_leaderboard.setRowCount(len(data))
        for row, (email, points) in enumerate(data):
            email_item = QtWidgets.QTableWidgetItem(email)
            points_item = QtWidgets.QTableWidgetItem(str(points))

            points_item.setTextAlignment(QtCore.Qt.AlignCenter)

            self.tableWidget_leaderboard.setItem(row, 0, email_item)
            self.tableWidget_leaderboard.setItem(row, 1, points_item)

    def showEvent(self, event):
        super().showEvent(event)
        self.show_page.emit()

    def hideEvent(self, event):
        super().hideEvent(event)
        self.tableWidget_leaderboard.clearContents()
        self.tableWidget_leaderboard.setRowCount(0)
