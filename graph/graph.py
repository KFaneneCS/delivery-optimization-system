from data_structures.hash import HashTable
from locations.location import Location


class Graph:
    """
    A self-adjusting class that implements a graph structure containing vertices and their weighted edges.

    This implementation allows for adding and removing vertices and edges, as well as getting all vertices, edges,
    and the graph itself.  It also provides a function that prints a simple representation of the graph and its
    connections to console.
    """
    def __init__(self):
        """
        Initializes a new instance of the Graph class.
        """
        self._graph = HashTable(60)
        self._size = 0

    @property
    def size(self) -> int:
        """
        Gets the size of the graph - that is, the number of vertices it contains.
        :return: The number of vertices in the graph.
        """
        return self._size

    @size.setter
    def size(self, size_val):
        """
        Sets the size of the graph when incremented or decremented (by 1 for each vertex added or removed).
        :param size_val: The new value of the graph's size.
        """
        self._size = size_val

    def add_vertex(self, vertex):
        """
        Adds a new vertex to the graph and increments the graph's size by 1 accordingly.
        :param vertex: The new vertex to be added to the graph.
        """
        self._graph[vertex] = []
        self.size += 1

    def add_weighted_edge(self, source: Location, target: Location, weight: float):
        """
        Adds a weighted edge to existing vertices in the graph.
        :param source: The source vertex of the weighted edge.
        :param target: The target vertex of the weighted edge.
        :param weight: The value/weight of the edge.
        """
        # Graph node with address as key and (target location, weight) tuple as value
        source_node = self._graph[source]
        source_tuple = (target, weight)
        source_node.value.append(source_tuple)

    def remove_vertex(self, vertex):
        """
        Removes a vertex from the graph if it exists.
        :param vertex: The vertex to be removed from the graph.
        :raises ValueError: If the hash table's delete method returns None, indicating the vertex does not exist.
        """
        if self._graph.delete(vertex):
            self._size -= 1
        else:
            raise ValueError(f'Vertex {vertex} not found in the graph.')

    def remove_edge(self, source: Location, target: Location):
        curr_edge_list = self._graph[source]
        # Update edge list by removing edge that contains the passed source vertex.
        curr_edge_list.value = [(v, w) for v, w in curr_edge_list.value if v != target]

    def change_edge_weight(self, source: Location, target: Location, new_weight: float):
        curr_edge_list = self._graph[source]
        for i, (vertex, weight) in enumerate(curr_edge_list.value):
            if vertex == target:
                curr_edge_list.value[i] = (vertex, new_weight)

    def get_graph(self):
        return self._graph

    def get_all_vertices(self):
        return [vertex for vertex, edge_list in self._graph.items()]

    def get_weighted_edges(self, loc_object):
        vertex = self._graph[loc_object]
        return vertex.value

    def show_all_connections(self):
        for location, edge_list in self._graph.items():
            print(f'Location: {location}')
            for edge in edge_list:
                print(f'  -> {edge[0].get_key()} | {edge[1]} miles')
