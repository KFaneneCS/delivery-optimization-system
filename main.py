from packages.packages import Packages
from trucks.trucks import Trucks
from locations.locations import Locations
from data_structures.hash import HashTable
from data_structures.priority_queue import PriorityQueue

from graph.graph import Graph
from graph.dijkstra import Dijkstra

import csv

if __name__ == '__main__':
    csv_file = 'data/distance_table.csv'
    locations = Locations(csv_file)

    start_location = locations.get_location('HUB')
    target_location = locations.get_location('2010 W 500 S')
    graph = locations.get_graph()

    # graph.show_all_connections()

    dijkstra = Dijkstra(start_location, graph)
    print(dijkstra.get_shortest_path(target_location))