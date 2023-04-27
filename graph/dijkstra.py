import math
from queue import Queue
from hash.hash import HashTable


class Dijkstra:

    def __init__(self, start, graph):
        print('dijkstra initialized')
        self.start = start
        self.graph = graph
        self.vertex_queue = Queue()
        self.distances = HashTable(self.graph.get_size() * 2)
        self.visited = set()
        self.initialize()

    def initialize(self):
        self.distances.add(self.start, 0)
        for vertex in self.graph.get_all_vertices():
            if vertex is not self.start:
                self.distances.add(vertex, math.inf)
            else:
                self.vertex_queue.put(vertex)

    def get_distance(self, target):
        return self.distances.get_node(target)

    def get_min_distance(self, source, target):
        return

    def dijkstra(self):
        while self.vertex_queue.qsize() > 0:
            return

