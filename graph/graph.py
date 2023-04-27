from hash.hash import HashTable
import bisect


class Graph:
    def __init__(self):
        self.graph = HashTable(60)
        self.size = 0

    def add_vertex(self, vertex):
        self.graph.add(vertex, [])
        self.size += 1

    def add_weighted_edge(self, source, target, weight):
        source_node = self.graph.get_node(source.get_key())
        source_tuple = (target, weight)

        # TODO:  May or may not need this sorted - come back to this later
        bisect.insort(source_node.value, source_tuple, key=lambda x: x[1])
        return self.graph

    def get_all_vertices(self):
        return [vertex for vertex, edge_list in self.graph.items()]

    def get_size(self):
        return self.size

    def show_all_connections(self):
        for location, edge_list in self.graph.items():
            print(f'Location: {location}')
            for edge in edge_list:
                print(f'  -> {edge[0].get_key()} | {edge[1]} miles')
        return

