from datetime import datetime, date, time, timedelta
from locations.location import Location
from packages.package import Package
from data_structures.priority_queue import MaxPriorityQueue
from .driver import Driver


class Truck:
    def __init__(self, id_: int, driver: Driver = None, current_time: timedelta = timedelta(hours=8, minutes=0),
                 current_location: Location = None):
        self._id = id_
        self._driver = driver
        self._current_time = current_time
        self._packages = MaxPriorityQueue()
        self._delivered_packages = []
        self._return_time = None
        self._current_location = current_location
        self._MAX_CAPACITY = 16
        self._current_capacity = self.MAX_CAPACITY

    def __str__(self):
        return f'Truck(ID={self._id} | driver={self._driver} | ' \
               f'location={self._current_location} | capacity={self._current_capacity})'

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
    def packages(self):
        return self._packages

    @property
    def delivered_packages(self):
        return self._delivered_packages

    @property
    def return_time(self):
        return self._return_time

    @return_time.setter
    def return_time(self, return_time: datetime):
        if not isinstance(return_time, datetime):
            raise ValueError('Invalid "current time" value.')
        self._return_time = return_time

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
        self.packages.insert(priority=priority, information=package)
        if not is_preassigned:
            self.current_capacity -= 1
        # print(f'{package} ADDED TO TRUCK #{self.id} with CAPACITY #{self.current_capacity}')
        return
