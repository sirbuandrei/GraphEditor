import math
from dataclasses import dataclass

from PyQt5.QtCore import QPointF

from views.items.node import LightweightNode


@dataclass(repr=True, eq=False)
class Connection:
    __slots__ = ('node1', 'node2', 'length')

    node1: LightweightNode
    node2: LightweightNode
    length: float

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Connection):
            return NotImplemented
        return (
            (self.node1 is other.node1 and self.node2 is other.node2) or
            (self.node1 is other.node2 and self.node2 is other.node1)
        ) and self.length == other.length

    def __hash__(self) -> int:
        node_ids_hash = hash(frozenset({id(self.node1), id(self.node2)}))
        return node_ids_hash ^ hash(self.length)

    def update(self, dx: float, dy: float) -> None:
        d = math.sqrt(dx * dx + dy * dy)
        if d == 0:
            return

        diff: float = self.length - d
        percent: float = diff / d * 0.5
        offset_x: float = dx * percent
        offset_y: float = dy * percent

        current_pos1 = self.node1.pos()
        current_pos2 = self.node2.pos()

        self.node1.setPos(current_pos1.x() - offset_x, current_pos1.y() - offset_y)
        self.node2.setPos(current_pos2.x() + offset_x, current_pos2.y() + offset_y)


class PhysicsEngine:
    SOFTENING_CONSTANT: float = 0.15
    G: float = 39.5
    dt: float = 0.027
    NODE_FIELD_RADIUS: int = 80

    def __init__(self, graph_view):
        self.graph_view = graph_view
        self.connections = set()

    def apply_physics(self) -> None:
        nodes = self.graph_view.get_nodes()
        edges = self.graph_view.get_edges()

        for node in nodes:
            if self.graph_view.get_gravity() and self.graph_view.get_force_mode():
                force_to_center = self._calculate_force_to_center(node)
                node.moveBy(force_to_center.x() * self.dt,
                            force_to_center.y() * self.dt)
                node.update()

            self._check_collision(node, nodes)

        # Apply spring forces from connections if force mode is enabled
        if self.graph_view.get_force_mode():
            for connection in self.connections:
                node1_pos = connection.node1.pos()
                node2_pos = connection.node2.pos()
                # Calculate vector from node1 to node2
                dx, dy, _ = self._calculate_vector_and_angle(node1_pos, node2_pos)  # angle not needed here
                connection.update(dx, dy)  # Applies spring force adjustment to node positions

        # Update visual paths for all edges in the view
        # for edge in edges:
        #     edge.update_path()

    def update_connections(self) -> None:
        """Clears all current connections. Connections will be re-established during physics simulation."""
        self.connections.clear()

    def _check_collision(self, node: LightweightNode, all_nodes: set) -> None:
        """Checks for collision between 'node' and other nodes in 'all_nodes'.
           Adds connections if nodes are within NODE_FIELD_RADIUS and gravity is on.
           Resolves direct overlaps otherwise.
        """
        for other_node in all_nodes:
            if other_node is node:  # Skip self-collision check
                continue

            dx, dy, _ = self._calculate_vector_and_angle(node.get_center(), other_node.get_center())
            distance = math.sqrt(dx * dx + dy * dy)

            if distance == 0:  # Avoid division by zero if nodes are somehow at the exact same spot
                continue

            connection_radius = self.NODE_FIELD_RADIUS + node.get_radius()  # node.radius from property

            if distance <= connection_radius:
                if self.graph_view.get_gravity() and self._verify_connection(node, other_node):
                    self.connections.add(Connection(node, other_node, connection_radius))
                else:
                    overlap = distance - node.get_radius() - self.NODE_FIELD_RADIUS
                    node.moveBy(-0.5 * overlap * (node.x() - other_node.x()) / distance,
                                -0.5 * overlap * (node.y() - other_node.y()) / distance)
                    other_node.moveBy(0.5 * overlap * (node.x() - other_node.x()) / distance,
                                      0.5 * overlap * (node.y() - other_node.y()) / distance)

                physical_radii_sum = node.get_radius() + other_node.get_radius()
                if distance < physical_radii_sum:  # Actual physical overlap
                    overlap_amount = physical_radii_sum - distance
                    move_x = 0.5 * overlap_amount * (dx / distance)
                    move_y = 0.5 * overlap_amount * (dy / distance)

                    node.moveBy(move_x, move_y)  # Move 'node' away from 'other_node'
                    other_node.moveBy(-move_x, -move_y)  # Move 'other_node' away from 'node'
                    node.update()
                    other_node.update()

    def _verify_connection(self, node1: LightweightNode, node2: LightweightNode) -> bool:
        """Checks if a connection between node1 and node2 already exists in self._connections.
           Returns True if NO connection exists (i.e., it's okay to add one), False otherwise.
        """
        for conn in self.connections:
            if (conn.node1 is node1 and conn.node2 is node2) or \
                    (conn.node1 is node2 and conn.node2 is node1):
                return False
        return True

    def _calculate_force_to_center(self, node: LightweightNode) -> QPointF:
        """Calculates a gravitational-like force pulling the node towards the center of the view."""
        # Calculate vector from node to view center
        view_center = QPointF(self.graph_view.width() / 2, self.graph_view.height() / 2)
        dx, dy, angle = self._calculate_vector_and_angle(node.pos(),
                                                         view_center)  # Use node.pos() for its current position

        distance_sq = dx * dx + dy * dy
        if distance_sq == 0:
            return QPointF(0, 0)
        distance = math.sqrt(distance_sq)

        # Force magnitude (custom law from original code)
        # Note: dsq in original was distance, not distance_sq. Renaming for clarity.
        force_magnitude = (distance * math.sqrt(distance + self.SOFTENING_CONSTANT)) / self.G
        if math.isnan(force_magnitude): force_magnitude = 0  # Avoid NaN issues if distance is very small

        # Force components
        # Original code had abs(dx) and abs(dy) which seems unusual for directional force.
        # A standard force vector would be: Fx = magnitude * cos(angle), Fy = magnitude * sin(angle)
        # Or: Fx = magnitude * (dx / distance), Fy = magnitude * (dy / distance)
        # Preserving original scaled by normalized vector components:
        force_x = force_magnitude * (dx / distance if distance != 0 else 0)
        force_y = force_magnitude * (dy / distance if distance != 0 else 0)

        return QPointF(force_x, force_y)

    def _calculate_vector_and_angle(self, p1: QPointF, p2: QPointF) -> (float, float, float):
        """Calculates dx, dy, and angle from p1 to p2."""
        dy = p2.y() - p1.y()
        dx = p2.x() - p1.x()
        angle = math.atan2(dy, dx)

        return dx, dy, angle

