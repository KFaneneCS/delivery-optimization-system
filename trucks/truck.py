from datetime import time


class Driver:
    def __init__(self, id_):
        self.id_ = id_

    def __repr__(self):
        return f'Driver(ID={self.id_})'


class Truck:
    def __init__(self, id_: int, driver: Driver):
        self._id = id_
        self._driver = driver
        self._packages = []
        self._return_time = None
        self._MAX_CAPACITY = 16
        self._SPEED = 18

    def __repr__(self):
        return f'Truck(ID={self.id} | driver={self.driver} | # packages={len(self.packages)})'

    @property
    def id(self):
        return self._id

    @property
    def driver(self):
        return self.driver

    @property
    def packages(self):
        return self.packages

    @property
    def return_time(self):
        return self._return_time

    @return_time.setter
    def return_time(self, return_time: time):
        self._return_time = return_time
