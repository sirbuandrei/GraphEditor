from PyQt5.QtCore import pyqtSignal, QObject


class GraphModel(QObject):
    update_scene_items = pyqtSignal()

    def __init__(self):
        super().__init__()
        self._directed = False
        self._radius = 15
        self._nodes = set()
        self._edges = {}

    def get_radius(self):
        return self._radius

    def set_radius(self, radius):
        self._radius = radius

    def set_directed(self, is_directed: bool):
        self._directed = is_directed

    def get_directed(self):
        return self._directed

    def get_edges(self):
        return self._edges

    def get_nodes(self):
        return self._nodes

    def add_node(self, node):
        self._nodes.add(node)

    def add_edge(self, from_node, to_node, weight):
        self._edges[(from_node, to_node)] = weight

    def clear(self):
        self._nodes.clear()
        self._edges.clear()

    def graph_update(self):
        self.update_scene_items.emit()
