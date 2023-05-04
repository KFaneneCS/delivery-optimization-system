from .truck import Truck, Driver


class Trucks:
    def __init__(self):
        self.trucks = []
        self.initialize_drivers_and_trucks()

    def initialize_drivers_and_trucks(self):
        driver1 = Driver(1)
        driver2 = Driver(2)
        truck1 = Truck(1, driver1)
        truck2 = Truck(2, driver2)
        truck3 = Truck(3, None)
        self.trucks.append(truck1)
        self.trucks.append(truck2)
        self.trucks.append(truck3)
