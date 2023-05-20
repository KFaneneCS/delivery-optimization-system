from datetime import datetime, timedelta
from .package import Package
from locations.locations import Locations
from data_structures.hash import HashTable
from data.packages_loader import PackagesLoader
from graph.dijkstra import Dijkstra


class Packages:
    def __init__(self, package_csv: str, locations: Locations):
        self._packages = []
        self._loader = PackagesLoader(package_csv)
        self._locations = locations
        self._priority_queue = None
        self._location_to_packages_table = HashTable()
        self._add_all_packages()
        self._associate_packages_to_locations()

    def _add_all_packages(self):
        for dataset in self._loader.get_data():
            try:
                package_id = int(dataset[0])
                destination = self._locations.get_location(dataset[1].strip())
                if dataset[5] != 'EOD':
                    deadline_dt = datetime.strptime(dataset[5], '%I:%M %p').time()
                    deadline = timedelta(hours=deadline_dt.hour, minutes=deadline_dt.minute)
                else:
                    deadline = None
                kilos = int(dataset[6])
                requirement_notes = dataset[7]
                self.packages.append(Package(package_id, destination, deadline, kilos, requirement_notes))
            except (IndexError, ValueError) as e:
                print(f'Error {e} at {dataset}.')

    def _associate_packages_to_locations(self):
        for package in self._packages:
            destination = package.destination
            if not self._location_to_packages_table[destination]:
                self._location_to_packages_table[destination] = [package]
            else:
                self._location_to_packages_table[destination].value.append(package)

    @property
    def packages(self):
        return self._packages

    @property
    def priority_queue(self):
        return self._priority_queue

    @property
    def locations_to_packages_table(self):
        return self._location_to_packages_table

    def get_num_packages(self):
        return len(self._packages)

    def get_package_by_id(self, package_id):
        for package in self.packages:
            if package.id == package_id:
                return package
        return None

    def get_all_statuses_by_time(self):
        for package in self._packages:
            yield package, package.status_at_times
