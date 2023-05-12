import datetime
from .package import Package
from locations.locations import Locations
from data.packages_loader import PackagesLoader
from graph.dijkstra import Dijkstra
from priority_logic import priority_logic


class Packages:
    def __init__(self, package_csv: str, shortest_paths: Dijkstra, locations: Locations):
        self._packages = []
        self.loader = PackagesLoader(package_csv)
        self.shortest_paths = shortest_paths
        self.locations = locations
        self._priority_queue = None
        self._add_all_packages()
        self._assign_priority_values()

    def _add_all_packages(self):
        for dataset in self.loader.get_data():
            try:
                package_id = int(dataset[0])
                destination = self.locations.get_location(dataset[1].strip())
                if dataset[5] != 'EOD':
                    deadline = datetime.datetime.strptime(dataset[5], '%I:%M %p').time()
                else:
                    deadline = None
                kilos = int(dataset[6])
                requirement_notes = dataset[7]
                self.packages.append(Package(package_id, destination, deadline, kilos, requirement_notes))
            except (IndexError, ValueError) as e:
                print(f'Error {e} at {dataset}.')

    def _assign_priority_values(self):
        max_distance = self.shortest_paths.get_max_distance()

        for package in self.packages:
            destination = package.destination
            distance = self.shortest_paths.distance_table.get_node(destination).value[0]
            deadline = package.deadline
            priority_value = priority_logic.get_package_weight(distance, deadline, max_distance)
            package.priority = priority_value

        return self

    @property
    def packages(self):
        return self._packages

    @property
    def priority_queue(self):
        return self._priority_queue

    # FIXME:  May not need this after all
    def get_package_by_id(self, package_id):
        for package in self.packages:
            if package.id == package_id:
                return package
        return None
