import random

from PyQt5.QtGui import QPainterPath, QPen

from PyQt5.QtCore import QPointF, QRectF, Qt, QObject

from views.edge import Edge
from views.node import LightweightNode


class GraphPresenter(QObject):
    def __init__(self, view, model):
        super().__init__()
        self.graph_view = view
        self.graph_model = model

        self.graph_model.update_scene.connect(self.update_items)

    def update_items(self):
        model_nodes = self.graph_model.nodes
        model_edges = self.graph_model.edges

        current_nodes = self.get_nodes()
        current_edges = self.get_edges()

        print(f"=== Update Items ===")
        print(f"Model nodes: {model_nodes}")
        print(f"Model edges: {self.graph_model.edges}")

        if not current_nodes:
            self.add_nodes(model_nodes)
            self.add_edges(model_edges)
        elif not model_nodes:
            self.remove_nodes(current_nodes)
        else:
            self.update_nodes(model_nodes, current_nodes)

        #self.update_edges(model_edges, current_edges)

    def update_nodes(self, model_nodes, current_nodes):
        nodes_to_add = model_nodes - set(node.get_text() for node in current_nodes)
        nodes_to_remove = current_nodes - set(node for node in current_nodes if node.get_text() in model_nodes)

        self.add_nodes(nodes_to_add)
        self.remove_nodes(nodes_to_remove)

    def update_edges(self):
        print("Updating edges ...")

    def add_nodes(self, nodes_to_add):
        for node_text in nodes_to_add:
            position = get_random_perimeter_position(
                self.graph_view.scene.sceneRect(),
                node_radius=15
            )
            node = LightweightNode(node_text, position)
            self.graph_view.scene.addItem(node)


    def remove_nodes(self, nodes_to_remove):
        for node in nodes_to_remove:
            self.graph_view.scene.removeItem(node)

    def get_nodes(self):
        list_of_nodes = set()

        for item in self.graph_view.scene.items():
            if isinstance(item, LightweightNode):
                list_of_nodes.add(item)

        return list_of_nodes

    def find_node_by_text(self, text):
        for node in self.get_nodes():
            if node.get_text() == text:
                return node
        return None

    def add_edges(self, edges_to_add):
        for edge_key, cost in edges_to_add.items():
            start_text, end_text = edge_key
            print(f"Adding edge: {start_text} -> {end_text} (cost: {cost})")

            start_node = self.find_node_by_text(start_text)
            end_node = self.find_node_by_text(end_text)

            if start_node and end_node:
                edge = Edge(
                    start_node=start_node,
                    end_node=end_node,
                    cost=cost,
                    directed=self.graph_model.directed
                )
                self.graph_view.scene.addItem(edge)
            else:
                print(f"Could not find nodes for edge {start_text} -> {end_text}")

    def get_edges(self):
        list_of_edges = set()

        for item in self.graph_view.scene.items():
            if isinstance(item, Edge):
                list_of_edges.add(item)

        return list_of_edges


def get_random_perimeter_position(scene_rect, node_radius=15):
    if not isinstance(scene_rect, QRectF):
        raise ValueError("scene_rect must be a QRectF")

    # Calculate the safe boundaries (accounting for node radius)
    left = scene_rect.left() + node_radius
    right = scene_rect.right() - node_radius
    top = scene_rect.top() + node_radius
    bottom = scene_rect.bottom() - node_radius

    # Calculate the perimeter lengths for each edge
    width = right - left
    height = bottom - top

    if width <= 0 or height <= 0:
        return scene_rect.center()

    # Total perimeter length
    total_perimeter = 2 * width + 2 * height

    # Choose a random point along the perimeter
    random_distance = random.uniform(0, total_perimeter)

    if random_distance <= width:
        # TOP EDGE
        x = left + random_distance
        y = top
        return QPointF(x, y)

    elif random_distance <= width + height:
        # RIGHT EDGE
        x = right
        y = top + (random_distance - width)
        return QPointF(x, y)

    elif random_distance <= 2 * width + height:
        # BOTTOM EDGE
        x = right - (random_distance - width - height)
        y = bottom
        return QPointF(x, y)

    else:
        # LEFT EDGE
        x = left
        y = bottom - (random_distance - 2 * width - height)
        return QPointF(x, y)