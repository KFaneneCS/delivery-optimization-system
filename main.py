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

    start_location = locations.get_location('300 State St')
    target_location = locations.get_location('6351 South 900 East')
    graph = locations.get_graph()

    # graph.show_all_connections()

    dijkstra = Dijkstra(start_location, target_location, graph)
    dijkstra.execute()


    # pq = PriorityQueue()
    # pq.insert(5, 'Bob')
    # pq.insert(3.0, 'Alice')
    # pq.insert(100, 'Joey')
    # pq.insert(1)
    # pq.insert(5.1, 'Tanisha')
    #
    # pq.print_queue()

    # pq.print_queue()
    # for _ in range(5):
    #     print(pq.get())
