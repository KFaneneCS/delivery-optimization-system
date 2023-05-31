from datetime import timedelta
from typing import List

from locations.location import Location
from packages.package import Package
from .driver import Driver
from .truck import Truck


class Trucks:
    """
    A class that instantiates and manages a collection of Truck objects and provides a means of interaction with all
    Truck objects.
    """

    def __init__(self, num_trucks: int, num_drivers: int, start_location: Location = None,
                 start_time: timedelta = None):
        """
        Initializes a new instance of the Truck class.
        :param num_trucks: The total number of trucks in circulation.
        :param num_drivers: The number of available drivers to drive the trucks.
        :param start_location: The starting location of the trucks.
        :param start_time: The start time (business opening).
        """
        self._num_trucks = num_trucks
        self._num_drivers = num_drivers
        self._starting_location = start_location
        self._start_time = start_time
        self._trucks = []
        self._delayed_packages = []
        self._initialize_drivers_and_trucks()

    def _initialize_drivers_and_trucks(self):
        """
        Initialization function that instantiates all Packages and Drivers and assigns each driver to a truck.  Some
        trucks may begin with no drivers (None) if there are fewer drivers than trucks.
        :return:
        """
        for i in range(1, self.num_drivers + 1):
            driver = Driver(i)
            self.trucks.append(Truck(id_=i, driver=driver, current_location=self._starting_location))

        for i in range(self._num_trucks - self.num_drivers):
            self.trucks.append(Truck(id_=i + self.num_drivers + 1, current_location=self._starting_location))

    @property
    def num_drivers(self) -> int:
        """
        Returns the number of drivers.
        :return: The number of drivers.
        """
        return self._num_drivers

    @property
    def trucks(self) -> List:
        """
        Returns the list of trucks.

        A list is used instead of a hash table due to the minimal number of trucks used. If user anticipates several
        trucks, it may be appropriate to change this to a hash table data structure.
        :return: the list of trucks.
        """
        return self._trucks

    @property
    def delayed_packages(self) -> List:
        """
        Returns the list of packages that are initially delayed and on their way to the hub.
        :return: the list of packages that are initially delayed and on their way to the hub.
        """
        return self._delayed_packages

    def add_delayed_package(self, package: Package):
        """
        Adds a package to the list of delayed packages.
        :param package: The package to be added to the delayed packages list.
        :raises ValueError: If package value is not a Package object.
        """
        if not isinstance(package, Package):
            raise ValueError('Invalid "package" value.')
        self._delayed_packages.append(package)

    def find_available_truck(self, assoc_packages: List[Package], current_time: timedelta):
        """
        A function that takes a list of packages and the current tracked time and finds the first available truck that
        has capacity and meets time requirements to assign them to.
        :param assoc_packages: The list of packages for which the best available truck will be found.
        :param current_time: The current time.
        :return: The first available truck, otherwise None.
        :raises ValueError: If current time provided is not timedelta object.
        """
        if not isinstance(current_time, timedelta):
            raise ValueError('Invalid "current time" value.')
        for package in assoc_packages:
            if package.truck_id:
                return self.get_truck_by_id(package.truck_id)

        num_packages = len(assoc_packages)
        available_trucks = [truck for truck in self._trucks if (
                truck.departure_time <= current_time or not truck.driver) and truck.current_capacity >= num_packages]
        return available_trucks[0] if available_trucks else None

    def get_truck_by_id(self, truck_id: int):
        """
        Returns the truck corresponding to the provided truck ID, otherwise None if it does not exist.
        :param truck_id: The ID of the truck to return.
        :return: The Truck object corresponding to the provided truck ID.
        """
        if not isinstance(truck_id, int):
            raise ValueError('Invalid "truck ID" value.')

        for truck in self.trucks:
            if truck.id == truck_id:
                return truck
        return None

    def get_total_mileage(self):
        """
        Returns the rounded total miles traveled for all trucks.
        :return: The rounded total miles traveled for all trucks.
        """
        return round(sum([truck.miles_traveled for truck in self._trucks]), ndigits=2)
