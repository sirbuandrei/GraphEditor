import types

from PyQt5.QtCore import QVariantAnimation, QEasingCurve, QSequentialAnimationGroup
from PyQt5.QtGui import QColor
from PyQt5.QtWidgets import QFileDialog, QApplication
from firebase_admin import db

from utils.styles import Styles
from utils.algorithms_manager import AlgorithmsManager
from views.items.custom_algorithm_dialog import CustomAlgorithmDialog
from views.items.user_input_dialog import UserInputDialog

EDITOR_DEFAULT_TEXT = """def your_algorithm(graph, algorithm_input):
    \"\"\" 
    The name of your algorithm will be taken form the function name,
    so please rename the function
    
    The parameters passed are an adjacent list of the current graph,
    and a str of the user input
    
    graph: dict
    algorithm_input: str
    
    The code must return a list and a str
    The animation steps must return a list of steps in dictionary format,
    of the items that want to be animated.
    eg: 
    animation_steps.append({"item": '1', "color": "orange"})
    animation_steps.append({"item": '2', "color": "yellow"})
    This will animate node with string '1' from it's current color to orange,
    then will animate node with string '2' from it's current color to yellow,
    if they exist.
    
    The adjacent list node are in str format, and the weights in int
    eg: {'1': [('2', 1), ('3': 2)], '2': [('4', 3)]}
    This means that node '1' has an edge of weight 1 to the node '2',
    that node '1' has an edge of weight 2 to the node '3', and
    that node '2' has an edge of weight 3 to the node '4'
    
    Also the adjacent list takes into consideration if the graph is directed or
    undirected.
    
    The output is the string that is compared with the user input before
    the animation stars. If the user inputs the exact string is rewarded a point.
    Otherwise there will be a penalty of one point.
    \"\"\"
    return animation_steps, output"""


