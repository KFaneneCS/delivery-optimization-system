from hash.hash import HashTable


class Graph:
    def __init__(self):
        self.size = 0
        self.vertices = []
        self.adjacencies = HashTable(table_size=50)

    def add_vertex(self, node):
        return self.vertices.append(node)

    def add_weighted_edge(self, source, target, weight):
        self.adjacencies.insert(source.get_address(), (target, weight))
        self.adjacencies.insert(target.get_address(), (source, weight))
        return self.adjacencies

    def show_all_connections(self):
        # FIXME:  Below shows failures in adjacencies hash table
        for x in self.adjacencies.get_all():
            print(x)
        # for vertex in self.vertices:
        #     print(f'current vertex = {vertex}')
        #     hashed_edges = self.adjacencies.lookup(vertex)
        #     print(type(hashed_edges))
        return


