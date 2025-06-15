import inspect


def bfs(graph, start_node):
    from collections import deque

    if start_node not in graph:
        return

    animation_steps = []
    output = ''
    animation_color = "#7289da"

    visited = set()
    visited_nodes = []
    queue = deque([start_node])

    visited.add(start_node)
    visited_nodes.append(start_node)
    animation_steps.append({"item": start_node, "color": animation_color})

    while queue:
        node = queue.popleft()
        animation_steps.append({"item": node, "color": "yellow"})

        for neighbor, _ in graph[node]:
            if neighbor not in visited:
                visited.add(neighbor)
                visited_nodes.append(neighbor)

                animation_steps.append({"item": (node, neighbor), "color": animation_color})
                animation_steps.append({"item": neighbor, "color": animation_color})

                queue.append(neighbor)

    return animation_steps, ' '.join(str(x) for x in visited_nodes)


def dfs(graph, start_node):
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


def dijkstra(graph, algorithm_input):
    import heapq

    items = algorithm_input.split(' ')

    if len(items) != 2:
        return

    if items[0] not in graph or items[1] not in graph:
        return

    start_node = items[0]
    end_node = items[1]

    distances = {node: float('inf') for node in graph}
    previous = {node: None for node in graph}
    came_from_edge = {}
    distances[start_node] = 0

    priority_queue = [(0, start_node)]
    visited = set()
    animation_steps = []

    while priority_queue:
        current_distance, current_node = heapq.heappop(priority_queue)

        if current_node in visited:
            continue
        visited.add(current_node)

        animation_steps.append({"item": current_node, "color": "yellow"})

        for neighbor, weight in graph.get(current_node, []):
            edge_tuple = (current_node, neighbor)
            if neighbor in visited:
                continue

            animation_steps.append({"item": edge_tuple, "color": "orange"})

            distance = current_distance + weight
            if distance < distances[neighbor]:
                if previous[neighbor] is not None:
                    old_edge = (previous[neighbor], neighbor)
                    animation_steps.append({"item": old_edge, "color": "red"})

                distances[neighbor] = distance
                previous[neighbor] = current_node
                came_from_edge[neighbor] = edge_tuple

                animation_steps.append({"item": neighbor, "color": "lightblue"})
                animation_steps.append({"item": edge_tuple, "color": "green"})

        animation_steps.append({"item": current_node, "color": "gray"})

    # Reconstruct path
    path = []
    current = end_node
    while current is not None:
        path.append(current)
        current = previous[current]
    path.reverse()

    if path and path[0] == start_node:
        for i in range(len(path) - 1):
            animation_steps.append({"item": path[i], "color": "blue"})
            animation_steps.append({"item": (path[i], path[i + 1]), "color": "blue"})
        animation_steps.append({"item": path[-1], "color": "blue"})
        return animation_steps, ''

    return animation_steps, ''


class AlgorithmsManager:
    def __init__(self):
        self._algorithms = {"Breadth First Search": bfs, "Depth First Search": dfs, "Shortest Path": dijkstra}

    def get_algorithm(self, algorithm):
        return inspect.getsource(self._algorithms[algorithm]), self._algorithms[algorithm].__name__

    def set_code(self, algorithm, code):
        self._algorithms[algorithm] = code

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



