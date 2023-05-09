from datetime import time


class Driver:
    def __init__(self, id_):
        self.id_ = id_

    def __repr__(self):
        return f'Driver(ID={self.id_})'


class Truck:
    def __init__(self, id_, driver):
        self.id_ = id_
        self.driver = driver
        self.packages = []
        self.return_time = None
        self.MAX_CAPACITY = 16
        self.SPEED = 18

    def __repr__(self):
        return f'Truck(ID={self.id_} | driver={self.driver} | # packages={len(self.packages)})'

    def get_id(self):
        return self.id_

    def get_driver(self):
        return self.driver

    def get_packages(self):
        return self.packages

    def set_return_time(self, return_time: time):
        self.return_time = return_time
        return self.return_time
