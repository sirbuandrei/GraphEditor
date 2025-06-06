from PyQt5.QtCore import QRectF, QBasicTimer, QTimer, pyqtSignal, QObject
from PyQt5.QtGui import QPainter
from PyQt5.QtWidgets import QGraphicsView, QGraphicsScene, QGraphicsItem


class GraphView(QGraphicsView):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setRenderHint(QPainter.HighQualityAntialiasing)
        self.setRenderHint(QPainter.TextAntialiasing)
        #self.setRenderHint(QPainter.SmoothPixmapTransform)
        #self.setRenderHint(QPainter.NonCosmeticDefaultPen)

        self.scene = QGraphicsScene()
        self.setScene(self.scene)

        # self.frameRateTimer = QBasicTimer()
        # self.startTimer(17)

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.scene.setSceneRect(QRectF(0, 0, self.width(), self.height()))

    # def timerEvent(self, event):
    #     if self.scene and self.scene.isActive():
    #         self.update()