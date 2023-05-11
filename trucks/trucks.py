from .truck import Truck
from .driver import Driver
from locations.location import Location


class Trucks:
    def __init__(self, num_trucks: int, num_drivers: int, starting_location: Location = None):
        self.num_trucks = num_trucks
        self._num_drivers = num_drivers
        self.starting_location = starting_location
        self._trucks = []
        self.initialize_drivers_and_trucks()

    def initialize_drivers_and_trucks(self):
        for i in range(1, self.num_drivers + 1):
            driver = Driver(i)
            self.trucks.append(Truck(id_=i, driver=driver, current_location=self.starting_location))

        for i in range(self.num_trucks - self.num_drivers):
            self.trucks.append(Truck(id_=i + self.num_drivers + 1, current_location=self.starting_location))

    @property
    def trucks(self):
        return self._trucks

    @property
    def num_drivers(self):
        return self._num_drivers

    def get_truck_by_id(self, truck_id):
        for truck in self.trucks:
            if truck.id == truck_id:
                return truck
        return None
