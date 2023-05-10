from datetime import time
from packages.package import Package
from data_structures.priority_queue import MaxPriorityQueue
from .driver import Driver


class Truck:
    def __init__(self, id_: int, driver: Driver = None):
        self._id = id_
        self._driver = driver
        self._packages = MaxPriorityQueue()
        self._return_time = None
        self._at_hub = True
        self._MAX_CAPACITY = 16
        self._curr_capacity = self.MAX_CAPACITY
        self._SPEED = 18

    def __str__(self):
        return f'Truck(ID={self.id} | driver={self.driver} | at HUB={self.at_hub})'

    @property
    def id(self):
        return self._id

    @property
    def driver(self):
        return self._driver

    @property
    def packages(self):
        return self._packages

    @property
    def return_time(self):
        return self._return_time

    @return_time.setter
    def return_time(self, return_time: time):
        self._return_time = return_time

    @property
    def at_hub(self):
        return self._at_hub

    @at_hub.setter
    def at_hub(self, is_at_hub: bool):
        self._at_hub = is_at_hub

    @property
    def MAX_CAPACITY(self):
        return self._MAX_CAPACITY

    @property
    def curr_capacity(self):
        return self._curr_capacity

    @curr_capacity.setter
    def curr_capacity(self, new_curr_capacity: int):
        if not isinstance(new_curr_capacity, int) or new_curr_capacity < 0:
            raise ValueError('Invalid "new current capacity value".')
        if new_curr_capacity > self.MAX_CAPACITY:
            raise ValueError('Cannot exceed maximum capacity.')

        self._curr_capacity = new_curr_capacity

    @property
    def SPEED(self):
        return self._SPEED

    def load_package(self, package: Package):
        priority = package.priority
        self.packages.insert(priority=priority, information=package)
        return

