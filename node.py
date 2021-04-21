#
from PyQt5.QtWidgets import (QGraphicsItem, QWidget, QGraphicsSimpleTextItem, QGraphicsPathItem)
from PyQt5.QtCore import (QRectF, Qt, QPointF, QVariantAnimation)
from PyQt5.QtGui import (QPen, QColor, QFont, QPainterPath, QBrush, QPolygonF)

import random
import math
import numpy as np

DFS_COLOR = QColor('yellow')
BFS_COLOR = QColor('orange')


class Node(QGraphicsItem):

    def __init__(self, _text, _engine):
        super(Node, self).__init__()
        self.setZValue(1)
        self.setFlags(QGraphicsItem.ItemIsMovable | QGraphicsItem.ItemSendsScenePositionChanges)

        self.engine = _engine
        self.text = NodeText(_text, self)
        self.setPos(*self.randomize_pos(_engine.view.scene.sceneRect()))
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
        return QRectF(-self.engine.node_radius, -self.engine.node_radius,
                      self.engine.node_radius * 2, self.engine.node_radius * 2)

    def paint(self, painter, option, widget: QWidget = None):
        painter.setPen(self.pen)
        painter.drawEllipse(self.boundingRect())

    def mousePressEvent(self, event):
        self.engine.gravity = False
        self.engine.remove_all_connections()

        return super(Node, self).mousePressEvent(event)

    def mouseMoveEvent(self, event):
        super(Node, self).mouseMoveEvent(event)

        scene_rect = self.scene().sceneRect()
        bounding_rect = self.boundingRect()

        if self.x() - bounding_rect.width() < 0:
            self.setPos(bounding_rect.width(), self.y())
        elif self.x() + bounding_rect.width() > scene_rect.width():
            self.setPos(scene_rect.width() - bounding_rect.width(), self.y())

        if self.y() - bounding_rect.height() < 0:
            self.setPos(self.x(), bounding_rect.height())
        elif self.y() + bounding_rect.height() > scene_rect.height():
            self.setPos(self.x(), scene_rect.height() - bounding_rect.height())

    def mouseReleaseEvent(self, event):
        self.engine.gravity = True

        return super(Node, self).mouseReleaseEvent(event)

    def mouseDoubleClickEvent(self, event):
        self.connectedTo.clear()
        self.pinned = not self.pinned
        self.thickness = 2
        if self.pinned:
            self.thickness = 3.5

        return super(Node, self).mouseDoubleClickEvent(event)

    def center(self):
        return QPointF(self.x(), self.y())

    def randomize_pos(self, scene_rect):
        width = scene_rect.width()
        height = scene_rect.height()

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


class Edge(QGraphicsPathItem):

    def __init__(self, node1, node2, engine, cost=None):
        super().__init__()
        self.node1 = node1
        self.node2 = node2
        self.engine = engine
        self.cost = cost
        self.arrow_length = 15

        self.setPen(QPen(Qt.white, 1.5, Qt.SolidLine))
        #self.setBrush(QBrush(Qt.white))

        self.DFS_animation = self.create_animation(DFS_COLOR)
        self.BFS_animation = self.create_animation(BFS_COLOR)

    def create_path(self, start_point, control_point, end_point, directed, alfa):
        path = QPainterPath()

        path.moveTo(start_point)

        intersecting_items = self.engine.view.scene.collidingItems(self)
        for item in intersecting_items:
            if (not isinstance(item, NodeText)) and (not isinstance(item, Edge)) and \
                    (item is not self.node1) and (item is not self.node2):
                m = - (self.node2.x() - self.node1.x()) / (self.node2.y() - self.node1.y())
                coeff = [1 + m ** 2, - 2 * control_point.y() - 2 * (m ** 2) * control_point.y(),
                         control_point.y() ** 2 + 4 * ((m * control_point.x()) ** 2) + ((m * control_point.y()) ** 2)
                         - ((m * self.engine.node_radius) ** 2)]
                roots = np.roots(coeff)
                #print(roots)
                #y = roots[0]
                #x = (y - control_point.y() + m * control_point.x()) / m
                #control_point = QPointF(x, y)

        path.cubicTo(control_point, control_point, end_point)

        if directed:
            pos = path.currentPosition()

            dx, dy, angle = self.engine.get_angle(control_point, self.node2)

            arrow = QPolygonF()
            arrow << QPointF(pos.x(), pos.y()) \
                  << QPointF(pos.x() + self.arrow_length * math.cos(angle + 60),
                             pos.y() + self.arrow_length * math.sin(angle + 60)) \
                  << QPointF(pos.x() + self.arrow_length * math.cos(angle - 60),
                             pos.y() + self.arrow_length * math.sin(angle - 60)) \
                  << QPointF(pos.x(), pos.y())

            path.addPolygon(arrow)

        return path

    def create_animation(self, color):
        animation = QVariantAnimation()
        animation.valueChanged.connect(self.handle_valueChanged)
        animation.setStartValue(self.pen().color())
        animation.setEndValue(color)
        animation.setDuration(1000)
        #animation.finished.connect(self.setPen(QPen(color, 1.5, Qt.SolidLine)))
        return animation

    def handle_valueChanged(self, value):
        self.setPen(QPen(value, 1.5, Qt.SolidLine))
        #self.setBrush(QBrush(value))


class Connection(object):

    def __init__(self, node1, node2, length):
        self.node1 = node1
        self.node2 = node2
        self.length = length
