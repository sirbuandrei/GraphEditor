"""Fisierul contine clasele corespunzaotare engin-ului aplicatiei"""

from node import Node, Connection, Edge

from PyQt5.QtCore import (QPointF, QSequentialAnimationGroup, QVariantAnimation)
from PyQt5.QtWidgets import QLineEdit
from PyQt5.QtGui import QColor

import numpy as np
import math
from collections import defaultdict

# Constante
SOFTENING_CONSTANT = 0.15
G = 39.5
dt = 0.017

# Culorile animatilor
DFS_COLOR = QColor('yellow')
BFS_COLOR = QColor('orange')
DIJKSTRA_COLOR = QColor('red')


class Graph:
    """Contine informatiile despre un graf

    Informatiile grafului sunt lista de adiacenta, costurile muchiilor
    si orientarea grafului. Acestea se for folosi mai departe pentru
    aplicarea algorimtilor (DFS, BFS, DIJKSTRA)

    Atribute
    ---------
    edges: dict
        lista de adiacenta a grafului
    weights: dict
        lista costurilor muchiilor
    directed:
        orientarea grafului

    Metode
    ------
    __delitem__(key)
        sterge un nod
    add_edge(from_node, to_node, weight)
        adauga o muchie
    remove_edge(from_node, to_node)
        sterge o muchie
    clear()
        sterge toate datele
    """

    def __init__(self, directed):
        self.edges = defaultdict(list)
        self.weights = {}
        self.directed = directed

    def __delitem__(self, key):
        """Elimina din dictionarul de muchii a unui nod"""

        del self.edges[key]

    def add_edge(self, from_node, to_node, weight):
        """Adauga o muchie intre 2 noduri cu un cost

        Daca graful este neorientat se va mai adauga o muchie
        si de la to_node la from_node cu costul respectiv

        Parametrii
        ----------
        from_node : Node
            primul nod al muchiei
        to_node : Node
            al doilea nod al muchiei
        weight : int
            costul muchiei
        """

        self.edges[from_node].append(to_node)
        self.weights[(from_node, to_node)] = weight

        if not self.directed:
            self.edges[to_node].append(from_node)
            self.weights[(to_node, from_node)] = weight

    def remove_edge(self, from_node, to_node):
        """Sterge muchia dintre 2 noduri si costul ei

        Daca graful este neorientat se va sterge si muchia de
        la to_node la from_node, inclusiv costul acesteia

        Parametrii
        ----------
        from_node : Node
            primul nod al muchiei
        to_node : Node
            al doilea nod al muchiei
        """

        self.edges[from_node].remove(to_node)
        del self.weights[(from_node, to_node)]

        if not self.directed:
            self.edges[to_node].remove(from_node)
            del self.weights[(to_node, from_node)]

    def clear(self):
        """Sterge toate datele grafului"""

        self.edges.clear()
        self.weights.clear()


