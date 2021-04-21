#
from PyQt5.QtWidgets import (QGraphicsView, QGraphicsScene)
from PyQt5.QtCore import (QBasicTimer, QRectF)
from PyQt5.QtGui import QPainter

from engine import GraphEngine


class GraphicsView(QGraphicsView):
    def __init__(self, parent):
        super(GraphicsView, self).__init__(parent=parent)
        self.setRenderHint(QPainter.HighQualityAntialiasing)
        self.frame_graph = parent
        self.frameRateTimer = QBasicTimer()
        self.frameRateTimer.start(17, self)
        self.engine = GraphEngine(self)

        self.scene = QGraphicsScene(self)
        self.setScene(self.scene)
        self.show()

    def resizeEvent(self, event):
        self.scene.setSceneRect(QRectF(10, 10, self.width() - 10, self.height() - 10))

    def timerEvent(self, timerEvent):
        if self.engine.force_mode:
            self.engine.update_nodes()
            self.engine.update_connections()
        self.engine.draw_edges()
        self.update()
