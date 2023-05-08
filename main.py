from packages.packages import Packages
from trucks.trucks import Trucks
from locations.locations import Locations
from data_structures.hash import HashTable
from data_structures.priority_queue import MinPriorityQueue
from statistics import mean
from priority_logic import priority_logic
import datetime

from graph.graph import Graph
from graph.dijkstra import Dijkstra

if __name__ == '__main__':
    locations_file = 'data/distance_table.csv'
    packages_file = 'data/package_file.csv'
    locations = Locations(locations_file)

    hub = locations.get_location('HUB')
    target_location = locations.get_location('2010 W 500 S')
    graph = locations.get_graph()

    # graph.show_all_connections()

    shortest_paths = Dijkstra(hub, graph)
    # print(f'longest distance from HUB:  {shortest_paths.get_max_distance()}')
    # print(shortest_paths.get_shortest_path(target_location))
    # print('\n\n\n')
    # for x in shortest_paths.get_dist_table().get_all():
    #     print(x)

    packages = Packages(packages_file, shortest_paths, locations)

    # t1 = datetime.time(9, 0)
    # print(priority_logic.get_package_weight(5, t1, shortest_paths.get_max_distance()))


