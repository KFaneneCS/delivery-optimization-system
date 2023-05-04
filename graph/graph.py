import networkx as nx
from data_structures.hash import HashTable
import bisect


class Graph:
    def __init__(self):
        self.graph = HashTable(60)
        self.size = 0

    def get_hashed_graph(self):
        return self.graph

    def add_vertex(self, vertex):
        self.graph.add_node(vertex, [])
        self.size += 1

    def add_weighted_edge(self, source, target, weight):
        # Graph node with address as key and (target location, weight) tuple as value
        source_node = self.graph.get_node(source)
        source_tuple = (target, weight)
        source_node.value.append(source_tuple)
        return self.graph

    def get_all_vertices(self):
        return [vertex for vertex, edge_list in self.graph.items()]

    def get_weighted_edges(self, loc_object):
        vertex = self.graph.get_node(loc_object)
        return vertex.value

    def get_size(self):
        return self.size

    def show_all_connections(self):
        for location, edge_list in self.graph.items():
            print(f'Location: {location}')
            for edge in edge_list:
                print(f'  -> {edge[0].get_key()} | {edge[1]} miles')
        return
