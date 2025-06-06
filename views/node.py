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


class LightweightNode(QGraphicsItem):
    # Shared resources
    _shared_pen = None
    _shared_font = None

    @classmethod
    def get_shared_pen(cls):
        if cls._shared_pen is None:
            cls._shared_pen = QPen(Qt.white, 2, Qt.SolidLine)
        return cls._shared_pen

    @classmethod
    def get_shared_font(cls):
        if cls._shared_font is None:
            cls._shared_font = QFont('Segoe UI Semibold', 11)
        return cls._shared_font

    def __init__(self, text, pos=None):
        super().__init__()

        # Set flags and properties
        self.setFlags(QGraphicsItem.ItemIsMovable | QGraphicsItem.ItemIsSelectable)
        self.setZValue(1)

        # Store data
        self.radius = 15
        self.node_text = text

        # CRITICAL: Pre-calculate and cache bounding rect
        # This must be constant and fast according to Qt docs
        r = self.radius
        self._cached_bounding_rect = QRectF(-r, -r, 2 * r, 2 * r)

        # Set position
        if pos:
            if hasattr(pos, 'x') and hasattr(pos, 'y'):
                self.setPos(pos.x(), pos.y())
            else:
                self.setPos(pos[0], pos[1])
        else:
            self.setPos(300, 300)

    def boundingRect(self):
        """
        CRITICAL: This method is called VERY frequently by Qt.
        Must be fast, consistent, and never cause side effects.
        From Qt docs: "This function should be as fast as possible"
        """
        # Return pre-calculated rect - NO calculations, NO method calls
        return self._cached_bounding_rect

    def paint(self, painter, option, widget=None):
        """
        Paint the node. This is only called when Qt needs to repaint.
        """
        try:
            # Draw circle
            painter.setPen(self.get_shared_pen())
            painter.drawEllipse(self._cached_bounding_rect)

            # Draw text
            painter.setFont(self.get_shared_font())
            painter.setPen(QPen(Qt.white))

            # Get text metrics ONLY during paint, not in boundingRect
            fm = painter.fontMetrics()
            text_rect = fm.boundingRect(self.node_text)

            # Center text
            text_x = -text_rect.width() / 2
            text_y = text_rect.height() / 4

            painter.drawText(text_x, text_y, self.node_text)

        except Exception as e:
            print(f"Paint error: {e}")

    def get_text(self):
        return self.node_text

    def mousePressEvent(self, event):
        super().mousePressEvent(event)

    def mouseMoveEvent(self, event):
        super().mouseMoveEvent(event)
