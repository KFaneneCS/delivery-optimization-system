from data_structures.hash import HashTable
from data_structures.priority_queue import MinPriorityQueue
import typing


class Dijkstra:

    def __init__(self, start, graph):
        self.start = start
        self.graph = graph
        self.start_edges = self.graph.get_weighted_edges(self.start)
        self._dist_table = HashTable()
        self.all_paths = HashTable()
        self.priority_queue = MinPriorityQueue()
        self.unvisited = set()
        self.visited = set()
        self.initialize()
        self.execute()
        self.find_all_shortest_paths()

    def initialize(self):
        if self.start not in self.graph.get_all_vertices():
            raise ValueError('Starting location node not found.')
        start_weight, prev_vertex = 0, None
        self.dist_table.add_node(self.start, (start_weight, prev_vertex))

        for vertex, weight in self.start_edges:
            self.dist_table.add_node(unhashed_key=vertex, value=(weight, self.start))
            self.priority_queue.insert(priority=weight, information=vertex)
            self.unvisited.add(vertex)

    def execute(self):
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
                        new_min_dist = round(min_dist_to_curr + dist_neighbor_to_curr, ndigits=1)
                        self.dist_table.change_node(unhashed_key=neighbor_node, new_value=(new_min_dist, curr_node))
                        self.priority_queue.change_priority(priority=new_min_dist, information=neighbor_node)

            self.unvisited.remove(curr_node)
            self.visited.add(curr_node)
        return self

    def find_all_shortest_paths(self):
        for target_location, _ in self.dist_table.items():
            self.get_shortest_path(target_location)
        return self

    @property
    def dist_table(self):
        return self._dist_table

    def get_shortest_path(self, target_location):
        if self.all_paths.has_node(target_location):
            return self.all_paths.get_node(target_location).value

        path = []
        target_node = self.dist_table.get_node(target_location)
        shortest_dist = target_node.value[0]
        path.append((target_node.key, shortest_dist))
        prev_loc = target_node.value[1]

        while prev_loc:
            path.append(prev_loc)
            prev_node = self.dist_table.get_node(prev_loc)
            prev_loc = prev_node.value[1]

        path.reverse()
        self.all_paths.add_node(target_location, path)
        return path

    def get_dist_and_prev(self, target):
        node = self.dist_table.get_node(target)
        weight = node.value[0]
        prev = node.value[1]
        return weight, prev

    def get_max_distance(self):
        max_distance = 0.0
        for location, dist_to_neighbor in self.dist_table.items():
            curr_distance = dist_to_neighbor[0]
            if curr_distance > max_distance:
                max_distance = curr_distance
        return max_distance
