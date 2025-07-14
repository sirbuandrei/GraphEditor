from PyQt5 import QtGui
from PyQt5.QtCore import QRectF, QBasicTimer, Qt, pyqtSignal
from PyQt5.QtGui import QPainter
from PyQt5.QtWidgets import QGraphicsView, QGraphicsScene, QGraphicsTextItem

from utils.physics_engine import PhysicsEngine


class GraphView(QGraphicsView):
    space_pressed = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self._physics_engine = PhysicsEngine(self)
        self._gravity = None
        self._force_mode = None
        self._directed = None
        self._nodes = []
        self._edges = []
        self._frameRateTimer = QBasicTimer()
        self._text = QGraphicsTextItem()
        self.scene = QGraphicsScene()

        self.setRenderHints(QPainter.HighQualityAntialiasing | QPainter.TextAntialiasing)
        self._text.setFont(QtGui.QFont("Segoe UI", 13, QtGui.QFont.Bold))
        self.setScene(self.scene)
        self.startTimer(17)

    def set_text(self, text, color):
        self._text.setPlainText(text)
        self._text.setDefaultTextColor(QtGui.QColor(color))

        scene_rect = self.scene.sceneRect()
        text_width = self._text.boundingRect().width()
        self._text.setPos((scene_rect.width() - text_width) / 2, 10)

        self.scene.addItem(self._text)

    def clear_text(self):
        self.scene.removeItem(self._text)

    def set_force_mode(self, is_enabled: bool):
        self._physics_engine.update_connections()
        self._force_mode = is_enabled
        self._gravity = False if not is_enabled else ...

    def get_directed(self):
        return self._directed

    def get_force_mode(self):
        return self._force_mode

    def get_gravity(self):
        return self._gravity

    def get_nodes(self):
        return self._nodes

    def get_edges(self):
        return self._edges

    def add_node(self, node):
        self._nodes.append(node)
        self.scene.addItem(node)

    def add_edge(self, edge):
        self._edges.append(edge)
        self.scene.addItem(edge)

        edge.get_start_node().add_edge(edge)
        edge.get_end_node().add_edge(edge)

    def remove_node(self, node):
        self._physics_engine.update_connections()
        self._nodes.remove(node)
        self.scene.removeItem(node)

    def remove_edge(self, edge):
        self._edges.remove(edge)
        self.scene.removeItem(edge)

    def change_directed(self, directed):
        self._directed = directed
        for edge in self._edges:
            edge.change_graph_type(directed)

    def resizeEvent(self, event):
        self.scene.setSceneRect(QRectF(0, 0, self.width(), self.height()))
        return  super(GraphView, self).resizeEvent(event)

    def timerEvent(self, event):
        if self.scene and self.scene.isActive():
            self._physics_engine.apply_physics()
            self.update()

    def mousePressEvent(self, event):
        if self.scene.items(event.pos()):
            self._physics_engine.update_connections()
            self._gravity = False if self._force_mode else ...
        return super(GraphView, self).mousePressEvent(event)

    def mouseReleaseEvent(self, event):
        if self._force_mode:
            self._gravity = True if not self._gravity else ...
            self._physics_engine.update_connections()
        return super(GraphView, self).mouseReleaseEvent(event)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Space:
            self.space_pressed.emit()
        return super(GraphView, self).keyPressEvent(event)