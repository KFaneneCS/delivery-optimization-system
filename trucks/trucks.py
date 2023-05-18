from typing import List
from datetime import timedelta
from data_structures.linked_list import LinkedList
from .truck import Truck
from packages.package import Package
from .driver import Driver
from locations.location import Location


class Trucks:
    def __init__(self, num_trucks: int, num_drivers: int, start_location: Location = None,
                 start_time: timedelta = None, curr_time: timedelta = None):
        self._num_trucks = num_trucks
        self._num_drivers = num_drivers
        self._starting_location = start_location
        self._start_time = start_time
        self._curr_time = curr_time
        self._trucks = []
        self._delayed_packages = []
        self._initialize_drivers_and_trucks()

    def _initialize_drivers_and_trucks(self):
        for i in range(1, self.num_drivers + 1):
            driver = Driver(i)
            self.trucks.append(Truck(id_=i, driver=driver, current_location=self._starting_location))

        for i in range(self._num_trucks - self.num_drivers):
            self.trucks.append(Truck(id_=i + self.num_drivers + 1, current_location=self._starting_location))

    @property
    def num_drivers(self):
        return self._num_drivers

    @property
    def trucks(self):
        return self._trucks

    @property
    def delayed_packages(self):
        return self._delayed_packages

    def add_delayed_package(self, package: Package):
        self._delayed_packages.append(package)

    def find_available_truck(self, assoc_packages: List[Package], current_time: timedelta):
        for package in assoc_packages:
            if package.truck_id:
                return self.get_truck_by_id(package.truck_id)

        num_packages = len(assoc_packages)
        available_trucks = [truck for truck in self._trucks if (truck.departure_time <= current_time or not truck.driver) and truck.current_capacity >= num_packages]
        return available_trucks[0] if available_trucks else None

    def get_truck_by_id(self, truck_id):
        for truck in self.trucks:
            if truck.id == truck_id:
                return truck
        return None

    def load_packages(self, packages: List[Package], current_time: timedelta):
        for package in packages:
            truck_id = package.truck_id
            truck = self.get_truck_by_id(truck_id)
            if not truck:
                raise ValueError(f'Package #{package.id} missing Truck assignment.')
            if not package.space_already_allocated:
                truck.current_capacity -= 1
            if package.deadline is None:
                # print(f'Package #{package.id} with NO deadline ---> {truck.id}')
                truck.packages_without_deadlines_queue.insert(priority=package.priority, information=package)
            else:
                # print(f'Package #{package.id} WITH deadline ---> {truck.id}')
                truck.packages_with_deadlines_queue.insert(priority=package.priority, information=package)
            # truck.test_queue.insert(priority=package.priority, information=package)

            if truck.driver and truck.departure_time <= self._start_time:
                package.set_status(Package.STATUSES[2], current_time)
        return
