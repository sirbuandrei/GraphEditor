from collections import defaultdict

from PyQt5.QtCore import pyqtSignal, QObject


class GraphModel(QObject):
    update_scene_items = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.directed = False
        self.current_radius = 15
        self.nodes = set()
        self.edges = {}

    def set_radius(self, radius):
        self.current_radius = radius

    def get_radius(self):
        return self.current_radius

    def set_directed(self, is_directed: bool):
        self.directed = is_directed

    def get_directed(self):
        return self.directed

    def get_edges(self):
        return self.edges

    def get_nodes(self):
        return self.nodes

    def add_node(self, node):
        self.nodes.add(node)

    def add_edge(self, from_node, to_node, weight):
        self.edges[(from_node, to_node)] = weight

    def clear(self):
        self.nodes.clear()
        self.edges.clear()

    def graph_update(self):
        self.update_scene_items.emit()
