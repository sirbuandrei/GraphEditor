#
from PyQt5.QtWidgets import QGraphicsItem, QWidget, QGraphicsSimpleTextItem, QGraphicsPathItem, QGraphicsLineItem
from PyQt5.QtCore import QRectF, Qt, QPointF
from PyQt5.QtGui import QPen, QColor, QPainter, QFont, QPalette, QPainterPathStroker, QPainterPath,QBrush

import random, math


class Node(QGraphicsItem):

    def __init__(self, _text, _engine):
        super(Node, self).__init__()
        self.setZValue(1)
        self.setFlag(QGraphicsItem.ItemIsMovable)
        self.engine = _engine
        self.text = NodeText(_text, self)
        self.setPos(*self.randomize_pos(_engine.nodeParent.width(),
                                        _engine.nodeParent.height()))
        self.vel = QPointF(0, 0)
        self.oldPos = QPointF(self.x(), self.y())
        self.isColliding = False
        self.force = QPointF(0, 0)
        self.forceR = QPointF(0, 0)
        self.pinned = False
        self.connectedTo = []
        self.fieldRadius = 80
        self.acc = QPointF(0, 0)
        self.isClicked = False

    def boundingRect(self):
        return QRectF(0, 0, self.engine.node_radius, self.engine.node_radius)

    def paint(self, _painter, _option, _widget: QWidget = None):
        _painter.setRenderHint(QPainter.Antialiasing)
        _painter.setPen(QPen(Qt.white, 2, Qt.SolidLine))
        _painter.setBrush(QBrush(Qt.red))
        _painter.drawEllipse(0, 0, self.engine.node_radius, self.engine.node_radius)

    def mouseReleaseEvent(self, _event):
        self.pinned = not self.pinned

        super(Node, self).mouseReleaseEvent(_event)

    def center(self):
        return QPointF(self.x() + self.engine.node_radius, self.y() + self.engine.node_radius)

    def randomize_pos(self, width, height):
        possible_pos = random.choice([
            (random.randint(50, height), random.randint(50, 100)),
            (random.randint(50, 100), random.randint(50, width)),
            (random.randint(50, height), random.randint(width - 100, width)),
            (random.randint(height - 100, height), random.randint(50, width))
        ])

        return possible_pos


class NodeText(QGraphicsSimpleTextItem):

    def __init__(self, _text, _parent):
        # TODO: set text position
        super(NodeText, self).__init__(_text, _parent)
        self.setPen(QPen(Qt.white))
        self.setFont(QFont('Segoe UI Semibold', 10))
        self.setPos(15, 15)


class Edge(QGraphicsPathItem):

    def __init__(self, node1, node2):
        super(Edge, self).__init__()
        self.node1 = node1
        self.node2 = node2
        self.setPen(QPen(Qt.white, 2, Qt.SolidLine))
        self.setBrush(QBrush(Qt.white))

    def create_path(self, radius):
        path = QPainterPath()
        path.moveTo(self.node1.x() + radius, self.node1.y() + radius)
        path.lineTo(self.node2.x() + radius, self.node2.y() + radius)

        return path


class Connection(object):

    def __init__(self, node1, node2, length):
        self.node1 = node1
        self.node2 = node2
        self.length = length