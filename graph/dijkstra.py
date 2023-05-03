from data_structures.hash import HashTable
from data_structures.priority_queue import PriorityQueue


class Dijkstra:

    def __init__(self, start, graph):
        self.start = start
        self.graph = graph
        self.start_edges = self.graph.get_weighted_edges(self.start)
        self.dist_table = HashTable()
        self.priority_queue = PriorityQueue()
        self.unvisited = set()
        self.visited = set()
        self.initialize()

    def initialize(self):
        if self.start not in self.graph.get_all_vertices():
            raise ValueError('Starting location node not found.')
        start_weight, prev_vertex = 0, None
        self.dist_table.add_node(self.start, (start_weight, prev_vertex))

        for vertex, weight in self.start_edges:
            self.dist_table.add_node(unhashed_key=vertex, value=(weight, self.start))
            self.priority_queue.insert(priority=weight, information=vertex)
            self.unvisited.add(vertex)
        self.execute()

    def execute(self):
        # print(f'START LOCATION: {self.start}')
        while self.unvisited:
            # print(f'\nNumber of unvisited: {len(self.unvisited)}')

            current = self.priority_queue.get()
            # print(f'   Current in queue:  {current}')
            # print(f'       In unvisited? ~{current in self.unvisited}')
            curr_min_dist = self.get_dist_and_prev(current)[0]
            # print(f" Current's distance from source = {curr_min_dist}")

            for neighbor_tuple in self.graph.get_weighted_edges(current):
                neighbor = neighbor_tuple[0]

                if neighbor not in self.visited:
                    neighbor_dist_from_curr = neighbor_tuple[1]
                    # print(f' * Neighbor: {neighbor}')
                    neighbor_dist_from_start = self.get_dist_and_prev(neighbor)[0]
                    # print(f'        From current: {neighbor_dist_from_curr} | From start: {neighbor_dist_from_start}')
                    if curr_min_dist + neighbor_dist_from_curr < neighbor_dist_from_start:
                        # print(f'                         *****UPDATING***** distance to neighbor node')
                        new_min_dist = curr_min_dist + neighbor_dist_from_curr
                        self.dist_table.change_node(neighbor, (new_min_dist, current))
                        self.priority_queue.change_priority(priority=new_min_dist, information=neighbor)

            self.unvisited.remove(current)
            self.visited.add(current)
        return

    def get_shortest_path(self, target_location):
        # print(f'START:  {self.start} ----> TARGET:  {target_location}')
        path = []
        target_node = self.dist_table.get_node(target_location)
        shortest_distance = target_node.value[0]
        path.append((target_node.key, shortest_distance))
        prev_loc = target_node.value[1]

        while prev_loc:
            path.append(prev_loc)
            prev_node = self.dist_table.get_node(prev_loc)
            prev_loc = prev_node.value[1]

        path.reverse()
        return path

    def get_dist_and_prev(self, target):
        node = self.dist_table.get_node(target)
        weight = node.value[0]
        prev = node.value[1]
        return weight, prev
