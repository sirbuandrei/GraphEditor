from PyQt5 import QtWidgets, QtCore
from PyQt5.QtWidgets import (QMessageBox, QDialog, QVBoxLayout, QHBoxLayout,
                             QLabel, QLineEdit, QDialogButtonBox)


class AlgorithmParametersDialog(QDialog):
    def __init__(self, params_list, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Algorithm Parameters")
        self.param_edits = {}

        main_layout = QVBoxLayout(self)
        form_layout = QVBoxLayout()  # To hold all parameter rows

        for param_name in params_list:
            row_layout = QHBoxLayout()
            label = QLabel(f"{param_name}:")
            edit = QLineEdit(self)
            self.param_edits[param_name] = edit
            row_layout.addWidget(label)
            row_layout.addWidget(edit)
            form_layout.addLayout(row_layout)

        main_layout.addLayout(form_layout)

        # OK and Cancel buttons
        button_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel, self)
        button_box.accepted.connect(self.accept)
        button_box.rejected.connect(self.reject)
        main_layout.addWidget(button_box)

        self.setLayout(main_layout)
        self.setMinimumWidth(300)  # Adjust as needed

    def get_param_values(self):
        param_values = {}
        for name, edit_widget in self.param_edits.items():
            param_values[name] = edit_widget.text()
        return param_values


