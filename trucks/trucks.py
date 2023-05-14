from typing import List
from datetime import timedelta
from .truck import Truck
from packages.package import Package
from .driver import Driver
from locations.location import Location


class Trucks:
    def __init__(self, num_trucks: int, num_drivers: int, start_location: Location = None,
                 curr_time: timedelta = None):
        self._num_trucks = num_trucks
        self._num_drivers = num_drivers
        self._starting_location = start_location
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

    def find_available_truck(self, num_packages: int, current_time: timedelta):
        for truck in self.trucks:
            if truck.current_capacity - num_packages > 0 and truck.departure_time <= current_time:
                return truck
        return None

    def get_truck_by_id(self, truck_id):
        for truck in self.trucks:
            if truck.id == truck_id:
                return truck
        return None

    def load_packages(self, truck: Truck, packages: List[Package], travel_time: timedelta):
        if truck.current_capacity < 1:
            raise ValueError(f'Truck #{truck.id} is full; cannot load Packages {[p.id for p in packages]}')
        # TODO:  Likely need add'l logic that inserts if priority value < tail value
        for package in packages:
            if not package.truck_id:
                package.truck_id = truck.id
                if not package.space_already_allocated:
                    truck.current_capacity -= 1
            truck.packages_list.add_link(value=package.priority, package=package, travel_time=travel_time)

        # priority = package.priority
        # self.packages_queue.insert(priority=priority, information=package)
        # package.status = Package.STATUSES[2]
        # if not self.locations_to_packages_table.get_node(package.destination):
        #     self.locations_to_packages_table.add_node(unhashed_key=package.destination, value=[package])
        # else:
        #     curr_loc_list = self.locations_to_packages_table.get_node(package.destination).value
        #     curr_loc_list.append(package)
        # self.cumulative_priority_value += priority
        # if not is_preassigned:
        #     self.current_capacity -= 1
        return
