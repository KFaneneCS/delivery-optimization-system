from hash.hash import HashTable

class Graph:
    def __init__(self):
        self.size = 0
        self.vertices = []
        self.adjacencies = HashTable(table_size=50)

    def add_vertex(self, node):
        return self.vertices.append(node)

    def add_edge(self, first, second, weight):
        self.adjacencies.insert(first, (second, weight))
        self.adjacencies.insert(second, (first, weight))
        return self.adjacencies



