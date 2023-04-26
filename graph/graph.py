from hash.hash import HashTable
import bisect


class Graph:
    def __init__(self):
        self.edges = HashTable(60)

    def add_vertex(self, node):
        self.edges.add(node.get_key(), [])

    def add_weighted_edge(self, source, target, weight):
        source_node = self.edges.get_node(source.get_key())
        source_tuple = (target, weight)

        # TODO:  May or may not need this sorted - come back to this later
        bisect.insort(source_node.value, source_tuple, key=lambda x: x[1])
        return self.edges

    def get_all_vertices(self):
        return [vertex for vertex, edge_list in self.edges.items()]

    def show_all_connections(self):
        for location, edge_list in self.edges.items():
            print(f'Location: {location}')
            for edge in edge_list:
                print(f'  -> {edge[0].get_key()} | {edge[1]} miles')
        return