class UserAlgorithmDialog(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.algorithm_path = None
        self.main_win = parent

        self.setWindowTitle("User Defined Algorithm")
        self.setMinimumSize(500, 400)

        # Main layout
        layout = QtWidgets.QVBoxLayout(self)

        # Code input area
        self.code_edit = QtWidgets.QTextEdit(self)
        self.code_edit.setPlaceholderText("Enter your Python algorithm here...")
        layout.addWidget(self.code_edit)

        # Button layout
        button_layout = QtWidgets.QHBoxLayout()

        self.execute_button = QtWidgets.QPushButton("Execute", self)
        self.execute_button.clicked.connect(self.run_code)
        button_layout.addWidget(self.execute_button)

        self.cancel_button = QtWidgets.QPushButton("Cancel", self)
        self.cancel_button.clicked.connect(self.reject)  # Or self.close()
        button_layout.addWidget(self.cancel_button)

        layout.addLayout(button_layout)
        self.setLayout(layout)

    def run_code(self):
        try:

            path, result = self.kruskal(self.main_win.view.engine.undirected_graph.edges,
                                        self.main_win.view.engine.undirected_graph.weights)
            code = self.get_code()
            # print(code)
            # # Create a namespace to capture the defined function
            namespace = {}
            exec(code, namespace)

            path, result = namespace['kruskal'](self.main_win.view.engine.undirected_graph.edges, self.main_win.view.engine.undirected_graph.weights)

            print("Traversed Path:")
            for step in path:
                print(step)

            print("\nOutput:")
            print(f"MST Edges: {result['mst_edges']}")
            print(f"Total Weight: {result['total_weight']}")

        except Exception as e:
            print(e)

    def kruskal(self, edges, weights):
        """
        Kruskal's algorithm for finding Minimum Spanning Tree

        Args:
            edges: defaultdict where keys are vertices and values are lists of adjacent vertices
            weights: Dictionary where keys are tuples (u, v) and values are edge weights

        Returns:
            tuple: (traversed_path, output)
                - traversed_path: List of steps showing the algorithm's progress
                - output: Dictionary containing MST edges, total weight, and final result
        """

        # Union-Find data structure
        class UnionFind:
            def __init__(self, vertices):
                self.parent = {v: v for v in vertices}
                self.rank = {v: 0 for v in vertices}

            def find(self, x):
                if self.parent[x] != x:
                    self.parent[x] = self.find(self.parent[x])  # Path compression
                return self.parent[x]

            def union(self, x, y):
                px, py = self.find(x), self.find(y)
                if px == py:
                    return False  # Already in same set (would create cycle)

                # Union by rank
                if self.rank[px] < self.rank[py]:
                    self.parent[px] = py
                elif self.rank[px] > self.rank[py]:
                    self.parent[py] = px
                else:
                    self.parent[py] = px
                    self.rank[px] += 1
                return True

        # Extract all vertices from the adjacency list
        vertices = set(edges.keys())

        # Create unique edges from the adjacency list and weights
        # Since the graph is undirected, we need to avoid duplicates
        unique_edges = set()
        for u in edges:
            for v in edges[u]:
                # Add edge in canonical form (smaller vertex first) to avoid duplicates
                edge = tuple(sorted([u, v]))
                unique_edges.add(edge)

        # Create list of edges with their weights for sorting
        edge_list = []
        for u, v in unique_edges:
            # Try both orientations since weights dict might have (u,v) or (v,u)
            if (u, v) in weights:
                weight = weights[(u, v)]
            elif (v, u) in weights:
                weight = weights[(v, u)]
            else:
                # This shouldn't happen if data is consistent
                continue

            edge_list.append((weight, u, v))

        # Sort edges by weight
        edge_list.sort()

        # Initialize Union-Find
        uf = UnionFind(vertices)

        # Track algorithm progress
        traversed_path = []
        mst_edges = []
        total_weight = 0

        traversed_path.append(
            f"Starting Kruskal's algorithm with {len(vertices)} vertices and {len(unique_edges)} unique edges")
        traversed_path.append(f"Vertices: {sorted(list(vertices))}")
        traversed_path.append(f"Sorted edges by weight: {[(weight, u, v) for weight, u, v in edge_list]}")

        # Process edges in order of increasing weight
        edges_added = 0
        for weight, u, v in edge_list:
            traversed_path.append(f"Considering edge ({u}, {v}) with weight {weight}")

            # Check if adding this edge would create a cycle
            if uf.union(u, v):
                # Edge accepted - doesn't create cycle
                mst_edges.append((u, v, weight))
                total_weight += weight
                edges_added += 1
                traversed_path.append(f"  ✓ Added edge ({u}, {v}) - No cycle created")
                traversed_path.append(f"  Current MST weight: {total_weight}")

                # Stop when we have n-1 edges (complete MST)
                if edges_added == len(vertices) - 1:
                    traversed_path.append(f"MST complete! Added {edges_added} edges for {len(vertices)} vertices")
                    break
            else:
                # Edge rejected - would create cycle
                traversed_path.append(f"  ✗ Rejected edge ({u}, {v}) - Would create cycle")

        # Prepare output
        output = {
            'mst_edges': mst_edges,
            'total_weight': total_weight,
            'num_vertices': len(vertices),
            'num_mst_edges': len(mst_edges),
            'vertices': sorted(list(vertices)),
            'is_connected': len(mst_edges) == len(vertices) - 1
        }

        traversed_path.append(f"Final result: MST with {len(mst_edges)} edges and total weight {total_weight}")

        return traversed_path, output

    # def execute_code(self):
    #     code_to_execute = self.code_edit.toPlainText()
    #     if not code_to_execute.strip():
    #         QMessageBox.warning(self, "Empty Code", "Please enter some Python code to execute.")
    #         return
    #
    #     try:
    #         compiled_code = compile(code_to_execute, '<string>', 'exec')
    #         print("Code compiled successfully.")
    #
    #         # --- Parameter Handling ---
    #         param_extraction_globals = {}  # For safety, separate from main exec
    #         param_extraction_locals = {}
    #         user_supplied_params = {}
    #         try:
    #             # Execute once to define functions and required_params
    #             exec(compiled_code, param_extraction_globals, param_extraction_locals)
    #             required_params_list = param_extraction_locals.get('required_params')
    #
    #             if isinstance(required_params_list, list) and required_params_list:
    #                 params_dialog = AlgorithmParametersDialog(required_params_list, self)
    #                 if params_dialog.exec_() == QtWidgets.QDialog.Accepted:
    #                     user_supplied_params = params_dialog.get_param_values()
    #                     print(f"User supplied parameters: {user_supplied_params}")
    #                 else:
    #                     QMessageBox.information(self, "Cancelled",
    #                                             "Algorithm execution cancelled due to parameter input cancellation.")
    #                     return  # Do not proceed, keep UserAlgorithmDialog open
    #         except Exception as param_exec_e:
    #             QMessageBox.critical(self, "Parameter Script Error",
    #                                  f"Error during parameter extraction or function definition phase: {param_exec_e}")
    #             return
    #         # --- End Parameter Handling ---
    #
    #         actual_graph_data = {}
    #         if self.graph_engine:
    #             nodes = [node.__repr__() for node in self.graph_engine.nodes]
    #             edges = [(edge.node1.__repr__(), edge.node2.__repr__(), edge.cost) for edge in self.graph_engine.edges]
    #
    #             adj_list_source = None
    #             if self.graph_engine.directed:
    #                 adj_list_source = self.graph_engine.directed_graph
    #             else:
    #                 adj_list_source = self.graph_engine.undirected_graph
    #
    #             adj = {}
    #             if adj_list_source:
    #                 adj = {node.__repr__(): [neighbor.__repr__() for neighbor in adj_list_source.edges[node]]
    #                        for node in adj_list_source.edges}
    #
    #             actual_graph_data = {
    #                 'nodes': nodes,
    #                 'edges': edges,
    #                 'adj': adj,
    #                 'is_directed': self.graph_engine.directed
    #             }
    #         else:
    #             # Fallback to placeholder if graph_engine is not provided
    #             QMessageBox.warning(self, "No Graph Data", "Graph engine not available. Using placeholder data.")
    #             actual_graph_data = {'nodes': [1, 2, 3], 'edges': [(1, 2), (2, 3)], 'adj': {1: [2], 2: [1, 3], 3: [2]},
    #                                  'is_directed': False}
    #
    #         # Prepare local variables for final exec context
    #         # Start with globals from the first pass (which includes function definitions from user script)
    #         # and then add/override with specific context variables.
    #         final_exec_globals = param_extraction_globals.copy()
    #         final_exec_locals = {
    #             'graph': actual_graph_data,
    #             'output_path': None
    #         }
    #         final_exec_locals.update(user_supplied_params)  # Add user-supplied params
    #
    #         # Execute the user's code (main logic part, expecting output_path)
    #         try:
    #             # The user's script might call functions defined within it,
    #             # so they need to be in the execution scope.
    #             # We pass final_exec_globals as both globals and locals to allow function calls
    #             # and variable assignments in a somewhat "script-like" manner.
    #             # Or, more controlled: exec(compiled_code, final_exec_globals, final_exec_locals)
    #             # and expect user to use global functions or assign output_path in final_exec_locals.
    #             # For now, let's assume the user script might rely on functions being callable
    #             # and output_path being set in the local scope.
    #
    #             # Re-executing the whole script. If it's structured with a main call
    #             # that uses the params, this is fine. If it's just flat statements,
    #             # the definitions will re-run but that's usually harmless.
    #             # The key is that `required_params` is read on first pass, and now the
    #             # parameters are injected for the second pass which should use them.
    #             exec(compiled_code, final_exec_globals, final_exec_locals)
    #             user_output_path = final_exec_locals.get('output_path')
    #
    #         except Exception as exec_e:
    #             QMessageBox.critical(self, "Execution Error", f"Error during final code execution: {exec_e}")
    #             return  # Do not accept dialog
    #
    #         # Validate output_path (retrieved from final_exec_locals)
    #         if user_output_path is None:
    #             QMessageBox.warning(self, "Output Not Set", "The script did not set 'output_path'.")
    #             return  # Do not accept dialog
    #
    #         if not isinstance(user_output_path, list):
    #             QMessageBox.warning(self, "Invalid Output Type",
    #                                 f"'output_path' must be a list, but got {type(user_output_path)}.")
    #             return  # Do not accept dialog
    #
    #         # Validate path elements (basic check: list of node reprs or list of tuples of node reprs)
    #         valid_path = True
    #         if not user_output_path:  # Empty list is a valid path (no path)
    #             pass
    #         elif isinstance(user_output_path[0], str):  # Path of node names (reprs)
    #             if not all(isinstance(node_name, str) for node_name in user_output_path):
    #                 valid_path = False
    #         elif isinstance(user_output_path[0], tuple):  # Path of edges (tuples of node names)
    #             if not all(isinstance(edge, tuple) and len(edge) == 2 and
    #                        isinstance(edge[0], str) and isinstance(edge[1], str)
    #                        for edge in user_output_path):
    #                 valid_path = False
    #         else:  # Neither list of str nor list of tuples of str
    #             valid_path = False
    #
    #         if not valid_path:
    #             QMessageBox.warning(self, "Invalid Path Format",
    #                                 "'output_path' must be a list of node names (strings) or a list of edges (tuples of two node names as strings).")
    #             return  # Do not accept dialog
    #
    #         self.algorithm_path = user_output_path
    #         print(f"User script set output_path to: {self.algorithm_path}")
    #         self.accept()
    #
    #     except (SyntaxError, Exception) as e:  # Covers compilation errors primarily
    #         QMessageBox.critical(self, "Compilation or Setup Error", f"Error: {e}\nPlease correct it and try again.")
    #         # Dialog remains open for user to correct the code

    def get_code(self):
        return self.code_edit.toPlainText()

    def get_algorithm_path(self):
        return self.algorithm_path


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    dialog = UserAlgorithmDialog()

    # To test, we can check if the dialog opens and if we can retrieve code
    if dialog.exec_() == QtWidgets.QDialog.Accepted:
        print("Dialog accepted, code was:")
        print(dialog.get_code())
    else:
        print("Dialog cancelled.")

    sys.exit(app.exec_())