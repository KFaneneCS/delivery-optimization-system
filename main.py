from packages.packages import Packages
from trucks.trucks import Trucks
from locations.locations import Locations
from hash.hash import HashTable
from graph.graph import Graph
from graph.dijkstra import Dijkstra

import csv

if __name__ == '__main__':
    csv_file = 'data/distance_table.csv'
    locations = Locations(csv_file)

    hub = locations.get_location('HUB')
    graph = locations.get_graph()

    dijkstra = Dijkstra(hub, '300 State St', graph)
    dijkstra.execute()
