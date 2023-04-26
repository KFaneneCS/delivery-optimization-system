from packages.packages import Packages
from trucks.trucks import Trucks
from locations.locations import Locations
from hash.hash import HashTable
from graph.graph import Graph
import csv

if __name__ == '__main__':
    # testing hash table
    hash_table = HashTable(10)  # TODO:  Change size to 100
    hash_table.add('hello', 'world')
    hash_table.add('ChatGPW', (10, 20))

    hash2 = HashTable(3)
    hash2.add('max', 100)
    hash2.add('min', 10)
    hash2.add('location', 'Super Main street')

    hash_table.add(123, hash2.get_all())
    # print(hash_table.get_value('ChatGPW'))
    # for h in hash_table.get_all():
    #     print(h)

    # testing locations
    locations = Locations()
    locations.add_all_locations('data/distance_table.csv')

    # for l in locations.get_locations():
    #     print(l)

    # for location in locations.get_all_locations():
    #     print(f'current location == {location}')
    #     for x in location.get_adjacency_list():
    #         print((str(x[0]), x[1]))




