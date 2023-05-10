from .truck import Truck
from .driver import Driver


class Trucks:
    def __init__(self, num_trucks: int, num_drivers: int):
        self.num_trucks = num_trucks
        self.num_drivers = num_drivers
        self._all_trucks = []
        self.initialize_drivers_and_trucks()

    def initialize_drivers_and_trucks(self):
        for i in range(1, self.num_drivers + 1):
            driver = Driver(i)
            self.all_trucks.append(Truck(i, driver))

        for i in range(self.num_trucks - self.num_drivers):
            self.all_trucks.append(Truck(i + self.num_drivers + 1))

    @property
    def all_trucks(self):
        return self._all_trucks

    def get_truck_by_id(self, truck_id):
        for truck in self.all_trucks:
            if truck.id == truck_id:
                return truck
        return None
