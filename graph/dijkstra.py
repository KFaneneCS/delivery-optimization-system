import math
from queue import Queue
from hash.hash import HashTable


class Dijkstra:

    def __init__(self, start, destination, graph):
        self.start = start
        self.destination = destination
        self.graph = graph
        # self.dist_queue = Queue()
        self.dist_table = HashTable(self.graph.get_size() * 2)
        # self.visited = set()
        self.initialize()

    def initialize(self):
        self.dist_table.add(self.start, 0)
        for vertex, value in self.graph.get_hashed_graph().items():
            self.dist_table.add(vertex, math.inf)
        print(f'DISTANCE TABLE:   {self.dist_table.print_all()}')

        # for tuple_val in self.graph.get_weighted_edges(self.start):
        #     self.dist_queue.put(tuple_val)
        # while self.dist_queue.qsize() > 0:
        #     print(self.dist_queue.get())


        # self.dist_table.add(self.start, 0)
        # for vertex in self.graph.get_all_vertices():
        #     if vertex is not self.start:
        #         self.dist_table.add(vertex, math.inf)
        #     self.vertex_list.append(vertex)

    def get_distance(self, target):
        return
        # return self.dist_table.get_node(target)

    def execute(self):
        return
        # while not self.v_queue.qsize() == 0:
        #     min_vertex = min(self.vertex_list, key=lambda x: self.dist_table.get_node(x).value)
        #     min_index = self.vertex_list.index(min_vertex)
        #     self.vertex_list.pop(min_index)

