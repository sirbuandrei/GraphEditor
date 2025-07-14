import random

from PyQt5.QtCore import Qt, QRectF, QPointF, pyqtProperty, QPropertyAnimation, pyqtSignal, QTimer, QObject
from PyQt5.QtGui import QPen, QBrush, QColor, QFont
from PyQt5.QtWidgets import QGraphicsEllipseItem, QGraphicsItem, QWidget, QGraphicsSimpleTextItem, QGraphicsEffect, \
    QGraphicsColorizeEffect


class NodeText(QGraphicsSimpleTextItem):
    TEXT_FONT = QFont('Segoe UI Semibold', 11)

    def __init__(self, text, parent):
        super(NodeText, self).__init__(text, parent)
        self.setPen(QPen(Qt.white, 0.5, Qt.SolidLine))
        self.setBrush(QBrush(Qt.white))
        self.setFont(self.TEXT_FONT)
        self.setPos(-self.boundingRect().width() / 2, -self.boundingRect().height() / 2)


class Node(QGraphicsItem):
    def __init__(self, text, pos):
        super(Node, self).__init__()
        self.setZValue(1)
        self.setFlags(QGraphicsItem.ItemIsMovable | QGraphicsItem.ItemIsSelectable)

        self.radius = 15
        self.thickness = 2
        self.pen = QPen(Qt.white, self.thickness, Qt.SolidLine)
        self.text = NodeText(text, self)

        self.setPos(pos.x(), pos.y())

    def get_text(self):
        return self.text.text()

    def boundingRect(self):
        r = self.radius
        return QRectF(-r, -r, 2 * r, 2 * r)

    def paint(self, painter, option, widget: QWidget = None):
        painter.setPen(self.pen)
        painter.drawEllipse(self.boundingRect())

    def mousePressEvent(self, event):
        return super(Node, self).mousePressEvent(event)

    def mouseMoveEvent(self, event):
        super(Node, self).mouseMoveEvent(event)

        scene_rect = self.scene().sceneRect()
        bounding_rect = self.boundingRect()

        x = self.x()
        y = self.y()

        if x - bounding_rect.width() < scene_rect.left():
            x = scene_rect.left() + bounding_rect.width()
        elif x + bounding_rect.width() > scene_rect.right():
            x = scene_rect.right() - bounding_rect.width()

        if y - bounding_rect.height() < scene_rect.top():
            y = scene_rect.top() + bounding_rect.height()
        elif y + bounding_rect.height() > scene_rect.bottom():
            y = scene_rect.bottom() - bounding_rect.height()

        self.setPos(x, y)

class NodeText(QGraphicsSimpleTextItem):
    def __init__(self, text, parent):
        super(NodeText, self).__init__(text, parent)
        self.setPen(QPen(Qt.white, 0.5, Qt.SolidLine))
        self.setBrush(QBrush(Qt.white))
        self.setFont(QFont('Segoe UI Semibold', 11))
        self.setPos(-self.boundingRect().width() / 2, -self.boundingRect().height() / 2)


class LightweightNode(QGraphicsItem):
    _shared_font = None

    def __init__(self, text, pos=None, radius=15):
        super().__init__()
        self._radius = radius
        self._node_text = NodeText(text, self)
        self._current_color = QColor("white")
        self._pen = QPen(Qt.white, 2, Qt.SolidLine)
        self._font = QFont('Segoe UI Semibold', 11)
        self._connected_edges = []

        self.setFlags(QGraphicsItem.ItemIsMovable | QGraphicsItem.ItemIsSelectable)
        self.setFlag(QGraphicsItem.ItemSendsGeometryChanges, True)
        self.setZValue(2)
        self.setPos(pos.x(), pos.y())

    def get_center(self):
        return QPointF(self.x(), self.y())

    def get_radius(self):
        return self._radius

    def get_text(self):
        return self._node_text.text()

    def get_color(self):
        return self._pen.color()

    def set_radius(self, radius):
        self.prepareGeometryChange()
        self._radius = radius

    def add_edge(self, edge):
        self._connected_edges.append(edge)

    def boundingRect(self):
        r = self._radius
        return QRectF(-r, -r, 2 * r, 2 * r)

    def paint(self, painter, option, widget=None):
        try:
            painter.setPen(self._pen)
            painter.drawEllipse(self.boundingRect())

        except Exception as e:
            print(f"Paint error: {e}")

    def itemChange(self, change, value):
        if change == QGraphicsItem.ItemPositionChange:
            for edge in self._connected_edges:
                edge.update_path()
        return super().itemChange(change, value)

    def color_change(self, color):
        self._pen.setColor(color)
        self.update()