import math

from PyQt5.QtCore import QPointF


class Connection:
    def __init__(self, node1, node2, length):
        self.node1 = node1
        self.node2 = node2
        self.length = length

    def update(self, dx, dy):
        d = math.sqrt(dx * dx + dy * dy)
        if d == 0:
            return

        diff = self.length - d
        percent = diff / d * 0.5
        offset_x = dx * percent
        offset_y = dy * percent

        # Move nodes toward ideal connection distance
        current_pos1 = self.node1.pos()
        current_pos2 = self.node2.pos()

        self.node1.setPos(current_pos1.x() - offset_x, current_pos1.y() - offset_y)
        self.node2.setPos(current_pos2.x() + offset_x, current_pos2.y() + offset_y)


class PhysicsEngine:
    SOFTENING_CONSTANT = 0.15
    G = 39.5
    dt = 0.017
    NODE_FIELD_RADIUS = 80

    def __init__(self, graph_view):
        self.graph_view = graph_view
        self._connections = set()

    def apply_physics(self):
        nodes = self.graph_view.get_nodes()
        edges = self.graph_view.get_edges()

        for node in nodes:
            if self.graph_view.get_gravity() and self.graph_view.get_force_mode():
                force = self._calculate_force(node)
                node.moveBy(force.x() * (self.dt ** 2),
                            force.y() * (self.dt ** 2))
                node.update()
            self._check_collision(node, nodes)

        if self.graph_view.get_force_mode():
            for connection in self._connections:
                node1_pos = connection.node1.pos()
                node2_pos = connection.node2.pos()

                dx, dy, angle = self._calculate_angle(node1_pos, node2_pos)
                connection.update(dx, dy)

        for edge in edges:
            edge.update_path()

    def update_connections(self):
        self._connections.clear()
        # for connection in self._connections:
        #     if connection.node1 == node_deleted or connection.node2 == node_deleted:
        #         print(f'Removing connection between {connection.node1.get_text()} and {connection.node2.get_text()}')
        #         #self._connections.remove(connection)

    def _check_collision(self, node, nodes):
        for other_node in nodes:
            if other_node is not node:

                dx, dy, alfa = self._calculate_angle(node.get_center(), other_node.get_center())
                dsq = math.sqrt(dx * dx + dy * dy)

                length = self.NODE_FIELD_RADIUS + node.get_radius()
                if dsq <= length:
                    if self.graph_view.get_gravity() and self._verify_connection(node, other_node):
                        self._connections.add(Connection(node, other_node, length))
                    else:
                        overlap = dsq - node.get_radius() - self.NODE_FIELD_RADIUS
                        node.moveBy(-0.5 * overlap * (node.x() - other_node.x()) / dsq,
                                    -0.5 * overlap * (node.y() - other_node.y()) / dsq)
                        other_node.moveBy(0.5 * overlap * (node.x() - other_node.x()) / dsq,
                                          0.5 * overlap * (node.y() - other_node.y()) / dsq)

    def _verify_connection(self, node1, node2):
        for connection in self._connections:
            if (connection.node1 == node1 and connection.node2 == node2) or (connection.node2 == node1 and connection.node1 == node2):
                return False
        return True

    def _calculate_force(self, node):
        dx, dy, alfa = self._calculate_angle(node, QPointF(self.graph_view.width() / 2, self.graph_view.height() / 2))
        dsq = math.sqrt(dx * dx + dy * dy)
        force = (dsq * math.sqrt(dsq + self.SOFTENING_CONSTANT)) / self.G

        force_x = float(force) * math.cos(alfa)
        force_y = float(force) * math.sin(alfa)

        return QPointF(force_x * abs(dx), force_y * abs(dy))

    def _calculate_angle(self, p1, p2):
        dy = p2.y() - p1.y()
        dx = p2.x() - p1.x()
        angle = math.atan2(dy, dx)

        return dx, dy, angle
