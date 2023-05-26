from datetime import timedelta
from typing import List

from data_structures.hash import HashTable
from data_structures.priority_queue import PriorityQueue
from locations.location import Location
from packages.package import Package
from .driver import Driver


class Truck:
    def __init__(self, id_: int, driver: Driver = None, current_time: timedelta = timedelta(hours=8, minutes=0),
                 current_location: Location = None):
        self._id = id_
        self._driver = driver
        self._current_time = current_time
        self._current_location = None
        self._location_by_time_list = []
        self.set_current_location(current_location, current_time, 0)
        self._tracked_current_time = self._current_time
        self._assigned_packages = []
        self._packages_queue = PriorityQueue(is_max=False)
        self._miles_traveled = 0
        self._locations_to_packages_table = HashTable()
        self._seen_packages = HashTable()
        self._delivered_packages = []
        self._departure_time = self._current_time
        self._MAX_CAPACITY = 16
        self._current_capacity = self.MAX_CAPACITY

    def __str__(self):
        return f'''Truck ID={self._id}
        Driver={self._driver}
        Current Location={self._current_location.address}
        Departure Time={self._departure_time}
        Current Time={self._current_time}
        Miles Traveled={self._miles_traveled}
        Capacity={self._current_capacity}'''

    @property
    def id(self):
        return self._id

    @property
    def driver(self):
        return self._driver

    @driver.setter
    def driver(self, new_driver: Driver):
        self._driver = new_driver

    @property
    def current_time(self):
        return self._current_time

    @current_time.setter
    def current_time(self, current_time: timedelta):
        if not isinstance(current_time, timedelta):
            raise ValueError('Invalid "current time" value.')
        self._current_time = current_time

    @property
    def current_location(self):
        return self._current_location

    @current_location.setter
    def current_location(self, current_location: Location):
        if not isinstance(current_location, Location):
            raise ValueError('Invalid "current location" value.')
        self._current_location = current_location

    @property
    def tracked_current_time(self):
        return self._tracked_current_time

    @tracked_current_time.setter
    def tracked_current_time(self, tracked_time: timedelta):
        if not isinstance(tracked_time, timedelta):
            raise ValueError('Invalid "tracked current time" value.')
        self._tracked_current_time = tracked_time

    @property
    def assigned_packages(self):
        return self._assigned_packages

    @assigned_packages.setter
    def assigned_packages(self, assigned_packages: List[Package]):
        self._assigned_packages = assigned_packages

    @property
    def packages_queue(self):
        return self._packages_queue

    @property
    def miles_traveled(self):
        return self._miles_traveled

    @miles_traveled.setter
    def miles_traveled(self, miles: float):
        if not isinstance(miles, (float, int)) or miles < 0:
            raise ValueError('Invalid "miles traveled" value.')
        self._miles_traveled = miles

    @property
    def locations_to_packages_table(self):
        return self._locations_to_packages_table

    @property
    def seen_packages(self):
        return self._seen_packages

    @property
    def delivered_packages(self):
        return self._delivered_packages

    @property
    def location_by_time_list(self):
        return self._location_by_time_list

    @property
    def departure_time(self):
        return self._departure_time

    @departure_time.setter
    def departure_time(self, departure_time: timedelta):
        if not isinstance(departure_time, timedelta):
            raise ValueError('Invalid "departure time" value.')
        self._departure_time = departure_time
        self._location_by_time_list.pop()
        self.set_current_location(self._current_location, self._departure_time, 0)

    @property
    def MAX_CAPACITY(self):
        return self._MAX_CAPACITY

    @property
    def current_capacity(self):
        return self._current_capacity

    @current_capacity.setter
    def current_capacity(self, new_curr_capacity: int):
        if not isinstance(new_curr_capacity, int):
            raise ValueError('Invalid "new current capacity value".')
        if new_curr_capacity < 0:
            raise ValueError('Cannot exceed maximum capacity.')

        self._current_capacity = new_curr_capacity

    def set_current_location(self, curr_location: Location, curr_time: timedelta, miles_traveled: float):
        self._current_location = curr_location
        self._location_by_time_list.append((curr_location, curr_time, miles_traveled))

    def add_assigned_package(self, package: Package):
        if self.current_capacity - len(self._assigned_packages) == 0:
            raise RuntimeError(f'Not enough capacity in truck #{self._id} to assign package #{package.id}')
        if package.assigned:
            raise RuntimeError(f'Package #{package.id} was already assigned!')

        self._assigned_packages.append(package)
        package.assigned = True

    def remove_assigned_package(self, package: Package):
        if package not in self._assigned_packages:
            raise ValueError(f'Package #{package.id} is not assigned to truck #{self._id}')
        else:
            self._assigned_packages.remove(package)
            package.assigned = False

    def load_bundle(self, packages: List[Package], distance_to_next: float, curr_travel_distance: float):
        if not isinstance(distance_to_next, (int, float)):
            raise ValueError('Invalid "distance to next" value.')
        if not isinstance(curr_travel_distance, (int, float)):
            raise ValueError('Invalid "current travel distance" value.')
        if not packages:
            return

        num_packages = len(packages)
        if self._current_capacity - num_packages < 0:
            raise RuntimeError(f'Truck {self._id} does not have enough capacity to load:\n{packages}')
        self.packages_queue.insert(priority=curr_travel_distance, information=(packages, distance_to_next))
        self._current_capacity -= num_packages
        if packages and self._driver:
            for package in packages:
                if package.status == 'En Route':
                    raise RuntimeError(f'Package #{package.id} is already En Route!')
                package.set_status(Package.STATUSES[2], self._departure_time)
                package.truck_id = self._id

    def deliver_package(self, package: Package, current_time: timedelta):
        if package.status == 'Delivered':
            raise RuntimeError(f'Package #{package.id} was already delivered!  ({current_time})')
        package.set_status(Package.STATUSES[3], current_time)
        self._delivered_packages.append(package)
        self._current_capacity += 1
