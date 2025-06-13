from PyQt5.QtCore import QVariantAnimation, QEasingCurve, QSequentialAnimationGroup, QPropertyAnimation
from PyQt5.QtGui import QColor
from PyQt5.QtWidgets import QFileDialog, QApplication

from styles import Styles
from utils.algorithms_manager import AlgorithmsManager
from views.custom_algorithm_dialog import CustomAlgorithmDialog
from views.user_input_dialog import UserInputDialog


class Coordinator:
    def __init__(self, view1, view2, model):
        self.config_page = view1
        self.graph_view = view2
        self.graph_model = model

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

        self.config_page.pushButton_force_mode.click()
        self.graph_view.set_force_mode(True)

        self.config_page.pushButton_undirected.click()
        self.config_page.pushButton_directed.setStyleSheet(Styles.btn_directed_undirected_non_clicked)
        self.config_page.pushButton_undirected.setStyleSheet(Styles.btn_directed_undirected_clicked)

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
        algorithm_input = self.config_page.get_algorithm_input()
        algorithm_type = self.config_page.get_algorithm_type()

        steps, correct_output = self.algorithm_manager.run_algorithm(algorithm_type, self.graph_model.get_edges(),
                                                      self.graph_model.get_directed(), algorithm_input)

        print(steps)
        print(correct_output)
        # input_dialog = UserInputDialog(f"Enter your response for the {algorithm_type} algorithm: ")
        # if input_dialog.exec_():
        #     user_response = input_dialog.getText()
        #
        #     if user_response == correct_output:
        #         self.graph_view.set_text("Correct", QColor("#00ff66"))
        #     else:
        #         self.graph_view.set_text("The actual path is: " + correct_output,  QColor("#ff4444"))
        #
        #     self.create_animation_sequence(steps)

    def create_animation_sequence(self, steps):
        """Create animations based on yield command sequence"""
        self._animation_group.clear()

        nodes = {int(node.get_text()): node for node in self.graph_view.get_nodes()}
        edges = {}
        for edge in self.graph_view.get_edges():
            from_node, to_node = edge.get_tuple()
            edges[(int(from_node), int(to_node))] = edge

            if not self.graph_model.get_directed():
                edges[(int(to_node), int(from_node))] = edge

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
        custom_algorithm_dialog = CustomAlgorithmDialog()
        custom_algorithm_dialog.exec()

        algorithm_code = custom_algorithm_dialog.get_full_code()
        algorithm_name = custom_algorithm_dialog.get_algorithm_name()

        print(algorithm_code)

        try:
            namespace = {}
            exec(algorithm_code, namespace)
            custom_func = namespace['custom_algorithm']
        except Exception as e:
            print(f"Compilation Error: {str(e)}")

        self.config_page.add_custom_algorithm(algorithm_name)
        self.algorithm_manager.add_algorithm(algorithm_name, custom_func)

    def save_graph(self):
        option = QFileDialog.Options()
        option |= QFileDialog.DontUseNativeDialog
        file = QFileDialog.getSaveFileName(QApplication.activeWindow(), 'Save File',
                                           'graph.png', 'All Files (*)', options=option)
        if file[0]:
            final_file = file[0].split('.')
            pixmap = self.graph_view.grab()
            pixmap.save(file[0], final_file[1].upper(), 0)