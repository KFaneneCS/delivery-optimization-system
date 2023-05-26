import bisect
from datetime import datetime, timedelta

from data.packages_loader import PackagesLoader
from data_structures.hash import HashTable
from locations.locations import Locations
from .package import Package


class Packages:
    def __init__(self, package_csv: str, locations: Locations):
        self._packages = HashTable(80)
        self._packages_list = []
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
                new_package = Package(package_id, destination, deadline, kilos, requirement_notes)
                self._packages[package_id] = new_package
            except (IndexError, ValueError) as e:
                print(f'Error {e} at {dataset}.')

    def _associate_packages_to_locations(self):
        for _, package in self._packages.items():
            destination = package.destination
            if not self._location_to_packages_table[destination]:
                self._location_to_packages_table[destination] = [package]
            else:
                self._location_to_packages_table[destination].value.append(package)

    @property
    def locations_to_packages_table(self):
        return self._location_to_packages_table

    def get_all(self):
        if not self._packages_list:
            for _, package in self._packages.items():
                bisect.insort(self._packages_list, package, key=lambda p: p.id)
        return self._packages_list

    def get_by_id(self, id_: int):
        if not isinstance(id_, int):
            raise ValueError('Invalid ID value.')

        return self._packages[id_].value

    def get_num_packages(self):
        return self._packages.get_size()

    def get_all_statuses_by_time(self):
        for package in self._packages:
            yield package, package.status_at_times
