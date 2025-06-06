import datetime

from PyQt5.QtCore import QPointF, QTimer

from views.node import Node


def random_coord():
    ...


class GraphPresenter:
    def __init__(self, view, model):
        self.graph_view = view
        self.graph_model = model

        self.graph_model.update.connect(self.update_items)

    def update_items(self):
        model_nodes = self.graph_model.nodes
        current_nodes = self.graph_view.scene.items()

        print(model_nodes, current_nodes)

        node = Node("1", QPointF(100, 100))
        self.graph_view.scene.addItem(node)

        # if not model_nodes:
        #     for node in current_nodes:
        #         self.graph_view.scene.removeItem(node)
        #     return
        #
        # nodes_to_add = model_nodes - set(node.get_text() for node in current_nodes)
        # nodes_to_remove = current_nodes - set(node for node in current_nodes if node.get_text() in model_nodes)
        #
        # for node in nodes_to_remove:
        #     self.graph_view.scene.removeItem(node)
        #
        # for node_text in nodes_to_add:
        #     node = Node(node_text, QPointF(100, 100))
        #     self.graph_view.scene.addItem(node)

    def get_nodes(self):
        list_of_nodes = set()

        for item in self.graph_view.scene.items():
            if isinstance(item, Node):
                list_of_nodes.add(item)

        return list_of_nodes