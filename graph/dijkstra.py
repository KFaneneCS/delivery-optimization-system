import math
from queue import Queue
from hash.hash import HashTable


class Dijkstra:

    def __init__(self, start, graph):
        self.start = start
        self.graph = graph
        self.vertex_list = []
        self.v_queue = Queue()
        self.dist_table = HashTable(self.graph.get_size() * 2)
        self.visited = set()
        self.initialize()

    def initialize(self):
        self.dist_table.add(self.start, 0)
        for vertex in self.graph.get_all_vertices():
            if vertex is not self.start:
                self.dist_table.add(vertex, math.inf)
            self.vertex_list.append(vertex)

    def get_distance(self, target):
        return self.dist_table.get_node(target)

    def execute(self):
        while not self.v_queue.qsize() == 0:
            min_vertex = min(self.vertex_list, key=lambda x: self.dist_table.get_node(x).value)
            min_index = self.vertex_list.index(min_vertex)
            self.vertex_list.pop(min_index)

