from data_structures.hash import HashTable
from data_structures.priority_queue import PriorityQueue


class Dijkstra:

    def __init__(self, start, destination, graph):
        self.start = start
        self.destination = destination
        self.graph = graph
        self.start_edges = self.graph.get_weighted_edges(self.start)
        # self.dist_queue = Queue()
        self.dist_table = HashTable()
        self.priority_queue = PriorityQueue()
        # self.visited = set()
        self.unvisited = set()
        self.initialize()

    def initialize(self):
        start_weight, prev_vertex = 0, None
        self.dist_table.add_node(self.start, (start_weight, prev_vertex))

        for vertex, weight in self.start_edges:
            self.dist_table.add_node(unhashed_key=vertex, value=(weight, self.start))
            self.priority_queue.insert(priority=weight, information=vertex)
            self.unvisited.add(vertex)

    def execute(self):
        print(f'START LOCATION: {self.start}')
        while self.unvisited:
            print(f'\nNumber of unvisited: {len(self.unvisited)}')
            print(f'   Current in queue:  {self.priority_queue.peek()}')
            print(f'       In unvisited? ~{self.priority_queue.peek() in self.unvisited}')
            current = self.priority_queue.get()
            curr_min_dist = self.get_dist_and_prev(current)[0]
            print(f" Current's distance from source = {curr_min_dist}")
            COUNT = 0
            for neighbor_tuple in self.graph.get_weighted_edges(current):
                neighbor = neighbor_tuple[0]

                if neighbor in self.unvisited:
                    COUNT += 1

                    neighbor_dist_from_curr = neighbor_tuple[1]
                    print(f' * Neighbor: {neighbor}')
                    neighbor_dist_from_start = self.get_dist_and_prev(neighbor)[0]
                    print(f'        From current: {neighbor_dist_from_curr} | From start: {neighbor_dist_from_start}')
                    if curr_min_dist + neighbor_dist_from_curr < neighbor_dist_from_start:
                        print(f'      UPDATING distance to neighbor node')
                        new_min_dist = curr_min_dist + neighbor_dist_from_curr
                        self.dist_table.change_node(neighbor, (new_min_dist, current))
            print(f' ~~ number of neighbors visited:  {COUNT}')
            self.unvisited.remove(current)

    def get_dist_and_prev(self, target):
        node = self.dist_table.get_node(target)
        weight = node.value[0]
        prev = node.value[1]
        return weight, prev



        # for tuple_val in self.graph.get_weighted_edges(self.start):
        #     self.dist_queue.put(tuple_val)
        # while self.dist_queue.qsize() > 0:
        #     print(self.dist_queue.get())


        # self.dist_table.add(self.start, 0)
        # for vertex in self.graph.get_all_vertices():
        #     if vertex is not self.start:
        #         self.dist_table.add(vertex, math.inf)
        #     self.vertex_list.append(vertex)



    # def execute(self):
    #     return
        # while not self.v_queue.qsize() == 0:
        #     min_vertex = min(self.vertex_list, key=lambda x: self.dist_table.get_node(x).value)
        #     min_index = self.vertex_list.index(min_vertex)
        #     self.vertex_list.pop(min_index)

