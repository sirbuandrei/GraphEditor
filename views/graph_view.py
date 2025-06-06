from datetime import datetime

from PyQt5.QtCore import QRectF, QBasicTimer, QTimer, pyqtSignal, QObject
from PyQt5.QtGui import QPainter
from PyQt5.QtWidgets import QGraphicsView, QGraphicsScene


class GraphView(QGraphicsView):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setRenderHint(QPainter.HighQualityAntialiasing)
        #self.setRenderHint(QPainter.SmoothPixmapTransform)

        self.frameRateTimer = QBasicTimer()
        self.startTimer(17)

        self.scene = QGraphicsScene(self)
        self.setScene(self.scene)

    def resizeEvent(self, event):
        self.scene.setSceneRect(QRectF(0, 0, self.width(), self.height()))

    def timerEvent(self, event):
        if self.scene.isActive():
            self.update()
