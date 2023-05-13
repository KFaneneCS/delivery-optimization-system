from datetime import datetime, date, time, timedelta
from locations.location import Location
from packages.package import Package
from data_structures.priority_queue import MaxPriorityQueue
from data_structures.linked_list import LinkedList
from data_structures.hash import HashTable
from .driver import Driver


class Truck:
    def __init__(self, id_: int, driver: Driver = None, current_time: timedelta = timedelta(hours=8, minutes=0),
                 current_location: Location = None):
        self._id = id_
        self._driver = driver
        self._current_time = current_time
        self._miles_traveled = 0
        self._packages_list = LinkedList()
        self._locations_to_packages_table = HashTable()
        # self._cumulative_priority_value = 0
        self._delivered_packages = []
        self._departure_time = current_time
        self._current_location = current_location
        self._MAX_CAPACITY = 16
        self._current_capacity = self.MAX_CAPACITY

    # def __str__(self):
    #     return f'''Truck ID={self.id}
    #     Driver={self.driver}
    #     Current Location={self.current_location.address}
    #     Next Stop={self.packages_queue.peek()}
    #     Return Time={self.departure_time}
    #     Capacity={self.current_capacity}'''

    @property
    def id(self):
        return self._id

    @property
    def driver(self):
        return self._driver

    @property
    def current_time(self):
        return self._current_time

    @current_time.setter
    def current_time(self, current_time: datetime):
        if not isinstance(current_time, datetime):
            raise ValueError('Invalid "current time" value.')
        self._current_time = current_time

    @property
    def miles_traveled(self):
        return self._miles_traveled

    @miles_traveled.setter
    def miles_traveled(self, miles: float):
        if not isinstance(miles, (float, int)):
            raise ValueError('Invalid "miles traveled" value.')
        self._miles_traveled = miles

    @property
    def packages_list(self):
        return self._packages_list

    @property
    def locations_to_packages_table(self):
        return self._locations_to_packages_table

    # def add_package_id(self, package_id: int):
    #     if not isinstance(package_id, int):
    #         raise ValueError('Invalid "package ID" value')
    #     self.package_ids.add_node(package_id, False)
    #     return
    #
    # def remove_package_id(self, package_id: int):
    #     if not isinstance(package_id, int):
    #         raise ValueError('Invalid "package ID" value')
    #     if package_id in self._package_ids:
    #         self._package_ids.remove(package_id)
    #     return

    # @property
    # def cumulative_priority_value(self):
    #     return self._cumulative_priority_value
    #
    # @cumulative_priority_value.setter
    # def cumulative_priority_value(self, new_value):
    #     if not isinstance(new_value, (float, int)):
    #         raise ValueError('Invalid "cumulative priority value".')
    #     self._cumulative_priority_value = new_value

    @property
    def delivered_packages(self):
        return self._delivered_packages

    @property
    def departure_time(self):
        return self._departure_time

    @departure_time.setter
    def departure_time(self, departure_time: timedelta):
        if not isinstance(departure_time, timedelta):
            raise ValueError('Invalid "departure time" value.')
        self._departure_time = departure_time

    @property
    def current_location(self):
        return self._current_location

    @current_location.setter
    def current_location(self, current_location: Location):
        if not isinstance(current_location, Location):
            raise ValueError('Invalid "current location" value.')
        self._current_location = current_location

    @property
    def MAX_CAPACITY(self):
        return self._MAX_CAPACITY

    @property
    def current_capacity(self):
        return self._current_capacity

    @current_capacity.setter
    def current_capacity(self, new_curr_capacity: int):
        if not isinstance(new_curr_capacity, int) or new_curr_capacity < 0:
            raise ValueError('Invalid "new current capacity value".')
        if new_curr_capacity > self.MAX_CAPACITY:
            raise ValueError('Cannot exceed maximum capacity.')

        self._current_capacity = new_curr_capacity

    def load_package(self, package: Package, is_preassigned: bool = False):
        if not is_preassigned and self.current_capacity == 0:
            raise ValueError(f'Truck #{self.id} is full; cannot load Package #{package.id}')
        priority = package.priority
        self.packages_queue.insert(priority=priority, information=package)
        package.status = Package.STATUSES[2]
        if not self.locations_to_packages_table.get_node(package.destination):
            self.locations_to_packages_table.add_node(unhashed_key=package.destination, value=[package])
        else:
            curr_loc_list = self.locations_to_packages_table.get_node(package.destination).value
            curr_loc_list.append(package)
        self.cumulative_priority_value += priority
        if not is_preassigned:
            self.current_capacity -= 1
        return
