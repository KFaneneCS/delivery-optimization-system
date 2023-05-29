import math
from typing import List

from data_structures.hash import HashTable
from data_structures.priority_queue import PriorityQueue
from locations.location import Location
from .graph import Graph


class Dijkstra:
    """

    """

    def __init__(self, start: Location, graph: Graph):
        self._start = start
        self.graph = graph
        self.start_edges = self.graph.get_weighted_edges(self.start)
        self._distance_table = HashTable()
        self.all_paths = HashTable()
        self.priority_queue = PriorityQueue(is_max=False)
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
        self._distance_table[self._start] = (start_weight, prev_vertex)

        for vertex, weight in self.start_edges:
            self._distance_table[vertex] = (weight, self.start)
            self.priority_queue.insert(priority=weight, information=vertex)
            self.unvisited.add(vertex)

    @property
    def start(self) -> Location:
        return self._start

    @property
    def distance_table(self):
        return self._distance_table

    def _execute(self):
        while self.unvisited:
            curr_node = self.priority_queue.get()
            min_dist_to_curr = self.get_dist_and_prev(curr_node)[0]

            for edge_to_neighbor in self.graph.get_weighted_edges(curr_node):
                neighbor_node = edge_to_neighbor[0]

                if neighbor_node not in self.visited:
                    dist_neighbor_to_curr = edge_to_neighbor[1]
                    dist_start_to_curr = self.get_dist_and_prev(neighbor_node)[0]
                    if min_dist_to_curr + dist_neighbor_to_curr < dist_start_to_curr:
                        new_min_dist = round(min_dist_to_curr + dist_neighbor_to_curr, ndigits=3)
                        self._distance_table.change_node(unhashed_key=neighbor_node,
                                                         new_value=(new_min_dist, curr_node))
                        self.priority_queue.change_priority(priority=new_min_dist, information=neighbor_node)

            self.unvisited.remove(curr_node)
            self.visited.add(curr_node)

    def _find_all_shortest_paths(self):
        for target_location, _ in self._distance_table.items():
            self.get_shortest_path(target_location)

    def get_shortest_path(self, target_location):
        if self.all_paths.has_node(target_location):
            return self.all_paths[target_location].value

        path = []
        target_node = self._distance_table[target_location]
        shortest_dist = target_node.value[0]
        path.append((target_node.key, shortest_dist))
        prev_loc = target_node.value[1]

        while prev_loc:
            path.append(prev_loc)
            prev_node = self._distance_table[prev_loc]
            prev_loc = prev_node.value[1]

        path.reverse()
        self.all_paths[target_location] = path
        return path

    def get_dist_and_prev(self, target):
        node = self._distance_table[target]
        weight = node.value[0]
        prev = node.value[1]
        return weight, prev

    def get_closest_from_start(self, visited: set):
        min_distance = math.inf
        curr_closest = None
        for target, (distance, _) in self._distance_table.items():
            if target not in visited and distance < min_distance and distance != 0:
                min_distance = distance
                curr_closest = target
        return curr_closest, min_distance

    def get_closest_from_group(self, group: List[Location]):
        min_distance = math.inf
        curr_closest = None
        for location in group:
            distance, _ = self._distance_table[location].value
            if distance != 0 and distance < min_distance:
                min_distance = distance
                curr_closest = location
        return curr_closest, min_distance

    def get_max_distance(self):
        max_distance = 0.0
        for location, dist_to_neighbor in self._distance_table.items():
            curr_distance = dist_to_neighbor[0]
            if curr_distance > max_distance:
                max_distance = curr_distance
        return max_distance