class GraphEngine(object):
    """Engiun-ul grafului

    Toate nodurile sunt atrase spre centrul sceneului de o forta de gravitatie, fiecare avand un camp
    de intercatiune propriu. Daca acest camp se intersecteaza cu un alt nod, ele for forma o
    conexiune si vor actiona unul in funtie de celalalt. Astfel se o obtine o aseazare centrata
    si imprastiata a nodurilor in scene.
    Exsita 2 liste de adiacenta, una pentru cazul unui graf orientat si una pentru cazul unui graf neorientat.

    Artibute
    --------
    view : QGraphicsView
        viewport-ul grafului
    node : list
        lista de noduri
    edges : list
        lista de muchii
    connections : list
        lista de conexiuni formate de noduri
    directed_graph : Graph
        graful orientat formate de datele primite
    undirected_graph : Graph
        graful neorientat formate de datele primite
    node_fieldRadius : int
        raza campului de interaciune a nodurilor
    label_node_count : QLabel
        labelul care contine numarul de noduri
    DFS_sequential : QSequentialAnimationGroup
        grupul de animatii in serie dupa efectuarea algorimului DFS
    BFS_sequential : QSequentialAnimationGroup
        grupul de animatii in serie dupa efectuarea algorimului BFS
    DIJKSTRA_sequential : QSequentialAnimationGroup
        grupul de animatii in serie dupa efectuarea algorimului DIJKSTRA
    sequential : QSequentialAnimationGroup
        grupul de animatii in serie responsabil de celelate 3 tipuri de aniamtii
    gravity : bool
    force_mode : bool
    directed :  bool
        orientarea grafului

    Metode
    ------
    receive_data(graph_data)
        Primeste datele grafului
    manipulate_data(graph_data)
        maniplueaza datele grafului
    add_remove_nodes(nodes)
        adauga sau sterge noduri
    add_remove_edges(edges)
        adauga sau sterge muchii
    update_nodes()
        actualizeaza pozitia nodurilor
    draw_edges()
        randeaza muchia dintre 2 noduri
    update_connections()
        actualizeaza pozitile nodurilor in funtie de conexiuni
    forces(node)
        calculeaza forta de gravitatie
    check_collision(node)
        actualizeaza conexiunile intre noduri
    get_angle(point1, point2)
        calculeaza distantele si ungiul dintre 2 pucnte
    find_edge(node1, node2)
        cauta o muchie intre 2 noduri
    remove_all_connections()
        sterge toate conexiunle
    start_animations(text_DFS, text_BFS, text_DIJKSTRA_src, text_DIJKSTRA_end)
        incepe animatiile alese
    DFS(start, visited, graph)
        algoritmul de DFS
    BFS(start, visited, graph)
        algoritmul de BFS
    DIJKSTRA(initial, end, graph)
        algorimtul DIJKSTRA
    create_animation(item, start_color, end_color)
        creaza o animatie a unui item
    """

    def __init__(self, view):
        self.view = view

        self.nodes = []
        self.edges = []
        self.connections = []
        self.directed_graph = Graph(directed=True)
        self.undirected_graph = Graph(directed=False)

        self.node_radius = 15
        self.node_fieldRadius = 80
        #self.graph_data = ''

        self.label_node_count = self.view.frame_graph.findChild(QLineEdit, 'lineEdit_node_count')

        self.DFS_sequential = QSequentialAnimationGroup()
        self.BFS_sequential = QSequentialAnimationGroup()
        self.DIJKSTRA_sequential = QSequentialAnimationGroup()
        self.sequential = QSequentialAnimationGroup()

        # Se atribuie cele 3 animatii ale algoritmilor animatiei de grup
        self.sequential.addAnimation(self.DFS_sequential)
        self.sequential.addAnimation(self.BFS_sequential)
        self.sequential.addAnimation(self.DIJKSTRA_sequential)

        self.gravity = True
        self.force_mode = False
        self.directed = False

    def receive_data(self, graph_data):
        """Verifica datele grafului

        Daca datele grafului sunt un string gol se sterg toate nodurile si muchile, la fel
        si datele anterioare despre graf. In caz contrar se va apela metoda manipulate_data.

        Parametrii
        ----------
        graph_data: str
            datele grafului
        """

        if not graph_data:

            for node in self.nodes:
                self.view.scene.removeItem(node)
            self.nodes.clear()

            for edge in self.edges:
                self.view.scene.removeItem(edge)
            self.edges.clear()

            self.undirected_graph.clear()
            self.directed_graph.clear()

            return

        self.manipulate_data(graph_data)

    def manipulate_data(self, graph_data):
        """Creearea grafului in funtie de datele primite

        Separand textul primit de toate spatiile si caracterele de sfarsit de line
        se vor obine toate nodurile, muchile si costurile acestora, daca este cazul.
        Acestea se vor adauga in vectorii de nodes si eedges care se vor pasa mai
        departe metodelor add_remove_nodes si add_remove_edges

        Parametrii
        ----------
        graph_data: str
            datele grafului
        """

        #self.graph_data = graph_data

        nodes = []
        edges = []

        graph_lines = graph_data.split('\n')
        for line in graph_lines:
            _line = list(filter(None, line.split(' ')))
            # Daca exista doar un nod pe line si nu a mai fost adaugat
            if len(_line) == 1 and _line[0] not in nodes:
                nodes.append(_line[0])
            # Daca exista mai multe elemente pe line
            elif len(_line) > 1:
                # Se adauga primul nod
                if _line[0] not in nodes:
                    nodes.append(_line[0])
                # Se adauga cel de-al doilea nod
                if _line[1] not in nodes:
                    nodes.append(_line[1])
                # Se adauga muchia dintre cele 2 noduri si costul (daca exista)
                if (_line[0], _line[1]) not in edges \
                        and _line[0] is not _line[1]:
                    cost = _line[2] if len(_line) >= 3 else None
                    edges.append((_line[0], _line[1], cost))

        self.add_remove_nodes(nodes)
        self.add_remove_edges(edges)

    def add_remove_nodes(self, nodes):
        """Adauga sau sterge noduri in functie de noile date

        Interand prin nodurile actuale se cauta care dintre acestea nu se afla printre noile noduri
        si se streg, inclusiv toate muchile actuale formate de acestea. Dupa stergerea celor
        neuitilizare se itereaza prin noile noduri si se adauga in scene si in lisele de adiacenta.

        Parametrii
        ----------
        nodes: list
            Lista nodurilor reinnoita
        """

        for node in self.nodes:
            found = False
            # Daca nodul a fost gasit nu mai trebuie adaugat
            for node_text in nodes:
                if node.__repr__() == node_text:
                    found = True
                    nodes.remove(node_text)
                    break
            # Daca nodul nu este gasit se sterge, inclusiv muchiile
            # formate de acesta
            if not found:
                edge_copy = self.edges.copy()

                for edge in edge_copy:
                    if edge.node1 == node or edge.node2 == node:
                        self.edges.remove(edge)
                        self.view.scene.removeItem(edge)

                del self.directed_graph[node]
                del self.undirected_graph[node]

                self.remove_all_connections()
                self.view.scene.removeItem(node)
        # Noiile noduri
        for node_text in nodes:
            node = Node(node_text, self)

            self.directed_graph.edges[node].clear()
            self.undirected_graph.edges[node].clear()

            self.view.scene.addItem(node)
            self.remove_all_connections()

        self.nodes = list(self.directed_graph.edges.keys())
        self.label_node_count.setText(str(len(self.nodes)))

    def add_remove_edges(self, edges):
        """Adauga sau sterge muchii in functie de noile date

        Interand prin muchile actuale se cauta care dintre acestea nu se afla in printre noile
        muchii si se streg. Dupa stergerea celor neuitilizare se itereaza prin noile muchii
        si se adauga in scene si in lisele de adiacenta.

        Parametrii
        ----------
        edges: list
            Lista muchilor reinnoita
        """

        edge_copy = self.edges.copy()
        for edge in edge_copy:
            found = False

            for elem in edges:
                n1, n2, cost = elem
                # Daca muchia este gasita
                if edge.node1.__repr__() == n1 and edge.node2.__repr__() == n2 and \
                        edge.cost == cost:
                    found = True
                    edges.remove(elem)
                    break
            # Daca muchia nu este gasita se sterge
            if not found:
                self.directed_graph.remove_edge(edge.node1, edge.node2)
                self.undirected_graph.remove_edge(edge.node1, edge.node2)

                self.view.scene.removeItem(edge)
                self.edges.remove(edge)
        # Noiile muchii
        for elem in edges:
            n1, n2, cost = elem

            for node in self.nodes:
                if node.__repr__() == n1:
                    node1 = node
                elif node.__repr__() == n2:
                    node2 = node

            edge = Edge(node1, node2, self, cost)
            cost = int(cost) if cost is not None and cost.isnumeric() else None

            self.directed_graph.add_edge(node1, node2, cost)
            self.undirected_graph.add_edge(node1, node2, cost)

            self.edges.append(edge)
            self.view.scene.addItem(edge)

    def update_nodes(self):
        """Reinnoiste pozirile nodurilor

        Daca modul de gravitatie nu este dezactivat se caluleaza forta de gravitatie
        care actioneaza asuprea fiecarui nod si i se actualizeaza pozitia in funtie
        de aceasta, dupa care se verifica coliziunea fiecarui nod.
        """

        for node in self.nodes:
            if self.gravity:
                node.force = self.forces(node)

                #tempPos = node.pos()
                node.moveBy(node.force.x() * (dt ** 2),
                            node.force.y() * (dt ** 2))
                #node.oldPos = tempPos

            self.check_collision(node)

    def draw_edges(self):
        """Acualizeaza muchile dintre fiecare pereche de noduri

        Creaza un path de la marginea cercului primului nod la marginea cercului celui
        de-al doilea nod, in funtie daca graful este orientat sau nu.
        """

        for edge in self.edges:
            dx, dy, alfa = self.get_angle(edge.node1, edge.node2)

            start_point = QPointF(edge.node1.x() + self.node_radius * (math.cos(alfa)),
                                  edge.node1.y() + self.node_radius * (math.sin(alfa)))

            end_point = QPointF(edge.node2.x() - self.node_radius * (math.cos(alfa)),
                                edge.node2.y() - self.node_radius * (math.sin(alfa)))

            created_path = edge.create_path(start_point, end_point, self.directed)
            edge.setPath(created_path)

    def update_connections(self):
        """Actualizarea pozitilor nodurlilor in funtie de conexiunile formate

        O conexiune intre noduri depinde de distanta dintre acestea
        """

        for connection in self.connections:
            dx, dy, angle = self.get_angle(connection.node1, connection.node2)
            connection.update(dx, dy)
            # node1 = connection.node1
            # node2 = connection.node2
            #
            # dx, dy, angle = self.get_angle(node1, node2)
            # d = math.sqrt(dx * dx + dy * dy)
            # diff = connection.length - d
            # percent = diff / d * 0.5
            # offsetX = dx * percent
            # offsetY = dy * percent
            #
            # #if not node1.pinned:
            # node1.setPos(node1.x() - offsetX, node1.y() - offsetY)
            # #if not node2.pinned:
            # node2.setPos(node2.x() + offsetX, node2.y() + offsetY)

    def forces(self, node):
        """Calularea fortei de gravitatie care actioneaza asupra nodului

        Forta de gravitatie este invers proportioanal cu distanta dintre
        nod si cnetrul scene-ului.

        Parametrii
        ----------
        node: Node
            nodul pentru care se va calcula forta de gravitatie

        Returneaza
        ----------
        force: QPointF
            reprezinta forta de gravitatie care actioneaza asupra nodului
            descomupsa pe cele 2 axe
        """

        dx, dy, alfa = self.get_angle(node, QPointF(self.view.width() / 2,
                                                    self.view.height() / 2))
        dsq = math.sqrt(dx * dx + dy * dy)
        force = (dsq * math.sqrt(dsq + SOFTENING_CONSTANT)) / G

        force_x = float(force) * math.cos(alfa)
        force_y = float(force) * math.sin(alfa)

        force = QPointF(force_x * abs(dx), force_y * abs(dy))
        return force

    def check_collision(self, node):
        """Intersectia dintre noduri

        Daca distanta dintre centrele nodurilor este mai mica sau egala cu raza unui nod adunata
        cu raza campului de interactiune inseamna ca se intersecteaza. Daca exista intersectie si
        gravitatie acestea vor actiona unul in funtie de celalalt si vor forma o conexiune, daca
        nu exista gravitatie si se intersecteaza (sunt mutate manual unul in celalalt), se vor respinge.

        Parametrii
        ----------
        node: Node
            nodul pentru care se verifica intersectiile
        """

        for other_node in self.nodes:
            if other_node is not node:

                dx, dy, alfa = self.get_angle(node.center(), other_node.center())
                dsq = math.sqrt(dx * dx + dy * dy)

                length = self.node_fieldRadius + self.node_radius
                if dsq <= length and other_node not in node.connectedTo:
                    if self.gravity:
                        node.connectedTo.append(other_node)
                        self.connections.append(Connection(node, other_node, length))
                    else:
                        overlap = dsq - self.node_radius - self.node_fieldRadius
                        node.moveBy(-0.5 * overlap * (node.x() - other_node.x()) / dsq,
                                    -0.5 * overlap * (node.y() - other_node.y()) / dsq)
                        other_node.moveBy(0.5 * overlap * (node.x() - other_node.x()) / dsq,
                                          0.5 * overlap * (node.y() - other_node.y()) / dsq)

    def get_angle(self, point1, point2):
        """Primeste 2 pucnte si calculeaza distanta orizontala, distanta verticala si unghiul dintre
           cele 2 pucnte

        Parametrii
        ----------
        point1: QPointF
            Coordonatele primului punct
        point2: QPointF
            Coordonatele celui de-al doilea punct

        Returneaza
        ----------
        dx: float
            distanta verticala
        dy: float
            distanta orizontala
        angle: float
            unghiul format de cele 2 pucnte
        """

        dy = point2.y() - point1.y()
        dx = point2.x() - point1.x()
        angle = math.atan2(dy, dx)

        return dx, dy, angle

    def find_edge(self, node1, node2):
        """Cauta prin daca exista o muchie intre 2 noduri

        Parametrii
        ----------
        node1: Node
            primul nod
        node2: Node
            al doilea nod

        Returneaza
        ----------
        edge: Edge
            daca exista o muchie intre cele 2 noduri
        None:
            daca nu exista muchie inter cele 2 noduri
        """

        for edge in self.edges:
            if (edge.node1 == node1 and edge.node2 == node2) or \
                    (edge.node1 == node2 and edge.node2 == node1):
                return edge
        return None

    def remove_all_connections(self):
        """Sterge toate conexiunile facute intre noduri"""

        self.connections.clear()
        for node in self.nodes:
            node.connectedTo.clear()

    def start_animations(self, text_DFS, text_BFS, text_DIJKSTRA_src, text_DIJKSTRA_end, algorithm_to_get_path=""):
        """Crearea grupurilor de aniamtii corespunzatoare

        Daca este pasat un argument in cel putin unul din cele 4 campuri, incepe cautarea nodurilor
        respective textul primit, daca nodul este gasit va incepe algorimtul respectiv, implict vor
        fi adaugate nodurile si muchile care trec prin algoritm si vor fi pornite (pe rand) animatile
        celor 3 algoritmi.
        """
        actual_path_to_return = None

        if not (text_DFS or text_BFS or text_DIJKSTRA_src or text_DIJKSTRA_end):  # if all are empty
            if not algorithm_to_get_path:  # and no specific path is requested
                return None  # Or an empty list, depending on desired signature for no-op
            # If a path is requested but no start points given for that algo, handle below or return []
            # For now, let specific algo sections handle it.

        self.DFS_sequential.clear()
        self.BFS_sequential.clear()
        self.DIJKSTRA_sequential.clear()

        node_end = None
        node_src = None

        # Find src/end for Dijkstra first, as it's not tied to iterating node for start_animations's main loop logic
        # This part is just to identify the nodes for Dijkstra if its texts are provided.
        # The actual Dijkstra call and path retrieval will happen after the loop.
        if text_DIJKSTRA_src or text_DIJKSTRA_end:  # Only search if Dijkstra texts are provided
            for node in self.nodes:
                if node.__repr__() == text_DIJKSTRA_src:
                    node_src = node
                if node.__repr__() == text_DIJKSTRA_end:  # Use if, not elif, as src and end can be the same node
                    node_end = node

        adj_list = self.undirected_graph if not self.directed else self.directed_graph
        for node in self.nodes:
            if text_DFS and node.__repr__() == text_DFS:  # Ensure text_DFS is provided
                visited = np.zeros(len(self.nodes))
                # DFS modifies the list passed to it and also returns it.
                # For start_animations, we want to capture this returned list if DFS is the target.
                dfs_path_names_list = []  # Initialize a new list for this call
                returned_dfs_path = self.DFS(node, visited, adj_list, dfs_path_names_list)
                if algorithm_to_get_path == "DFS":
                    actual_path_to_return = returned_dfs_path

            if text_BFS and node.__repr__() == text_BFS:  # Ensure text_BFS is provided
                visited = np.zeros(len(self.nodes))
                bfs_path_names = self.BFS(node, visited, adj_list)
                if algorithm_to_get_path == "BFS":
                    actual_path_to_return = bfs_path_names

        # DIJKSTRA path retrieval logic
        if text_DIJKSTRA_src and text_DIJKSTRA_end:  # Check if texts were provided
            if node_src and node_end:  # Check if nodes were found
                dijkstra_path_names = self.DIJKSTRA(node_src, node_end, adj_list)
                if algorithm_to_get_path == "DIJKSTRA":
                    actual_path_to_return = dijkstra_path_names
            elif algorithm_to_get_path == "DIJKSTRA":  # Dijkstra requested, but src/end nodes not found or not valid
                actual_path_to_return = []
        elif algorithm_to_get_path == "DIJKSTRA":  # Dijkstra requested, but src/end texts were not provided
            actual_path_to_return = []

        self.sequential.start()
        return actual_path_to_return

    def DFS(self, start, visited, graph, visited_order_names):
        """Algoritmul DFS din nodul de start pe lista de adiacenta"""

        # The list `visited_order_names` is passed by reference and appended to.
        # No need to check if it's None here if start_animations guarantees initialization.
        # However, the original check `if not visited_order_names:` was more for standalone/robustness.
        # Let's stick to the plan: start_animations initializes it.

        visited[self.nodes.index(start)] = 1
        visited_order_names.append(start.__repr__())
        self.DFS_sequential.addAnimation(self.create_animation(start, start.pen.color(), DFS_COLOR))

        for node in graph.edges[start]:
            if not visited[self.nodes.index(node)]:
                edge = self.find_edge(start, node)
                self.DFS_sequential.addAnimation(self.create_animation(edge, node.pen.color(), DFS_COLOR))
                self.DFS(node, visited, graph, visited_order_names)

        return visited_order_names

    def BFS(self, start, visited, graph):
        """Algoritmul BFS din nodul de start pe lista de adiacenta"""

        visited_order_names = []
        queue = [start]
        visited[self.nodes.index(start)] = 1
        visited_order_names.append(start.__repr__())
        self.BFS_sequential.addAnimation(self.create_animation(start, start.pen.color(), BFS_COLOR))

        while queue:
            s = queue.pop(0)
            for node in graph.edges[s]:
                node_index = self.nodes.index(node)
                if not visited[node_index]:
                    queue.append(node)
                    visited[node_index] = 1
                    visited_order_names.append(node.__repr__())

                    edge = self.find_edge(s, node)
                    self.BFS_sequential.addAnimation(self.create_animation(edge, edge.pen().color(), BFS_COLOR))
                    self.BFS_sequential.addAnimation(self.create_animation(node, node.pen.color(), BFS_COLOR))

        return visited_order_names

    def DIJKSTRA(self, initial, end, graph):
        """Algorimul DIJKSTRA pe lista de adiacenta

        shortest_paths e un dictionar de noduri
        ale carui valori sunt un tuple de forma
        (nod_anterior, cost)
        """

        shortest_paths = {initial: (None, 0)}
        current_node = initial
        visited = set()

        while current_node != end:
            visited.add(current_node)
            destinations = graph.edges[current_node]
            weight_to_current_node = shortest_paths[current_node][1]

            for next_node in destinations:
                weight = graph.weights[(current_node, next_node)] + weight_to_current_node
                if next_node not in shortest_paths:
                    shortest_paths[next_node] = (current_node, weight)
                else:
                    current_shortest_weight = shortest_paths[next_node][1]
                    if current_shortest_weight > weight:
                        shortest_paths[next_node] = (current_node, weight)

            next_destinations = {node: shortest_paths[node] for node in shortest_paths if node not in visited}
            if not next_destinations:
                return []
            # Nodul urmator este destinatia cu cel mai mic cost
            current_node = min(next_destinations, key=lambda k: next_destinations[k][1])

        # Se merge inapoi prin destinatii pe cel mai scurt drum
        path = []
        while current_node is not None:
            path.append(current_node)
            next_node = shortest_paths[current_node][0]
            current_node = next_node

        # Se inverseaza vectorul
        path = path[::-1]
        path_names = [node.__repr__() for node in path]

        if not path_names:  # Should not happen if next_destinations handles empty path, but as a safeguard
            return []

        src_node = path[0]
        self.DIJKSTRA_sequential.addAnimation(self.create_animation(src_node, src_node.pen.color(), DIJKSTRA_COLOR))

        for node in path[1:]:
            edge = self.find_edge(src_node, node)
            self.DIJKSTRA_sequential.addAnimation(self.create_animation(edge, edge.pen().color(), DIJKSTRA_COLOR))
            self.DIJKSTRA_sequential.addAnimation(self.create_animation(node, node.pen.color(), DIJKSTRA_COLOR))
            src_node = node

        return path_names

    def create_animation(self, item, start_color, end_color):
        """Creaza o animatie a item-ul de la culoare de start la cea de sfarsit tip de 1 secunda"""

        animation = QVariantAnimation()
        animation.DeletionPolicy(QVariantAnimation.DeleteWhenStopped)

        animation.valueChanged.connect(item.handle_value_changed)
        animation.setDuration(1000)

        animation.setStartValue(start_color)
        animation.setEndValue(end_color)

        return animation
