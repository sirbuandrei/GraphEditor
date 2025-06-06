from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPen, QPainterPath
from PyQt5.QtWidgets import QGraphicsPathItem


class Edge(QGraphicsPathItem):
    def __init__(self, start_node, end_node, cost=None, directed=False):
        super().__init__()
        print(f"Creating edge between {start_node.get_text()} and {end_node.get_text()}")

        try:
            # Check if nodes exist
            print(f"Start node: {start_node}")
            print(f"End node: {end_node}")

            # Get positions with safety checks
            start_pos = start_node.pos()
            end_pos = end_node.pos()

            print(f"Start pos: {start_pos}")
            print(f"End pos: {end_pos}")

            # Create path
            path = QPainterPath(start_pos)
            path.lineTo(end_pos)

            print("Path created successfully")

            # Set path and pen
            self.setPath(path)
            self.setPen(QPen(Qt.white, 2, Qt.SolidLine))

            print("Edge created successfully")

        except Exception as e:
            print(f"Error in Edge.__init__: {e}")
            import traceback
            traceback.print_exc()