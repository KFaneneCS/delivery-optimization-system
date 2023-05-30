from datetime import timedelta
from typing import List

from data_structures.priority_queue import PriorityQueue
from locations.location import Location
from packages.package import Package
from .driver import Driver

MAX_CAPACITY = 16


class Truck:
    """
    A class representing a truck that is used to deliver packages to various locations along a specified route by a
    driver.
    """

    def __init__(self, id_: int, driver: Driver = None, current_time: timedelta = timedelta(hours=8, minutes=0),
                 current_location: Location = None):
        """
        Initializes a new instance of the Truck class.
        :param id_: The ID number of the truck.
        :param driver: The driver of the truck as a Driver object.
        :param current_time: The current time of the truck.
        :param current_location: The current location of the truck.
        """
        self._id = id_
        self._driver = driver
        self._current_time = current_time
        self._current_location = None
        self._location_by_time_list = []
        self.set_current_location(current_location, current_time, 0)
        self._tracked_current_time = self._current_time
        self._assigned_packages = []
        self._packages_queue = PriorityQueue(is_max=False)
        self._miles_traveled = 0
        self._delivered_packages = []
        self._departure_time = self._current_time
        self._MAX_CAPACITY = 16
        self._current_capacity = MAX_CAPACITY

    def __str__(self):
        """
        Returns the string representation of the Truck object.
        :return:
        """
        return f'''Truck ID={self._id}
        Driver={self._driver}
        Current Location={self._current_location.address}
        Departure Time={self._departure_time}
        Current Time={self._current_time}
        Miles Traveled={self._miles_traveled}
        Capacity={self._current_capacity}'''

    @property
    def id(self) -> int:
        """
        Returns the ID associated with the Truck.
        :return: The ID associated with the Truck.
        """
        return self._id

    @property
    def driver(self) -> Driver:
        """
        Returns the driver of the truck.
        :return: The driver of the truck.
        """
        return self._driver

    @driver.setter
    def driver(self, new_driver: Driver):
        """
        Sets a new driver for the truck.
        :param new_driver: The new driver to be associated with the truck.
        :raises ValueError:  If new driver value is not a Driver object.
        """
        if new_driver is not None and not isinstance(new_driver, Driver):
            raise ValueError('Invalid "driver" value.')
        self._driver = new_driver

    @property
    def current_time(self):
        """
        Returns the current time of the truck.
        :return: The current time of the truck.
        """
        return self._current_time

    @current_time.setter
    def current_time(self, current_time: timedelta):
        """
        Sets the current time of the truck.
        :param current_time: The current time as a timedelta object to be associated with the truck.
        :raises ValueError:  If current time value is not a timedelta object.
        """
        if not isinstance(current_time, timedelta):
            raise ValueError('Invalid "current time" value.')
        self._current_time = current_time

    @property
    def current_location(self) -> Location:
        """
        Returns the current location of the truck.
        :return: The current location of the truck.
        """
        return self._current_location

    @current_location.setter
    def current_location(self, current_location: Location):
        """
        Sets the current location for the truck.
        :param current_location: The current location of the truck.
        :raises ValueError: If the current location value is not a Location object.
        """
        if not isinstance(current_location, Location):
            raise ValueError('Invalid "current location" value.')
        self._current_location = current_location

    @property
    def tracked_current_time(self) -> timedelta:
        """
        Returns the tracked current time of the truck, which is intended to track hypothetical time passage and not
        the actual elapsed time. The true "current time" remains unchanged.
        :return: The tracked current time of the truck, which is intended to track hypothetical time passage and not
        the actual elapsed time. The true "current time" remains unchanged.
        """
        return self._tracked_current_time

    @tracked_current_time.setter
    def tracked_current_time(self, tracked_time: timedelta):
        """
        Sets the tracked current time of the truck.
        :param tracked_time: The tracked current time to be associated with the truck.
        :raises ValueError: If the tracked time value is not a timedelta object.
        """
        if not isinstance(tracked_time, timedelta):
            raise ValueError('Invalid "tracked current time" value.')
        self._tracked_current_time = tracked_time

    @property
    def assigned_packages(self) -> List:
        """
        Returns the packages assigned to the truck before loading.
        :return: The packages assigned to the truck before loading.
        """
        return self._assigned_packages

    @assigned_packages.setter
    def assigned_packages(self, assigned_packages: List[Package]):
        """
        Sets the assigned packages for the truck.

        Intended to simplify alteration of the packages via list comprehension. To assign packages, the
        "add_assigned_package" method should be used.
        :param assigned_packages: The list of packages to assign to the truck.
        """
        self._assigned_packages = assigned_packages

    @property
    def packages_queue(self) -> PriorityQueue:
        """
        Returns the queue of packages to be delivered.
        :return: The queue of packages to be delivered.
        """
        return self._packages_queue

    @property
    def miles_traveled(self) -> float:
        """
        Returns the mileage of the truck.
        :return: the mileage of the truck.
        """
        return self._miles_traveled

    @miles_traveled.setter
    def miles_traveled(self, miles: float):
        """
        Sets the current mileage of the truck
        :param miles: The number of miles traveled.
        :raises ValueError: If value of miles is not an integer or float.
        """
        if not isinstance(miles, (float, int)) or miles < 0:
            raise ValueError('Invalid "miles traveled" value.')
        self._miles_traveled = miles

    @property
    def delivered_packages(self) -> List:
        """
        Returns a list of delivered packages.
        :return: A list of delivered packages.
        """
        return self._delivered_packages

    @property
    def location_by_time_list(self) -> List:
        """
        Returns a list of tuples which contain the truck's current location at a particular time.
        :return: A list of tuples which contain the truck's current location at a particular time.
        """
        return self._location_by_time_list

    @property
    def departure_time(self) -> timedelta:
        """
        Returns the departure time of the truck from the hub.
        :return: The departure time of the truck from the hub.
        """
        return self._departure_time

    @departure_time.setter
    def departure_time(self, departure_time: timedelta):
        """
        Sets the departure time of the truck from the hub.  Removes the first element of the "locations_by_time_list"
        and replaces it with the new location, departure time pairing.
        :param departure_time: The new departure time of the truck.
        :raises ValueError: If the provided departure time is not a timedelta object.
        """
        if not isinstance(departure_time, timedelta):
            raise ValueError('Invalid "departure time" value.')
        self._departure_time = departure_time
        self._location_by_time_list.pop()
        self.set_current_location(self._current_location, self._departure_time, 0)

    @property
    def current_capacity(self) -> int:
        """
        Returns the current capacity of the truck with respect to the number of packages.
        :return: The current capacity of the truck with respect to the number of packages.
        """
        return self._current_capacity

    @current_capacity.setter
    def current_capacity(self, new_curr_capacity: int):
        """
        Sets the current capacity of the truck.
        :param new_curr_capacity: The new current capacity of the truck.
        :raises ValueError: If the new capacity value added is not an integer, or if it would reduce the truck's
        capacity to below 0.
        """
        if not isinstance(new_curr_capacity, int):
            raise ValueError('Invalid "new current capacity value".')
        if new_curr_capacity < 0:
            raise ValueError('Cannot exceed maximum capacity.')

        self._current_capacity = new_curr_capacity

    def set_current_location(self, curr_location: Location, curr_time: timedelta, miles_traveled: float):
        """
        Sets the current location of the truck, as well as the current time and the current mileage.
        :param curr_location: The current location of the truck.
        :param curr_time: The current time of the truck at the new current location.
        :param miles_traveled: The current number of miles traveled of the truck.
        :raises ValueError: If current location value is not a Location object.
        :raises ValueError: If current time value is not a timedelta object.
        :raises ValueError: If miles traveled value is not an integer or float, or less than 0.
        """
        if not isinstance(curr_location, Location):
            raise ValueError('Invalid "current location" value.')
        if not isinstance(curr_time, timedelta):
            raise ValueError('Invalid "current time" value.')
        if not isinstance(miles_traveled, (int, float)) or miles_traveled < 0:
            raise ValueError('Invalid "miles traveled" value.')
        self._current_location = curr_location
        self._location_by_time_list.append((curr_location, curr_time, miles_traveled))

    def add_assigned_package(self, package: Package):
        """
        Adds a package to the truck's assigned packages list.
        :param package: The package to add to the assigned packages list.
        :raises RuntimeError: If the truck lack's capacity for the assignment, or if the provided package has already
        been assigned.
        """
        if self.current_capacity - len(self._assigned_packages) == 0:
            raise RuntimeError(f'Not enough capacity in truck #{self._id} to assign package #{package.id}')
        if package.assigned:
            raise RuntimeError(f'Package #{package.id} was already assigned!')

        self._assigned_packages.append(package)
        package.assigned = True

    def remove_assigned_package(self, package: Package):
        """
        Removes a package from the truck's assigned packages list.
        :param package: The package to be removed from the assigned packages list.
        :raises ValueError:  If the provided package is not currently assigned to the truck.
        """
        if package not in self._assigned_packages:
            raise ValueError(f'Package #{package.id} is not assigned to truck #{self._id}')
        else:
            self._assigned_packages.remove(package)
            package.assigned = False

    def load_bundle(self, packages: List[Package], distance_from_prev: float, curr_travel_distance: float):
        """
        A function that loads a list of packages to the truck and updates the status of the package accordingly.
        When a package is loaded, it is added to the truck's priority queue of packages.
        :param packages: The packages to be loaded into the truck.
        :param distance_from_prev: The traversed mileage from the previous location.
        :param curr_travel_distance: The total number of miles traveled up to this point.
        :raises ValueError: If "distance_from_prev" value is not an integer or float.
        :raises ValueError: If "curr_travel_distance" value is not an integer or float.
        :raises RuntimeError: If the truck does not have enough capacity to load the package(s).
        :raises RuntimeError: If a package in the list is somehow already en route.
        """
        if not isinstance(distance_from_prev, (int, float)):
            raise ValueError('Invalid "distance to next" value.')
        if not isinstance(curr_travel_distance, (int, float)):
            raise ValueError('Invalid "current travel distance" value.')
        if not packages:
            return

        num_packages = len(packages)
        if self._current_capacity - num_packages < 0:
            raise RuntimeError(f'Truck {self._id} does not have enough capacity to load:\n{packages}')
        self.packages_queue.insert(priority=curr_travel_distance, information=(packages, distance_from_prev))
        self._current_capacity -= num_packages
        if packages and self._driver:
            for package in packages:
                if package.status == 'En Route':
                    raise RuntimeError(f'Package #{package.id} is already En Route!')
                package.set_status(Package.STATUSES[2], self._departure_time)
                package.truck_id = self._id

    def deliver_package(self, package: Package, current_time: timedelta):
        """
        A function that delivers a loaded package to its destination and updates the package's status accordingly.
        :param package: The package that was delivered.
        :param current_time: The time at which the package was delivered.
        :raises ValueError: If provided package is not a Package object.
        :raises ValueError: If provided current time is not a timedelta object.
        :raises RuntimeError: If the provided package has somehow already been delivered.
        """
        if not isinstance(package, Package):
            raise ValueError('Invalid "package" value.')
        if not isinstance(current_time, timedelta):
            raise ValueError('Invalid "current time" value.')
        if package.status == 'Delivered':
            raise RuntimeError(f'Package #{package.id} was already delivered!  ({current_time})')
        package.set_status(Package.STATUSES[3], current_time)
        self._delivered_packages.append(package)
        self._current_capacity += 1

    def get_curr_location_and_mileage(self, curr_time: timedelta):
        """
        A function serving the UI component to display the location and mileage of the truck at any given time.
        :param curr_time: The current time from which we will determine the location and mileage of the truck.
        :return: A tuple containing the current or most recent location, the total distance travelled thus far, and a
        boolean indicating whether the truck is in transit (i.e. not at the package's delivery location, not at the
        hub, etc.).
        """
        in_transit = False
        n = len(self._location_by_time_list)

        if curr_time < self._departure_time:
            curr_time = self._departure_time

        for i in range(n):
            location, arrival_time, dist_travelled = self._location_by_time_list[i]

            # If the current time (rounded to the nearest minute) is one of our arrival times, then we are at that
            # location and dropping off a package. Or, if we have reached the end of our list, then the truck's route
            # is complete and its last location and distance travelled represent its final status.
            if (curr_time.total_seconds() // 60 == arrival_time.total_seconds() // 60) or i == (n - 1):
                return location, dist_travelled, in_transit

            if i > 0:
                prev_location, prev_arrival_time, prev_dist_travelled = self._location_by_time_list[i - 1]

                if prev_arrival_time < curr_time < arrival_time:
                    in_transit = True

                    time_diff = arrival_time - prev_arrival_time
                    dist_diff = dist_travelled - prev_dist_travelled

                    time_ratio = (curr_time - prev_arrival_time) / time_diff
                    actual_dist_travelled = prev_dist_travelled + (dist_diff * time_ratio)

                    return location, actual_dist_travelled, in_transit
