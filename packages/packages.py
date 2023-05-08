import datetime

from .package import Package
from data_structures.priority_queue import MaxPriorityQueue
from data_structures.hash import HashTable
from data.packages_loader import PackagesLoader
from priority_logic import priority_logic


class Packages:
    def __init__(self, package_csv, shortest_paths, locations):
        self.packages = []
        self.loader = PackagesLoader(package_csv)
        self.shortest_paths = shortest_paths
        self.locations = locations
        self._add_all_packages()
        self._assign_priority_values()

    def _add_all_packages(self):
        for dataset in self.loader.get_data():
            try:
                package_id = int(dataset[0])
                address = self.locations.get_location(dataset[1].strip())
                city = dataset[2]
                state = dataset[3]
                zip_code = dataset[4]
                if dataset[5] != 'EOD':
                    deadline = datetime.datetime.strptime(dataset[5], '%I:%M %p').time()
                else:
                    deadline = None
                kilos = int(dataset[6])
                self.packages.append(Package(package_id, address, city, state, zip_code, deadline, kilos))
            except (IndexError, ValueError) as e:
                print(f'Error {e} at {dataset}.')

    def _assign_priority_values(self):
        max_distance = self.shortest_paths.get_max_distance()
        # for end_location, (shortest_distance, _) in self.shortest_paths.get_distance_table().items():
        #

        for package in self.packages:
            destination = package.get_destination()
            print(f'DEST:   {destination}')
            # print(self.shortest_paths.get_dist_table().get_node(destination))
            distance = self.shortest_paths.get_dist_table().get_node(destination).value[0]
            deadline = package.get_deadline()
            priority_value = priority_logic.get_package_weight(distance, deadline, max_distance)
            print(f'Package {package} with priority value {priority_value}')

        # for key, dist_to_neighbor in self.shortest_paths.get_distance_table():
        #     distance = dist_to_neighbor[0]
        #     neighbor_location = dist_to_neighbor[1]
        #     # priority_logic.get_package_weight(distance, neighbor_location)
        #     # print(f'distance:  {distance} ~~ neighbor:  {neighbor_location}')

    def get_packages(self):
        return self.packages
