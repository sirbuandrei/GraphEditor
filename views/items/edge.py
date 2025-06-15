import math

import numpy as np
from PyQt5.QtCore import Qt, QPointF, QLineF
from PyQt5.QtGui import QPen, QPainterPath, QFontMetrics, QFont
from PyQt5.QtWidgets import QGraphicsPathItem

from views.items.node import LightweightNode


class Edge(QGraphicsPathItem):
    _arrow_length = 15
    _text_font = QFont('Segoe UI', 10)

    def __init__(self, start_node, end_node, cost=None, directed=False):
        super().__init__()
        self._start_node = start_node
        self._end_node = end_node
        self._cost = cost
        self._is_directed = directed
        self._pen = QPen(Qt.white, 2, Qt.SolidLine)

        self.setZValue(1)

        start_pos = start_node.pos()
        end_pos = end_node.pos()

        path = QPainterPath(start_pos)
        path.lineTo(end_pos)

        self.setPath(path)
        self.setPen(self._pen)

    def get_color(self):
        return self._pen.color()

    def get_tuple(self):
        return self._start_node.get_text(), self._end_node.get_text()

    def get_start_node(self):
        return self._start_node

    def get_end_node(self):
        return self._end_node

    def get_cost(self):
        return self._cost

    def set_cost(self, cost):
        self._cost = cost

    def change_graph_type(self, directed):
        self._is_directed = directed

    def update_path(self):
        self.prepareGeometryChange()
        self._create_path()

    def color_change(self, color):
        self._pen.setColor(color)
        self.update()

    def _create_path(self):
        if not self._start_node or not self._end_node:
            return

        start_point, end_point = self._get_connection_points()

        # Create the path
        path = QPainterPath(start_point)

        control_point = self._calculate_control_point(start_point, end_point)

        path.cubicTo(control_point, control_point, end_point)

        if self._is_directed:
            self._add_arrow_to_path(path, control_point, end_point)

        if self._cost:
            self._add_cost_to_path(path, control_point)

        # Set the path and appearance
        self.setPath(path)
        self.setPen(self._pen)

    def _get_connection_points(self):
        node1_pos = self._start_node.pos()
        node2_pos = self._end_node.pos()
        _radius = self._start_node.get_radius()

        # Calculate angle between nodes
        dx = node2_pos.x() - node1_pos.x()
        dy = node2_pos.y() - node1_pos.y()

        distance = math.sqrt(dx * dx + dy * dy)

        # If nodes are too close, return center points
        if distance < 2 * _radius:
            return node1_pos, node2_pos

        # Calculate angle
        angle = math.atan2(dy, dx)

        # Calculate connection points on circle edges
        start_point = QPointF(
            node1_pos.x() + _radius * math.cos(angle),
            node1_pos.y() + _radius * math.sin(angle)
        )

        end_point = QPointF(
            node2_pos.x() - _radius * math.cos(angle),
            node2_pos.y() - _radius * math.sin(angle)
        )

        return start_point, end_point

    def _calculate_control_point(self, start_point, end_point):
        control_point = QPointF((start_point.x() + end_point.x()) / 2,
                                (start_point.y() + end_point.y()) / 2)
        point1 = point2 = None

        _path = QGraphicsPathItem()
        _painter_path = QPainterPath(start_point)
        _painter_path.lineTo(end_point)
        _path.setPath(_painter_path)

        intersecting_items = self.scene().collidingItems(_path)
        intersecting_items.remove(self._start_node)
        intersecting_items.remove(self._end_node)

        try:
            m = -1 * (self._end_node.x() - self._start_node.x()) / (self._end_node.y() - self._start_node.y())
            agent = 1 + (m ** 2)
            factors = [agent, -2 * control_point.x() * agent,
                       (control_point.x() ** 2) * agent - (self._start_node.get_radius() * 2) ** 2]
            roots = np.roots(factors)

        except ZeroDivisionError:
            point1 = control_point + QPointF(0, self._start_node.get_radius() * 2)
            point2 = control_point - QPointF(0, self._start_node.get_radius() * 2)

        for item in intersecting_items:
            if isinstance(item, LightweightNode):
                if (point1 and point2) is None:
                    point1 = QPointF(roots[0], m * (roots[0] - control_point.x()) + control_point.y())
                    point2 = QPointF(roots[1], m * (roots[1] - control_point.x()) + control_point.y())

                line1 = QLineF(item.pos(), point1)
                line2 = QLineF(item.pos(), point2)

                control_point = point2 if line1.length() <= line2.length() else point1
                break

        return control_point

    def _add_cost_to_path(self, path, control_point):
        font_metrics = QFontMetrics(self._text_font)
        font_offset = QPointF(font_metrics.height(), font_metrics.horizontalAdvance(str(self._cost)))
        path.addText(control_point - font_offset / 2, self._text_font, str(self._cost))

    def _add_arrow_to_path(self, path, control_point, end_point):
        pos = path.currentPosition()
        dx, dy, angle = self._calculate_angle(control_point, end_point)

        path.lineTo(QPointF(pos.x() + self._arrow_length * math.cos(angle + 60),
                            pos.y() + self._arrow_length * math.sin(angle + 60)))
        path.moveTo(end_point)
        path.lineTo(QPointF(pos.x() + self._arrow_length * math.cos(angle - 60),
                            pos.y() + self._arrow_length * math.sin(angle - 60)))

    def _calculate_angle(self, p1, p2):
        dy = p2.y() - p1.y()
        dx = p2.x() - p1.x()
        angle = math.atan2(dy, dx)

        return dx, dy, angle