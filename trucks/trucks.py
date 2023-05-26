from datetime import timedelta
from typing import List

from locations.location import Location
from packages.package import Package
from .driver import Driver
from .truck import Truck


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
