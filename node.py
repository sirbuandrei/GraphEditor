#
from PyQt5.QtWidgets import (QGraphicsItem, QWidget, QGraphicsSimpleTextItem, QGraphicsPathItem, QGraphicsObject)
from PyQt5.QtCore import (QRectF, Qt, QPointF, QVariantAnimation)
from PyQt5.QtGui import (QPen, QColor, QPainter, QFont, QPainterPath, QBrush, QPolygonF)

import random
import math
import numpy as np

DFS_COLOR = QColor('yellow')
BFS_COLOR = QColor('orange')


class Node(QGraphicsItem):

    def __init__(self, _text, _engine):
        super(Node, self).__init__()
        self.setZValue(1)
        self.setFlag(QGraphicsItem.ItemIsMovable)
        self.engine = _engine
        self.text = NodeText(_text, self)
        self.setPos(*self.randomize_pos(_engine.view.width(),
                                        _engine.view.height()))
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
        self.thickness = 2
        self.edges = []
        self.pen = QPen(Qt.white, self.thickness, Qt.SolidLine)

        self.DFS_animation = QVariantAnimation()
        self.DFS_animation.valueChanged.connect(self.handle_valueChanged)
        self.DFS_animation.setStartValue(self.pen.color())
        self.DFS_animation.setEndValue(DFS_COLOR)
        self.DFS_animation.setDuration(1000)

        self.BFS_animation = QVariantAnimation()
        self.BFS_animation.valueChanged.connect(self.handle_valueChanged)
        self.BFS_animation.setStartValue(self.pen.color())
        self.BFS_animation.setEndValue(BFS_COLOR)
        self.BFS_animation.setDuration(1000)

    def __repr__(self):
        return self.text.text()

    def boundingRect(self):
        return QRectF(-self.engine.node_radius - self.pen.width() / 2, -self.engine.node_radius - self.pen.width() / 2,
                      self.engine.node_radius * 2 + self.pen.width(), self.engine.node_radius * 2 + self.pen.width())

    def paint(self, painter, option, widget: QWidget = None):
        painter.setRenderHint(QPainter.Antialiasing)
        painter.setPen(self.pen)
        painter.drawEllipse(self.boundingRect())

    def mousePressEvent(self, event):
        self.engine.gravity = False
        self.pinned = True
        self.engine.remove_all_connections()

        super(Node, self).mousePressEvent(event)

    def mouseReleaseEvent(self, event):
        self.engine.gravity = True
        self.pinned = False

        super(Node, self).mouseReleaseEvent(event)

    def mouseDoubleClickEvent(self, event):
        self.connectedTo.clear()
        self.pinned = not self.pinned
        self.thickness = 2
        if self.pinned:
            self.thickness = 3.5

        super(Node, self).mouseDoubleClickEvent(event)

    def center(self):
        return QPointF(self.x() + self.engine.node_radius, self.y() + self.engine.node_radius)

    def randomize_pos(self, width, height):
        pos = random.choice([
            (random.randint(50, height - 50), random.randint(50, 100)),
            (random.randint(50, 100), random.randint(50, width - 50)),
            (random.randint(50, height - 50), random.randint(width - 100, width - 50)),
            (random.randint(height - 100, height - 50), random.randint(50, width - 50))
        ])
        return pos

    def handle_valueChanged(self, value):
        self.pen = QPen(value, self.thickness, Qt.SolidLine)


class NodeText(QGraphicsSimpleTextItem):

    def __init__(self, text, parent):
        super(NodeText, self).__init__(text, parent)
        self.setPen(QPen(Qt.white, 0.5, Qt.SolidLine))
        self.setBrush(QBrush(Qt.white))
        self.setFont(QFont('Segoe UI Semibold', 11))
        self.setPos(-self.boundingRect().width() / 2, -self.boundingRect().height() / 2)

class Edge(QGraphicsObject):

    def __init__(self, node1, node2, engine):
        super().__init__()
        self.node1 = node1
        self.node2 = node2
        self.engine = engine
        self.arrow_length = 15
        self.pen = QPen(Qt.white, 1.5, Qt.SolidLine)
        self.brush = QBrush(Qt.white)

    def boundingRect(self):
        rect = QRectF()



# class Edge(QGraphicsPathItem):
#
#     def __init__(self, node1, node2):
#         super().__init__()
#         self.node1 = node1
#         self.node2 = node2
#         self.arrow_length = 15
#         self.setPen(QPen(Qt.white, 1.5, Qt.SolidLine))
#         self.setBrush(QBrush(Qt.white))
#
#         self.DFS_animation = self.create_animation(DFS_COLOR)
#         self.BFS_animation = self.create_animation(BFS_COLOR)
#
#     def create_path(self, radius, directed, dx, dy, alfa1, alfa2):
#         path = QPainterPath()
#
#         path.moveTo(self.node1.x() + radius * (1 + math.cos(alfa1)),
#                     self.node1.y() + radius * (1 + math.sin(alfa1)))
#         path.lineTo(self.node2.x() + radius * (1 + math.cos(alfa2)),
#                     self.node2.y() + radius * (1 + math.sin(alfa2)))
#
#         # intersecting_nodes = []
#         # for node in self.node1.engine.nodes:
#         #     bounding_rect = node.boundingRect()
#         #     if (node is not self.node1) and (node is not self.node2) and \
#         #             (path.contains(QPointF(100, 100))):
#         #         intersecting_nodes.append(node)
#
#
#
#         # for node in self.node1.engine.nodes:
#         #     if (node is not self.node1) and (node is not self.node2) and \
#         #             self.node1.engine.view.scene.collidingItems(self, node):
#         #         print(node)
#
#         # QRectF(node.x(), node.y(), node.x() + bounding_rect.width(),
#         #        node.y() + bounding_rect.height())
#
#         # if intersecting_node:
#         #     path.clear()
#         #     path.moveTo(self.node1.x() + radius * (1 + math.cos(alfa1)),
#         #                 self.node1.y() + radius * (1 + math.sin(alfa1)))
#         #     control = QPointF(intersecting_node.x() + 20, intersecting_node.y() + 20)
#         #     end = QPointF(self.node2.x() + radius * (1 + math.cos(alfa2)),
#         #                   self.node2.y() + radius * (1 + math.sin(alfa2)))
#         #     path.cubicTo(control, control, end)
#
#         if directed:
#             pos = path.currentPosition()
#             arrow = QPolygonF()
#             arrow << QPointF(pos.x(), pos.y()) \
#                   << QPointF(pos.x() + self.arrow_length * math.cos(alfa1 + 60),
#                              pos.y() + self.arrow_length * math.sin(alfa1 + 60)) \
#                   << QPointF(pos.x() + self.arrow_length * math.cos(alfa1 - 60),
#                              pos.y() + self.arrow_length * math.sin(alfa1 - 60)) \
#                   << QPointF(pos.x(), pos.y())
#             path.addPolygon(arrow)
#
#         # TODO: add path text
#
#         return path
#
#     def create_animation(self, color):
#         animation = QVariantAnimation()
#         animation.valueChanged.connect(self.handle_valueChanged)
#         animation.setStartValue(self.pen().color())
#         animation.setEndValue(color)
#         animation.setDuration(1000)
#         return animation
#
#     def handle_valueChanged(self, value):
#         self.setPen(QPen(value, 1.5, Qt.SolidLine))
#         self.setBrush(QBrush(value))


class Connection(object):

    def __init__(self, node1, node2, length):
        self.node1 = node1
        self.node2 = node2
        self.length = length
