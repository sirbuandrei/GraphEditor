from collections import defaultdict

from PyQt5.QtCore import pyqtSignal, QObject


class GraphModel(QObject):
    update = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.directed = False
        self.nodes = set()
        self.edges = {}

    def set_directed(self, is_directed: bool):
        self.directed = is_directed

    def add_node(self, node):
        self.nodes.add(node)

    def add_edge(self, from_node, to_node, weight):
        self.edges[(from_node, to_node)] = weight

        if not self.directed:
            self.edges[(to_node, from_node)] = weight

    def clear(self):
        self.nodes.clear()
        self.edges.clear()

    def graph_update(self):
        self.update.emit()
