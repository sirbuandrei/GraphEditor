import heapq
from collections import defaultdict, deque


class AlgorithmsManager:
    def __init__(self):
        self._algorithms = {"Breadth First Search": self.bfs, "Depth First Search": self.dfs, "Shortest Path": self.dijkstra}

    def run_algorithm(self, algorithm_type, edges, is_directed, algorithm_input):
        graph = self.build_adjacency_list(edges, is_directed)
        print(graph)
        try:
            return self._algorithms[algorithm_type](graph, algorithm_input)
        except Exception as e:
            print(e)

    def add_algorithm(self, algorithm_type, func):
        self._algorithms[algorithm_type] = func

    def build_adjacency_list(self, edges, directed):
        graph = {}

        for (from_node, to_node), cost in edges.items():
            if from_node not in graph:
                graph[from_node] = []
            if to_node not in graph:
                graph[to_node] = []

        for (from_node, to_node), cost in edges.items():
            graph[from_node].append((to_node, cost))
            if not directed:
                graph[to_node].append((from_node, cost))

        return graph

    def bfs(self, graph, start_node):
        if start_node not in graph:
            return

        animation_steps = []
        output = ''
        animation_color = "#7289da"

        visited = set()
        visited_nodes = []
        traversed_edges = []
        queue = deque([start_node])

        while queue:
            node = queue.popleft()

            if node in visited:
                continue

            visited.add(node)
            visited_nodes.append(node)
            animation_steps.append({"item": node, "color": animation_color})

            for neighbor, _ in graph[node]:
                if neighbor not in visited:
                    traversed_edges.append((node, neighbor))
                    animation_steps.append({"item": (node, neighbor), "color": animation_color})
                    queue.append(neighbor)

        return animation_steps, ' '.join(str(x) for x in visited_nodes)

    def dfs(self, graph, start_node):
        if start_node not in graph:
            return

        animation_steps = []
        animation_color = "#7289da"

        if start_node not in graph:
            return [], []

        visited = set()
        visited_nodes = []
        traversed_edges = []

        def dfs_recursive(node):
            if node in visited:
                return

            visited.add(node)
            visited_nodes.append(node)
            animation_steps.append({"item": node, "color": animation_color})

            for neighbor, _ in graph[node]:
                if neighbor not in visited:
                    traversed_edges.append((node, neighbor))
                    animation_steps.append({"item": (node, neighbor), "color": animation_color})
                    dfs_recursive(neighbor)

        dfs_recursive(start_node)
        return animation_steps, ' '.join(x for x in visited_nodes)

    def dijkstra(self, graph, algorithm_input):
        items = algorithm_input.split(' ')

        if len(items) != 2:
            return

        if items[0] not in graph or items[1] not in graph:
            return

        start_node = items[0]
        end_node = items[1]

        paths = {start_node: (0, None)}
        current_node = start_node
        visited = set()

        while current_node != end_node:
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

        return [], ''



