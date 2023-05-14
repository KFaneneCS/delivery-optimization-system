import math

from data_structures.hash import HashTable
from data_structures.priority_queue import MinPriorityQueue
from locations.location import Location
from .graph import Graph


class Dijkstra:

    def __init__(self, start: Location, graph: Graph):
        self._start = start
        self.graph = graph
        self.start_edges = self.graph.get_weighted_edges(self.start)
        self._distance_table = HashTable()
        self.all_paths = HashTable()
        self.priority_queue = MinPriorityQueue()
        self.unvisited = set()
        self.visited = set()
        self._closest_from_start = None
        self._initialize()
        self._execute()
        self._find_all_shortest_paths()

    def _initialize(self):
        if self.start not in self.graph.get_all_vertices():
            raise ValueError('Starting location node not found.')
        start_weight, prev_vertex = 0, None
        self.distance_table.add_node(self.start, (start_weight, prev_vertex))

        for vertex, weight in self.start_edges:
            self.distance_table.add_node(unhashed_key=vertex, value=(weight, self.start))
            self.priority_queue.insert(priority=weight, information=vertex)
            self.unvisited.add(vertex)

    @property
    def start(self):
        return self._start

    def _execute(self):
        while self.unvisited:
            # print(f'\nNumber of unvisited: {len(self.unvisited)}')
            curr_node = self.priority_queue.get()
            # print(f'   Current in queue:  {curr_node}')
            # print(f'       In unvisited? ~{curr_node in self.unvisited}')
            min_dist_to_curr = self.get_dist_and_prev(curr_node)[0]
            # print(f" Current's distance from source = {min_dist_to_curr}")

            for edge_to_neighbor in self.graph.get_weighted_edges(curr_node):
                neighbor_node = edge_to_neighbor[0]

                if neighbor_node not in self.visited:
                    dist_neighbor_to_curr = edge_to_neighbor[1]
                    # print(f' * Neighbor: {neighbor_node}')
                    dist_start_to_curr = self.get_dist_and_prev(neighbor_node)[0]
                    # print(f'        From curr_node: {dist_neighbor_to_curr} | From start: {dist_start_to_curr}')
                    if min_dist_to_curr + dist_neighbor_to_curr < dist_start_to_curr:
                        # print(f'*****UPDATING***** distance to neighbor_node node')
                        new_min_dist = round(min_dist_to_curr + dist_neighbor_to_curr, ndigits=3)
                        self.distance_table.change_node(unhashed_key=neighbor_node, new_value=(new_min_dist, curr_node))
                        self.priority_queue.change_priority(priority=new_min_dist, information=neighbor_node)

            self.unvisited.remove(curr_node)
            self.visited.add(curr_node)
        return self

    def _find_all_shortest_paths(self):
        for target_location, _ in self.distance_table.items():
            self.get_shortest_path(target_location)
        return self

    @property
    def distance_table(self):
        return self._distance_table

    def get_shortest_path(self, target_location):
        if self.all_paths.has_node(target_location):
            return self.all_paths.get_node(target_location).value

        path = []
        target_node = self.distance_table.get_node(target_location)
        shortest_dist = target_node.value[0]
        path.append((target_node.key, shortest_dist))
        prev_loc = target_node.value[1]

        while prev_loc:
            path.append(prev_loc)
            prev_node = self.distance_table.get_node(prev_loc)
            prev_loc = prev_node.value[1]

        path.reverse()
        self.all_paths.add_node(target_location, path)
        return path

    def get_shortest_path_distance(self, target_location) -> float:
        return self.all_paths.get_node(target_location).value[-1][1]

    def get_dist_and_prev(self, target):
        node = self.distance_table.get_node(target)
        weight = node.value[0]
        prev = node.value[1]
        return weight, prev

    def get_closest_from_start(self, visited: set):
        min_distance = math.inf
        curr_closest = None
        for target, (distance, _) in self.distance_table.items():
            if target not in visited and distance < min_distance and distance != 0:
                min_distance = distance
                curr_closest = target
        return curr_closest, min_distance

    def get_max_distance(self):
        max_distance = 0.0
        for location, dist_to_neighbor in self.distance_table.items():
            curr_distance = dist_to_neighbor[0]
            if curr_distance > max_distance:
                max_distance = curr_distance
        return max_distance
