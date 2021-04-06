#
from PyQt5.QtGui import QPen

from node import Node, Connection, Edge
from PyQt5.QtCore import QPointF, Qt
from PyQt5.QtWidgets import QGraphicsPathItem
from PyQt5.QtGui import QPainterPath
import numpy as np
import math, time
from collections import OrderedDict

# CONSTANTS
SOFTENING_CONSTANT = 0.15
G = 39.5
dt = 0.017
FRICTION = 0.77


class GraphEngine(object):

    def __init__(self, nodeParent):
        # TODO: nodeParent -> parent
        self.nodeParent = nodeParent
        self.nodeCount = None
        self.nodes = {}
        self.matrix = [[]]
        self.connections = []
        self.edges = []
        self.edge_ideal_length = 150
        self.node_radius = 30
        self.node_fieldRadius = 80
        self.graphData = ''
        self.gravity = True
        self.force_mode = False
        self.directed = False

    """

    """
    def receive_data(self, _text):
        if not self.check(_text):
            self.nodes = None
            return

        self.manipulate_data(_text)

    """
    
    """

    def check(self, _text):
        if not _text:
            return False

        graph_lines = _text.split('\n')
        for line in graph_lines:
            if len(line.split(' ')) > 3:
                return False

        return True

    """
    
    """

    def manipulate_data(self, _text):
        self.graphData = _text

        self.nodeCount = self.count_nodes()
        if self.nodeCount != len(self.matrix):
            self.matrix = [[0 for _ in range(self.nodeCount)] for __ in range(self.nodeCount)]

        graph_lines = list(filter(None, _text.split('\n')))
        for line in graph_lines:
            elements = line.split(' ')
            if len(elements) > 1:
                values = list(self.nodes.values())
                first = values.index(elements[0])
                second = values.index(elements[1])
                self.matrix[first][second] = \
                    self.matrix[second][first] = 1

        self.count_edges()

    """
    
    """

    def count_nodes(self):
        # TODO: change values and list to self
        values = list(self.nodes.values())
        keys = list(self.nodes.keys())

        nodes = []
        [nodes.extend(line.split(' ')) for line in self.graphData.split('\n')]
        final_nodes = list(OrderedDict.fromkeys(nodes))

        new_nodes = [i for i in final_nodes if i not in values]
        unused_nodes = [i for i in values if i not in final_nodes]

        for node_text in unused_nodes:
            node = keys[values.index(node_text)]
            self.nodeParent.scene.removeItem(node)
            del self.nodes[node]

        for node_txt in new_nodes:
            node = Node(node_txt, self)
            self.nodes[node] = node_txt
            self.nodeParent.scene.addItem(node)

        return len(final_nodes)

    """
    
    """

    def update_nodes(self):
        # self.gravity = True
        for node in list(self.nodes.keys()):
            if not node.pinned:
                node.force = self.forces(node)

                tempPos = node.pos()
                node.setPos(node.x() + node.force.x() * (dt ** 2),
                            node.y() + node.force.y() * (dt ** 2))
                node.oldPos = tempPos

                self.check_collision(node)

    """
    
    """

    def count_edges(self):
        if not self.directed: # PE DEASUPRA DIAG PRINC
            for i, line in enumerate(self.matrix):
                for j, col in enumerate(line):
                    if col == 1:
                        node1 = list(self.nodes.keys())[i]
                        node2 = list(self.nodes.keys())[j]

                        edge = Edge(node1, node2)
                        self.edges.append(edge)
                        self.nodeParent.scene.addItem(edge)

        else: # PE TOATA MATRICEA
            pass

    """

    """

    def update_edges(self):
        for i, line in enumerate(self.matrix):
            for j, col in enumerate(line):
                if col == 1:
                    node1 = list(self.nodes.keys())[i]
                    node2 = list(self.nodes.keys())[j]

                    dx, dy, angle = self.get_angle(node1, node2)
                    d = math.sqrt(dx * dx + dy * dy)
                    diff = self.edge_ideal_length - d
                    percent = diff / d / 2
                    offsetX = dx * percent
                    offsetY = dy * percent

                    node1.setPos(node1.x() - offsetX, node1.y() - offsetY)
                    node2.setPos(node2.x() + offsetX, node2.y() + offsetY)

                    # self.nodeParent.scene.addItem(Edge(node1, node2))

    def draw_edges(self):
        for edge in self.edges:
            path = edge.create_path(self.node_radius / 2)
            edge.setPath(path)

    """
    
    """

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

            node1.setPos(node1.x() - offsetX, node1.y() - offsetY)
            node2.setPos(node2.x() + offsetX, node2.y() + offsetY)

    """
    
    """

    def forces(self, node):
        # for node in list(self.nodes.keys()):
        #self.check_collision(node)
        if not node.isClicked:
            dx, dy, alfa = self.get_angle(node, QPointF(self.nodeParent.width() / 2,
                                                        self.nodeParent.height() / 2))
            dsq = math.sqrt(dx * dx + dy * dy)
            force = (dsq * math.sqrt(dsq + SOFTENING_CONSTANT)) / G * FRICTION

            force_x = float(force) * math.cos(alfa)  # - ((node.forceR.x()) if node.isColliding else 0)
            force_y = float(force) * math.sin(alfa)  # - ((node.forceR.y()) if node.isColliding else 0)

            return QPointF(force_x * abs(dx), force_y * abs(dy))
        return QPointF(0, 0)

    """
    
    """

    def check_collision(self, node):
        node.isColliding = False
        for other_node in list(self.nodes.keys()):
            if other_node is not node:
                dx, dy, alfa = self.get_angle(node.center(), other_node.center())
                dsq = math.sqrt(dx * dx + dy * dy)
                length = self.node_fieldRadius + self.node_radius
                if dsq <= length and not other_node in node.connectedTo:
                    node.connectedTo.append(other_node)
                    node.isColliding = True
                    self.connections.append(Connection(node, other_node, length))

    """
    
    """

    def get_angle(self, point1, point2):
        dy = point2.y() - point1.y()
        dx = point2.x() - point1.x()
        return dx, dy, math.atan2(dy, dx)

    def start_DFS(self, node):
        print(node)

    def start_BFS(self, node):
        print(node)
