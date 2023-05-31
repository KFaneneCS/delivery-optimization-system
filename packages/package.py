import copy
from datetime import timedelta

from locations.location import Location


class Package:
    """
    A class representing a package consisting of destination information, its assigned truck, special conditions,
    and its statuses.
    """
    STATUSES = ['At the Hub', 'Delayed', 'En Route', 'Delivered']

    def __init__(self, id_: int, destination: Location, city: str, state: str, zip_code: str, deadline: timedelta,
                 kilos: int, notes: str):
        """
        Initializes a new instance of the Package class.
        :param id_: The ID number of the package.
        :param destination: The destination of the package.
        :param city: The city of the destination.
        :param state: The state of the destination.
        :param zip_code: The zip code of the destination.
        :param deadline: The delivery deadline of the package.
        :param kilos: The number of kilograms of the package.
        :param notes: Special notes pertaining to the package, if any.
        """
        self._id = id_
        self._destination = destination
        self._city = city
        self._state = state
        self._zip_code = zip_code
        self._deadline = deadline
        self._kilos = kilos
        self._special_notes = notes
        self._assigned = False
        self._truck_id = None
        self._has_wrong_address = False
        self._old_package_copy = None
        self._not_special = False
        self._priority = None
        self._status = None
        self._status_at_times = []

    def __repr__(self):
        """
        Returns the string representation of the Package object.  Intended for testing purposes.
        :return: The string representation of the Package object.
        """
        return f'Package(ID={self._id} | destination={self.destination} | ' \
               f'deadline={self._deadline} | assigned={self._assigned} | ' \
               f'priority={self._priority} | status={self._status} | ' \
               f'truck={self._truck_id}) '

    @property
    def id(self) -> int:
        """
        Returns the ID associated with the Package.
        :return: The ID associated with the Package.
        """
        return self._id

    @property
    def destination(self) -> Location:
        """
        Returns the destination associated with the Package.
        :return: The destination associated with the Package.
        """
        return self._destination

    @destination.setter
    def destination(self, new_destination: Location):
        """
        Sets a new destination for the Package.
        :param new_destination: The new destination to be associated with the Package.
        :raises ValueError:  If value passed is not a Location object.
        """
        if not isinstance(new_destination, Location):
            raise ValueError('Invalid "destination" value.')
        self._destination = new_destination

    @property
    def city(self) -> str:
        """
        Returns the package's destination's city.
        :return: The package's destination's city.
        """
        return self._city

    @property
    def zip_code(self) -> str:
        """
        Returns the package's destination's zip code.
        :return: The package's destination's zip code.
        """
        return self._zip_code

    @property
    def deadline(self) -> timedelta:
        """
        Returns the delivery deadline associated with the Package.
        :return: The delivery deadline associated with the Package.
        """
        return self._deadline

    @property
    def kilos(self) -> int:
        """
        Returns the package's mass in kilograms.
        :return: The package's mass in kilograms.
        """
        return self._kilos

    @property
    def special_notes(self) -> str:
        """
        Returns special notes associated with the package.
        :return: Special notes associated with the package.
        """
        return self._special_notes

    @property
    def assigned(self) -> bool:
        """
        Returns True if Package has been assigned to a truck, otherwise False.
        :return: True if Package has been assigned to a truck, otherwise False.
        """
        return self._assigned

    @assigned.setter
    def assigned(self, is_assigned: bool):
        """
        Sets the Package's "assigned" boolean attribute.
        :param is_assigned: Boolean value indicating if Package is assigned.
        :raises ValueError: If value passed is not a boolean.
        """
        if not isinstance(is_assigned, bool):
            raise ValueError('Invalid "is assigned" value.')
        self._assigned = is_assigned

    @property
    def priority(self) -> (int, float):
        """
        Returns the priority value of the Package.
        :return: The priority value of the Package.
        """
        return self._priority

    @priority.setter
    def priority(self, priority_value: float):
        """
        Sets the priority value of the Package.
        :param priority_value: The new priority value of the Package.
        :raises ValueError: If value passed is not an integer or float.
        """
        if not isinstance(priority_value, (int, float)):
            raise ValueError('Invalid "priority value".')
        self._priority = priority_value

    @property
    def truck_id(self) -> int:
        """
        Returns the truck ID associated with the Package.
        :return: The truck ID associated with the Package.
        """
        return self._truck_id

    @truck_id.setter
    def truck_id(self, truck_id: int):
        """
        Sets the truck ID associated with the Package.
        :param truck_id: The new truck ID associated with the Package.
        :raises ValueError: If value passed is not an integer.
        """
        if truck_id < 0:
            raise ValueError('Invalid truck ID value.')
        self._truck_id = truck_id

    @property
    def has_wrong_address(self) -> bool:
        """
        Returns True if Package starts with a wrong destination address, otherwise False.
        :return: True if Package starts with a wrong destination address, otherwise False.
        """
        return self._has_wrong_address

    @has_wrong_address.setter
    def has_wrong_address(self, has_wrong_address: bool):
        """
        Sets the Package's "wrong_address" boolean attribute, then stores the original package info to access incorrect
        destination information after that information has been updated.
        :param has_wrong_address: Boolean value indicating if Package has wrong destination address at the start.
        :raises ValueError: If value passed is not a boolean.
        """
        if not isinstance(has_wrong_address, bool):
            raise ValueError('Invalid "has wrong address" value.')
        self._has_wrong_address = has_wrong_address
        self._old_package_copy = copy.deepcopy(self)

    @property
    def old_package_copy(self):
        """
        Returns the original Package object before destination information is updated.
        :return: The original Package object before destination information is updated.
        """
        return self._old_package_copy

    @property
    def not_special(self) -> bool:
        """
        Returns True if Package has no special conditions, otherwise False.
        :return: True if Package has no special conditions, otherwise False.
        """
        return self._not_special

    @not_special.setter
    def not_special(self, is_not_special: bool):
        """
        Sets the Package's "not_special" boolean attribute.
        :param is_not_special: Boolean value indicating whether Package does not have special conditions.
        :raises ValueError: If value passed is not a boolean.
        """
        if not isinstance(is_not_special, bool):
            raise ValueError('Invalid "is not special" value.')
        self._not_special = is_not_special

    @classmethod
    def get_status_options(cls):
        """
        Returns all possible status options for the Package class.
        :return: All possible status options for the Package class.
        """
        return cls.STATUSES

    @property
    def status(self):
        """
        Returns the current status of the Package.
        :return: The current status of the Package.
        """
        return self._status

    @property
    def status_at_times(self):
        """
        Returns the list of Package's statuses at their associated times.
        :return: The list of Package's statuses at their associated times.
        """
        return self._status_at_times

    def set_status(self, new_status: STATUSES, curr_time: timedelta):
        """
        Sets the current status of the Package at the given time, and appends the status and time as a tuple to the
        "status_at_times" list.
        :param new_status: The new status of the Package.
        :param curr_time: The time at which the status changes to the new status.
        :raises ValueError:  If new status is not one of the STATUSES options, or if current time is not a timedelta
        object.
        """
        if new_status not in self.STATUSES:
            raise ValueError(f'Invalid status: {new_status}.')
        if not isinstance(curr_time, timedelta):
            raise ValueError(f'Invalid "curr_time" value.')
        self._status = new_status
        self._status_at_times.append((curr_time, new_status))

    def get_status(self, curr_time: timedelta):
        """
        Returns the Package's status at a given time.
        :param curr_time:
        :return: The time for which the Package's status is being requested.  None if no status exists at the given
        time.
        """
        for td, status in reversed(self._status_at_times):
            if curr_time >= td:
                if status == 'Delayed':
                    return 'At the Hub (Delayed)'
                return status
        return None

    def get_time_of_delivery(self):
        """
        Returns the time at which the Package was delivered.
        :return: The time at which the Package was delivered, or None if its delivery was not tracked.
        """
        for time, status in self._status_at_times:
            if status == 'Delivered':
                return time
        return None
