from PyQt5 import QtWidgets, QtCore
from PyQt5.QtCore import pyqtSignal


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

        self.verticalLayout_leaderboard.addWidget(self.tableWidget_leaderboard)

    def showEvent(self, event):
        super().showEvent(event)
        self.show_page.emit()