class Coordinator:
    def __init__(self, view1, view2, model):
        self.config_page = view1
        self.graph_view = view2
        self.graph_model = model

        self.user_id = None
        self.algorithm_manager = AlgorithmsManager()
        self._animation_group = QSequentialAnimationGroup()

        self.config_page.force_mode_toggled.connect(self.toggle_force_mode)
        self.config_page.radius_changed.connect(self.change_radius)
        self.config_page.directed.connect(self.toggle_directed)
        self.config_page.undirected.connect(self.toggle_undirected)
        self.config_page.run_algorithm.connect(self.run_algorithm)
        self.config_page.create_custom_algorithm.connect(self.create_custom_algorithm)
        self.config_page.save_graph.connect(self.save_graph)
        self.config_page.clear_algorithm.connect(self.clear_algorithm)
        self.config_page.edit_algorithm.connect(self.edit_algorithm)

        self.graph_view.space_pressed.connect(self.pause_animation)

        self.config_page.pushButton_force_mode.click()
        self.graph_view.set_force_mode(True)

        self.config_page.pushButton_undirected.click()
        self.config_page.pushButton_directed.setStyleSheet(Styles.btn_directed_undirected_non_clicked)
        self.config_page.pushButton_undirected.setStyleSheet(Styles.btn_directed_undirected_clicked)

    def set_current_user(self, user_id):
        self.user_id = user_id

    def toggle_force_mode(self, is_enabled):
        self.graph_view.set_force_mode(is_enabled)

    def change_radius(self, value):
        nodes = self.graph_view.get_nodes()
        for node in nodes:
            node.set_radius(value)
        self.graph_model.set_radius(value)

    def toggle_directed(self):
        self.config_page.pushButton_directed.setStyleSheet(Styles.btn_directed_undirected_clicked)
        self.config_page.pushButton_undirected.setStyleSheet(Styles.btn_directed_undirected_non_clicked)
        self.graph_view.change_directed(True)
        self.graph_model.set_directed(True)

    def toggle_undirected(self):
        self.config_page.pushButton_directed.setStyleSheet(Styles.btn_directed_undirected_non_clicked)
        self.config_page.pushButton_undirected.setStyleSheet(Styles.btn_directed_undirected_clicked)
        self.graph_view.change_directed(False)
        self.graph_model.set_directed(False)

    def run_algorithm(self):
        if not self.graph_model.get_edges():
            return

        algorithm_input = self.config_page.get_algorithm_input()
        algorithm_type = self.config_page.get_algorithm_type()

        if not algorithm_input:
            return

        try:
            steps, correct_output = self.algorithm_manager.run_algorithm(algorithm_type, self.graph_model.get_edges(),
                                                              self.graph_model.get_directed(), algorithm_input)

            input_dialog = UserInputDialog(f"Enter your response for the {algorithm_type} algorithm: ")
            if input_dialog.exec_():
                user_response = input_dialog.getText()

                if user_response == correct_output:
                    self.graph_view.set_text("Correct", QColor("#00ff66"))
                    self.reward_point()
                else:
                    self.graph_view.set_text("The actual path is: " + correct_output,  QColor("#ff4444"))
                    self.subtract_point()

                self.create_animation_sequence(steps)
        except Exception as e:
            print(str(e))

    def reward_point(self):
        try:
            ref = db.reference(f'leaderboard/{self.user_id}')
            data = ref.get()

            if data and 'points' in data:
                new_points = data['points'] + 1
            else:
                new_points = 1

            ref.set({'points': new_points})
        except Exception as e:
            print(str(e))

    def subtract_point(self):
        try:
            ref = db.reference(f'leaderboard/{self.user_id}')
            data = ref.get()

            if data and 'points' in data:
                new_points = max(0, data['points'] - 1)
            else:
                new_points = 0

            ref.set({'points': new_points})
        except Exception as e:
            print(str(e))

    def create_animation_sequence(self, steps):
        """Create animations based on yield command sequence"""
        self._animation_group.clear()

        nodes = {node.get_text(): node for node in self.graph_view.get_nodes()}
        edges = {}
        for edge in self.graph_view.get_edges():
            from_node, to_node = edge.get_tuple()
            edges[(from_node, to_node)] = edge

            if not self.graph_model.get_directed():
                edges[(to_node, from_node)] = edge

        for step in steps:
            item = step["item"]
            color = step["color"]

            if item in nodes:
                animation = self.create_animation(nodes[item], color)
            else:
                edge_item = self.find_edge_item(item, edges)
                animation = self.create_animation(edge_item, color)

            self._animation_group.addAnimation(animation)

        self._animation_group.start()

    def find_edge_item(self, edge_tuple, edges):
        from_node, to_node = edge_tuple

        if (from_node, to_node) in edges:
            return edges[(from_node, to_node)]
        elif (to_node, from_node) in edges:
            return edges[(to_node, from_node)]

        return None

    def create_animation(self, item, color):
        animation = QVariantAnimation()
        animation.DeletionPolicy(QVariantAnimation.DeleteWhenStopped)
        animation.setEasingCurve(QEasingCurve.InOutQuad)

        animation.valueChanged.connect(item.color_change)
        animation.setDuration(1000)

        animation.setStartValue(item.get_color())
        animation.setEndValue(QColor(color))

        return animation

    def clear_algorithm(self):
        self.config_page.clear_algorithm_input()
        self.graph_view.clear_text()

        for node in self.graph_view.get_nodes():
            node.color_change(QColor("white"))

        for edge in self.graph_view.get_edges():
            edge.color_change(QColor("white"))

        self._animation_group.clear()

    def create_custom_algorithm(self):
        custom_algorithm_dialog = CustomAlgorithmDialog(EDITOR_DEFAULT_TEXT)
        if custom_algorithm_dialog.exec_():
            algorithm_code = custom_algorithm_dialog.get_full_code()

            try:
                namespace = {}
                exec(algorithm_code, namespace)
                custom_func = next(
                    (v for k, v in namespace.items() if isinstance(v, types.FunctionType) and not k.startswith('__')),
                    None
                )

                self.config_page.add_custom_algorithm(custom_func.__name__)
                self.algorithm_manager.add_algorithm(custom_func.__name__, custom_func)
            except Exception as e:
                print(f"Compilation Error: {str(e)}")

    def edit_algorithm(self):
        algorithm_type = self.config_page.get_algorithm_type()
        algorithm, func_name  = self.algorithm_manager.get_algorithm(algorithm_type)

        dialog = CustomAlgorithmDialog(algorithm)
        if dialog.exec_():
            try:
                new_code = dialog.get_full_code()

                namespace = {}
                exec(new_code, namespace)
                custom_func = namespace[func_name]

                self.algorithm_manager.set_code(algorithm_type, custom_func)
            except Exception as e:
                print(f"Compilation Error: {str(e)}")

    def save_graph(self):
        option = QFileDialog.Options()
        option |= QFileDialog.DontUseNativeDialog
        file = QFileDialog.getSaveFileName(QApplication.activeWindow(), 'Save File',
                                           'graph.png', 'All Files (*)', options=option)
        if file[0]:
            final_file = file[0].split('.')
            pixmap = self.graph_view.grab()
            pixmap.save(file[0], final_file[1].upper(), 0)

    def pause_animation(self):
        if self._animation_group.state() == 2:
            self._animation_group.pause()
        elif self._animation_group.state() == 1:
            self._animation_group.resume()