import random

from PyQt5.QtCore import Qt, QRectF
from PyQt5.QtGui import QPen, QBrush, QColor, QFont
from PyQt5.QtWidgets import QGraphicsEllipseItem, QGraphicsItem, QWidget, QGraphicsSimpleTextItem


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

        self.setPos(300, 300)

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

        if self.x() - bounding_rect.width() < 0:
            self.setPos(bounding_rect.width(), self.y())
        elif self.x() + bounding_rect.width() > scene_rect.width():
            self.setPos(scene_rect.width() - bounding_rect.width(), self.y())

        if self.y() - bounding_rect.height() < 0:
            self.setPos(self.x(), bounding_rect.height())
        elif self.y() + bounding_rect.height() > scene_rect.height():
            self.setPos(self.x(), scene_rect.height() - bounding_rect.height())

