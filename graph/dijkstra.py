import math
from typing import List

from data_structures.hash import HashTable
from data_structures.priority_queue import PriorityQueue
from locations.location import Location
from .graph import Graph


class Dijkstra:
    """
    A class that implements Dijkstra's algorithm for finding the shortest path between two nodes.

    This implementation first takes a start vertex form which we will find all the shortest path to every other vertex.
    The direct weights/distances to every other node are predetermined and queued according to their distance, with
    the shortest distance being first in the queue.  As we visit each node in the queue, we determine whether any
    indirect paths exist that are shorter.  If so, our distance table, which tracks all paths for the start vertex, is
    updated accordingly.
    """

    def __init__(self, start: Location, graph: Graph):
        """
        Initializes a new instance of the Dijkstra class.

        Stores the shortest distance and shortest paths to every other node from the start node.  Three initializer
        functions are called to get the predetermined direct paths and then to ultimately execute the algorithm to find
        all the shortest paths and distances to every other node in the graph.
        :param start: The primary node from which the algorithm finds all shortest paths.
        :param graph: The graph that contains all applicable nodes, including the start node and every possible target
        node.
        """
        self._start = start
        self.graph = graph
        self.start_edges = self.graph.get_weighted_edges(self.start)
        self._distance_table = HashTable()
        self.all_paths = HashTable()
        self.priority_queue = PriorityQueue(is_max=False)
        self.unvisited = set()
        self.visited = set()
        self._closest_from_start = None
        self._initialize()
        self._execute()
        self._find_all_shortest_paths()

    def _initialize(self):
        """
        A function which initializes the weight to each vertex from the starting vertex with their associated values
        predetermined direct path values.
        :raises ValueError:  If the starting node is not found.
        """
        if self.start not in self.graph.get_all_vertices():
            raise ValueError('Starting location node not found.')
        start_weight, prev_vertex = 0, None
        self._distance_table[self._start] = (start_weight, prev_vertex)

        for vertex, weight in self.start_edges:
            self._distance_table[vertex] = (weight, self.start)
            self.priority_queue.insert(priority=weight, information=vertex)
            self.unvisited.add(vertex)

    @property
    def start(self) -> Location:
        """
        Returns the starting location node.
        :return: The starting location node.
        """
        return self._start

    @property
    def distance_table(self):
        """
        Returns the distance table containing the shortest distance to every vertex in the graph.
        :return: The distance table containing the shortest distance to every vertex in the graph.
        """
        return self._distance_table

    def _execute(self):
        """
        Contains the primary logic of Dijkstra's algorithm.

        This implementation iterates through each node in the graph starting from the node with the closest direct
        distance from the starting node.  The distance table and priority queue are as we visit each node, along the
        way finding the shortest paths and distances to every other node in the graph.

        While all target nodes are typically assigned with "infinity" values at the start using Dijkstra's algorithm,
        the initial data this program is provided has all direct distance values from each location to every  other
        location, forming a weighted, undirected complete graph.  We therefore initialize each target node with these
        weights instead of infinity.  This improves the algorithm's efficiency since there are typically several cases
        where the direct path is in fact the shortest path.

        **Complexity**:

        Time Complexity: O(n * log(n))

        Each node is fetched from the queue.  Since the queue's get() method includes heapify, this = O(log(n)).  The
        min. distance to current node is searched via hash function = O(1).  Then access each neighbor node = O(n-1).
        Next "if" statement will only check neighbor nodes that have not been visited = O(log(n-1)).  Finding the
        distance from current node to neighbor node and known distance from start to neighbor node are each via hash
        function = O(1). The distance through the current node in the next "if" statement would happen every time
        worst-case, therefore complexity = O(log( n-1)).  Changing a node in the hash table is simply accessing and
        altering the current value = O(1). Changing the priority of a node in the queue would = O(n * log(n)) since
        the "change_priority" method iterates through each node until the correct one is found, then performs a
        "heapify" on the queue.
        O(n * (log(n) + 1 + (n-1) + log(n-1) + 1 + 1) + n * log(n)) = O(n * log(n))

        Space Complexity:  O(1)

        "curr_node", "min_dist_to_curr", "neighbor_node", similar variables each have a space complexity = O(1). The
        weighted edges list returns a reference to a list stored in a hash, so does not add to the space complexity.
        Each time a node is removed form the "unvisited" list, it is also added to the "visited" list, and both lists
        were created outside this method, thereby contributing net 0 to space usage.  The total space complexity
        is therefore O(1) since no additional space is used beyond the variables holding single values.

        """
        while self.unvisited:
            curr_node = self.priority_queue.get()
            min_dist_to_curr = self.get_dist_and_prev(curr_node)[0]

            for edge_to_neighbor in self.graph.get_weighted_edges(curr_node):
                neighbor_node = edge_to_neighbor[0]

                if neighbor_node not in self.visited:
                    dist_curr_to_neighbor = edge_to_neighbor[1]
                    dist_start_to_neighbor = self.get_dist_and_prev(neighbor_node)[0]
                    if min_dist_to_curr + dist_curr_to_neighbor < dist_start_to_neighbor:
                        new_min_dist = round(min_dist_to_curr + dist_curr_to_neighbor, ndigits=3)
                        self._distance_table.change_node(unhashed_key=neighbor_node,
                                                         new_value=(new_min_dist, curr_node))
                        self.priority_queue.change_priority(priority=new_min_dist, information=neighbor_node)

            self.unvisited.remove(curr_node)
            self.visited.add(curr_node)

    def _find_all_shortest_paths(self):
        """
        Finds the shortest path to every other node in the graph.
        """
        for target_location, _ in self._distance_table.items():
            self.get_shortest_path(target_location)

    def get_shortest_path(self, target: Location):
        """
        This implementation first checks if the shortest path has already been found previously; if not, it traces
        its path backwards starting from the target node using the distance table and stores it in the 'all_paths' hash
        table to avoid duplicative calculations.

         **Complexity**:

        Time Complexity: O(n)

        We will assume the path to target node does not already exist, in which case it would simply be returned from
        the hash table at O(1) time complexity.
        Finding target node is accessing the distance hash table = O(1), and the "shortest_dist" simply returns the
        node's 1st tuple value = O(1).  Python's list's "append" method simply appends to the end of the list, which
        is O(1) time complexity.  Finding "prev_loc" is the same node's 2nd tuple value = O(1).
        Though the while loop in practice only loops a few times, it could hypothetically iterate through every other
        node if the shortest path required going through every other node, so complexity = O(n). The path is reverse,
        and Python's reverse() method slices and iterates through the list at a time complexity of O(n/2), or O(n).
        O(n + n) = O(n)

        Space Complexity:  O(m + n)

        A new "path" list is created which would hold no more than the total number of Locations = O(n). Adding the
        path to the "all_paths" hash table uses space equal to the length of the unhashed key string, which we will
        call 'm' since its storage usage is independent of the number of nodes.
        O(n) + O(m) = O(m + n)


        :param target: The target node to which the shortest path will be found from the starting node.
        :return: The path from the start node to the target node, the final element of which will be a tuple containing
        both the target node itself and the total weight/traversed distance.
        """
        if self.all_paths.has_node(target):
            return self.all_paths[target]

        path = []
        shortest_dist, prev_loc = self._distance_table[target]
        path.append((target, shortest_dist))

        while prev_loc:
            path.append(prev_loc)
            _, prev_loc = self._distance_table[prev_loc]

        path.reverse()
        self.all_paths[target] = path
        return path

    def get_dist_and_prev(self, target):
        """
        Returns the shortest known weight/distance from start node to target node as well as the node last visited
        before the target node.  If the shortest path was a direct path from start to target, then the start node would
        be the node last visited before the target node.
        :param target: The target node in the graph.
        :return: The edge weight and last node in the path to the target as a tuple.
        """
        weight, prev = self._distance_table[target]
        return weight, prev

    def get_closest_from_group(self, group: List[Location]):
        """
        Finds a node that is closest to the starting node among those included in the provided "group" list.
        :param group: The group of Location nodes to be searched against.
        :return: A tuple containing the closest node from the start among all nodes in the "group" list and its
        corresponding distance.
        """
        min_distance = math.inf
        curr_closest = None
        for location in group:
            distance, _ = self._distance_table[location]
            if distance != 0 and distance < min_distance:
                min_distance = distance
                curr_closest = location
        return curr_closest, min_distance
