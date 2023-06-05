from datetime import datetime, timedelta

from data.packages_loader import PackagesLoader
from data_structures.hash import HashTable
from locations.locations import Locations
from .package import Package


class Packages:
    """
    A class that instantiates and manages a collection of Package objects and provides a means of interacting with all
    Package objects.
    """

    def __init__(self, package_csv: str, locations: Locations, time_address_corrected: timedelta):
        """
        Initializes a new instance of the Packages class.

        Two initialization functions are called to add all packages to the "packages_list" and to associate each
        Package to its destination Location object via a hash table.
        :param package_csv: The csv file from which data for all packages is found.
        :param locations: A Locations object from which all Location objects can be accessed.
        """
        self._locations = locations
        self._time_address_corrected = time_address_corrected
        self._packages = HashTable(80)
        self._packages_list = []
        self._loader = PackagesLoader(package_csv)
        self._priority_queue = None
        self._location_to_packages_table = HashTable()
        self._add_all_packages()
        self._associate_packages_to_locations()

    def _add_all_packages(self):
        """
        Initialization function that extracts data from the packages csv file and instantiates corresponding Package
        objects, then adds those objects to the packages list.
        :raises IndexError:  If csv data has missing values, causing an index error during extraction.
        :raises ValueError:  If csv data has invalid data.
        """
        for dataset in self._loader.get_data():
            try:
                package_id = int(dataset[0])
                destination = self._locations.get_location(dataset[1].strip())
                city = dataset[2]
                state = dataset[3]
                zip_code = dataset[4]
                if dataset[5] != 'EOD':
                    deadline_dt = datetime.strptime(dataset[5], '%I:%M %p').time()
                    deadline = timedelta(hours=deadline_dt.hour, minutes=deadline_dt.minute)
                else:
                    deadline = None
                kilos = int(dataset[6])
                requirement_notes = dataset[7]
                new_package = Package(package_id, destination, city, state, zip_code, deadline, kilos,
                                      requirement_notes)
                self._packages[package_id] = new_package
            except (IndexError, ValueError):
                raise

    def _associate_packages_to_locations(self):
        """
        Initialization function that groups all Packages by their corresponding Location object in a hash table.
        """
        for _, package in self._packages.items():
            destination = package.destination
            if not self._location_to_packages_table[destination]:
                self._location_to_packages_table[destination] = [package]
            else:
                self._location_to_packages_table[destination].value.append(package)

    @property
    def locations_to_packages_table(self):
        """
        Returns the hash table containing each Location's associated Packages.
        :return: The hash table containing each Location's associated Packages.
        """
        return self._location_to_packages_table

    def get_all_as_list(self):
        """
        Allows access to all packages in a list data structure drawn from the hash table.
        :return: A list of all packages.
        """
        if not self._packages_list:
            for _, package in self._packages.items():
                self._packages_list.append(package)
        return sorted(self._packages_list, key=lambda p: p.id)

    def get_all_as_table(self):
        """
        Returns the Packages hash table.
        :return: The Packages hash table.
        """
        return self._packages

    def get_by_id(self, id_: int):
        """
        Returns the Package object with the provided ID if it exists.
        :param id_: The ID of the Package to be returned.
        :return: The Package object with the provided ID if it exists.
        :raises ValueError: If Package ID is not an integer value.
        :raises KeyError: If Package with provided ID does not exist.
        """
        if not isinstance(id_, int):
            raise ValueError('Invalid ID value.')
        try:
            return self._packages[id_].value
        except KeyError:
            raise KeyError(f'Package with ID {id_} does not exist.')

    def get_num_packages(self):
        """
        Returns the total number of packages.
        :return: The total number of packages.
        """
        return self._packages.get_size()

    def get_all_statuses_by_time(self):
        """
        Yields each Package's "status_at_time" list comprising each status at a particular time as tuples.
        :return: Each Package's "status_at_time" list.
        """
        for package in self._packages:
            yield package, package.status_at_times

    def display_package_info(self, package, curr_time):
        """
        Prints specific package information to console.  Intended for the user as part of the UI experience.  If the
        package started with a wrong delivery address, and the current time is less than the time the address is
        corrected, then the original wrong destination information is displayed - otherwise, its updated information is
        displayed.
        :param package: The Package object whose information is being displayed.
        :param curr_time: The current time to compare against the time the wrong address is corrected.
        :raises ValueError: If package is not Package object or curr_time is not timedelta object.
        """
        if not isinstance(package, Package):
            raise ValueError('Invalid "package" value.')
        if not isinstance(curr_time, timedelta):
            raise ValueError('Invalid "current time" value.')

        if package.has_wrong_address and curr_time < self._time_address_corrected:
            package = package.old_package_copy

        print(f'ID={package.id} | Delivery Address={package.destination.address} | Delivery City={package.city} | '
              f'Delivery Zip Code={package.destination.zip_code} | Delivery Deadline={package.deadline} | '
              f'Package Weight={package.kilos}')
