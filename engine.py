#
from node import Node, Connection, Edge

from PyQt5.QtCore import (QPointF, QSequentialAnimationGroup, QVariantAnimation)
from PyQt5.QtWidgets import QLineEdit
from PyQt5.QtGui import QColor

from ctypes import (c_float, c_int32, cast, byref, POINTER)
import numpy as np
import math
from collections import defaultdict

# CONSTANTS
SOFTENING_CONSTANT = 0.15
G = 39.5
dt = 0.017

# ANIMATION COLORS
DFS_COLOR = QColor('yellow')
BFS_COLOR = QColor('orange')


class GraphEngine(object):

    def __init__(self, view):
        self.view = view

        self.nodes = []
        self.edges = []
        self.connections = []
        self.directed_graph = defaultdict(list)
        self.undirected_graph = defaultdict(list)

        self.node_radius = 15
        self.node_fieldRadius = 80
        self.graph_data = ''

        self.label_node_count = self.view.frame_graph.findChild(QLineEdit, 'lineEdit_node_count')
        self.DFS_sequential = QSequentialAnimationGroup()
        self.BFS_sequential = QSequentialAnimationGroup()

        self.gravity = True
        self.force_mode = False
        self.directed = False

    def receive_data(self, text_received):
        if not text_received:

            for node in self.nodes:
                self.view.scene.removeItem(node)
            self.nodes.clear()

            for edge in self.edges:
                self.view.scene.removeItem(edge)
            self.edges.clear()

            self.undirected_graph.clear()
            self.directed_graph.clear()

            return

        self.manipulate_data(text_received)

    def manipulate_data(self, text_received):
        self.graph_data = text_received

        nodes = []
        edges = []

        graph_lines = text_received.split('\n')
        for line in graph_lines:
            _line = list(filter(None, line.split(' ')))
            if len(_line) == 1 and _line[0] not in nodes:
                nodes.append(_line[0])
            elif len(_line) > 1:
                if _line[0] not in nodes:
                    nodes.append(_line[0])
                if _line[1] not in nodes:
                    nodes.append(_line[1])
                if (_line[0], _line[1]) not in edges \
                        and _line[0] is not _line[1]:
                    cost = _line[2] if len(_line) == 3 else None
                    edges.append((_line[0], _line[1], cost))

        self.add_remove_nodes(nodes)
        self.add_remove_edges(edges)

    def add_remove_nodes(self, nodes):
        for node in self.nodes:
            found = False
            for node_text in nodes:
                if node.__repr__() == node_text:
                    found = True
                    nodes.remove(node_text)
                    break
            if not found:
                edge_copy = self.edges.copy()
                for edge in edge_copy:
                    if edge.node1 == node or edge.node2 == node:
                        self.edges.remove(edge)
                        self.view.scene.removeItem(edge)
                del self.directed_graph[node]
                del self.undirected_graph[node]
                self.view.scene.removeItem(node)

        for node_text in nodes:
            node = Node(node_text, self)
            self.directed_graph[node].clear()
            self.undirected_graph[node].clear()
            self.view.scene.addItem(node)

        self.nodes = list(self.directed_graph.keys())
        self.label_node_count.setText(str(len(self.nodes)))

    def add_remove_edges(self, edges):
        edge_copy = self.edges.copy()
        for edge in edge_copy:
            found = False
            for elem in edges:
                n1, n2, cost = elem
                if edge.node1.__repr__() == n1 and edge.node2.__repr__() == n2 and \
                        edge.cost == cost:
                    found = True
                    edges.remove(elem)
                    break
            if not found:
                self.directed_graph[edge.node1].remove(edge.node2)
                self.undirected_graph[edge.node1].remove(edge.node2)
                self.undirected_graph[edge.node2].remove(edge.node1)
                self.view.scene.removeItem(edge)
                self.edges.remove(edge)

        for elem in edges:
            n1, n2, cost = elem
            for node in self.nodes:
                if node.__repr__() == n1:
                    node1 = node
                elif node.__repr__() == n2:
                    node2 = node
            edge = Edge(node1, node2, self, cost)
            self.edges.append(edge)
            self.view.scene.addItem(edge)
            self.directed_graph[node1].append(node2)
            self.undirected_graph[node1].append(node2)
            self.undirected_graph[node2].append(node1)

    def update_nodes(self):
        for node in self.nodes:
            if not node.pinned:
                node.force = self.forces(node)

                tempPos = node.pos()
                node.moveBy(node.force.x() * (dt ** 2),
                            node.force.y() * (dt ** 2))
                node.oldPos = tempPos

            self.check_collision(node)

    def draw_edges(self):
        for edge in self.edges:
            dx, dy, alfa = self.get_angle(edge.node1, edge.node2)

            start_point = QPointF(edge.node1.x() + self.node_radius * (math.cos(alfa)),
                                  edge.node1.y() + self.node_radius * (math.sin(alfa)))

            end_point = QPointF(edge.node2.x() - self.node_radius * (math.cos(alfa)),
                                edge.node2.y() - self.node_radius * (math.sin(alfa)))

            control_point = QPointF(start_point.x() + (end_point.x() - start_point.x()) / 2,
                                    start_point.y() + (end_point.y() - start_point.y()) / 2)

            created_path = edge.create_path(start_point, control_point, end_point, self.directed, alfa)
            edge.setPath(created_path)

    def update_connections(self):
        for connection in self.connections:
            node1 = connection.node1
            node2 = connection.node2

            dx, dy, angle = self.get_angle(node1, node2)
            d = math.sqrt(dx * dx + dy * dy)
            diff = connection.length - d
            percent = diff / d / 2
            offsetX = dx * percent
            offsetY = dy * percent

            if not node1.pinned:
                node1.setPos(node1.x() - offsetX, node1.y() - offsetY)
            if not node2.pinned:
                node2.setPos(node2.x() + offsetX, node2.y() + offsetY)

    def remove_all_connections(self):
        self.connections.clear()
        for node in self.nodes:
            node.connectedTo.clear()

    def remove_node_connections(self, node):
        node.connectedTo.clear()
        for other_node in self.nodes:
            if node in other_node.connectedTo:
                other_node.connectedTo.remove(node)

    def find_edge(self, node1, node2):
        for edge in self.edges:
            if (edge.node1 == node1 and edge.node2 == node2) or \
                    (edge.node1 == node2 and edge.node2 == node1):
                return edge
        return None

    def forces(self, node):
        if self.gravity:
            dx, dy, alfa = self.get_angle(node, QPointF(self.view.width() / 2,
                                                        self.view.height() / 2))
            dsq = math.sqrt(dx * dx + dy * dy)
            # dsq = self.fast_inverse_sqrt(dx * dx + dy * dy)
            # dsq_sc = self.fast_inverse_sqrt(dsq ** -1 + SOFTENING_CONSTANT)
            # force = (G * (dsq * dsq_sc)) ** -1
            force = (dsq * math.sqrt(dsq + SOFTENING_CONSTANT)) / G

            force_x = float(force) * math.cos(alfa)
            force_y = float(force) * math.sin(alfa)

            return QPointF(force_x * abs(dx), force_y * abs(dy))
        return QPointF(0, 0)

    def check_collision(self, node):
        for other_node in self.nodes:
            if other_node is not node:

                dx, dy, alfa = self.get_angle(node.center(), other_node.center())
                dsq = math.sqrt(dx * dx + dy * dy)

                length = self.node_fieldRadius + self.node_radius
                if dsq <= length and other_node not in node.connectedTo:
                    if self.gravity:
                        node.connectedTo.append(other_node)
                        self.connections.append(Connection(node, other_node, length))
                    else:
                        overlap = dsq - self.node_radius - self.node_fieldRadius
                        node.moveBy(-0.5 * overlap * (node.x() - other_node.x()) / dsq,
                                    -0.5 * overlap * (node.y() - other_node.y()) / dsq)
                        other_node.moveBy(0.5 * overlap * (node.x() - other_node.x()) / dsq,
                                          0.5 * overlap * (node.y() - other_node.y()) / dsq)

    def get_angle(self, point1, point2):
        dy = point2.y() - point1.y()
        dx = point2.x() - point1.x()
        return dx, dy, math.atan2(dy, dx)

    def fast_inverse_sqrt(self, number):
        x2 = number * 0.5
        y = c_float(number)

        i = cast(byref(y), POINTER(c_int32)).contents.value
        i = c_int32(0x5f3759df - (i >> 1))
        y = cast(byref(i), POINTER(c_float)).contents.value

        y = y * (1.5 - (x2 * y * y))
        return y

    def start_animations(self, text_DFS, text_BFS):
        if not text_DFS and not text_BFS:
            return

        self.DFS_sequential.clear()
        self.BFS_sequential.clear()

        adj_list = self.undirected_graph if not self.directed else self.directed_graph
        for node in self.nodes:
            if node.__repr__() == text_DFS:
                visited = np.zeros(len(self.nodes))
                self.DFS(node, visited, adj_list)
            elif node.__repr__() == text_BFS:
                visited = np.zeros(len(self.nodes))
                self.BFS(node, visited, adj_list)

        self.DFS_sequential.start()
        self.BFS_sequential.start()

    def DFS(self, start, visited, adj_list):
        visited[self.nodes.index(start)] = 1
        self.DFS_sequential.addAnimation(self.create_animation(start, start.pen.color(), DFS_COLOR))
        for node in adj_list[start]:
            if not visited[self.nodes.index(node)]:
                edge = self.find_edge(start, node)
                self.DFS_sequential.addAnimation(self.create_animation(edge, start.pen.color(), DFS_COLOR))
                self.DFS(node, visited, adj_list)

    def BFS(self, start, visited, adj_list):
        queue = [start]
        visited[self.nodes.index(start)] = 1
        self.BFS_sequential.addAnimation(self.create_animation(start, start.pen.color(), BFS_COLOR))
        while queue:
            s = queue.pop(0)
            for node in adj_list[s]:
                node_index = self.nodes.index(node)
                if not visited[node_index]:
                    edge = self.find_edge(s, node)
                    self.BFS_sequential.addAnimation(self.create_animation(edge, edge.pen().color(), BFS_COLOR))
                    self.BFS_sequential.addAnimation(self.create_animation(node, node.pen.color(), BFS_COLOR))
                    queue.append(node)
                    visited[node_index] = 1

    def create_animation(self, item, start_color, end_color):
        animation = QVariantAnimation()
        animation.DeletionPolicy(QVariantAnimation.DeleteWhenStopped)

        animation.valueChanged.connect(item.handle_valueChanged)
        animation.setDuration(1000)

        animation.setStartValue(start_color)
        animation.setEndValue(end_color)

        return animation
