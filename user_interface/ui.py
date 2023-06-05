from datetime import timedelta, time

from packages.package import Package
from packages.packages import Packages
from trucks.trucks import Trucks


class UI:
    """
    This class represents the UI component of the program.  The user is immediately shown the individual and combined
    mileage of all trucks, as well as each truck's associated package IDs.  The user then has the option of searching
    all package statuses at a given time, or individual package's at a given time.
    """

    def __init__(self, packages: Packages, trucks: Trucks):
        self._packages = packages
        self._trucks = trucks

    @staticmethod
    def _timedelta_to_time(td: timedelta):
        total_seconds = td.total_seconds()
        hours = total_seconds // 3600
        minutes = (total_seconds % 3600) // 60
        seconds = total_seconds % 60
        return time(int(hours), int(minutes), int(seconds)).strftime('%H:%M')

    @staticmethod
    def _get_user_time() -> timedelta:
        try:
            user_time = input('Enter (military) time in HH:MM format: ')
            hours, minutes = map(int, user_time.split(':'))
            if not (0 <= hours <= 23) or not (0 <= minutes <= 59):
                raise ValueError
            curr_time = timedelta(hours=hours, minutes=minutes)
            return curr_time
        except ValueError:
            print('Please enter a valid time in HH:MM format.')

    def display_trucks_info(self):
        for truck in self._trucks.trucks:
            print(f'Truck #{truck.id} total mileage = {round(truck.miles_traveled, ndigits=1)}')
            associated_package_ids = sorted([p.id for p in truck.delivered_packages])
            print(f'\tAssociated packages = {associated_package_ids}')
        total_mileage = self._trucks.get_total_mileage()
        print(f'\nTOTAL mileage for all trucks = {total_mileage}')
        print('\n----------------------------------------------------------')

    def execute(self):
        self.display_trucks_info()

        while True:
            print('\n•Option 1: Display all packages')
            print('•Option 2: Search by package ID')
            user_choice = input('Please enter "1" or "2" (or "q" to quit): ')
            if user_choice == 'q':
                return
            try:
                user_choice = int(user_choice)
                if user_choice == 1:
                    self.show_all_statuses_at_time()
                elif user_choice == 2:
                    self.show_package_status_at_time()
                else:
                    print(f'Please enter valid choice.')
            except ValueError:
                print(f'Please enter valid integer choice.')

    def show_package_status_at_time(self):
        try:
            packages_table = self._packages.get_all_as_table()
            user_package_id = input('Enter package ID: ')
            package_id = int(user_package_id)

            if not packages_table[package_id]:
                print('Please enter valid Package ID.')
                return

            curr_package: Package = packages_table[package_id]

        except ValueError:
            print('Please enter a valid integer for Package ID.')
            return
        except KeyError:
            print('Please enter a valid Package ID.')
            return

        curr_truck = self._trucks.get_truck_by_id(curr_package.truck_id)
        curr_time = self._get_user_time()
        if not curr_time:
            return

        curr_status = curr_package.get_status(curr_time)
        print(f'\nPackage assigned to Truck #{curr_truck.id}')
        if curr_status == 'Delivered':
            delivery_time = curr_package.get_time_of_delivery()
            print(f'At {self._timedelta_to_time(curr_time)}, package has been delivered.  '
                  f'Package was delivered at {delivery_time}')
        else:
            print(f'At {self._timedelta_to_time(curr_time)}, package is {curr_status}')
        self._packages.display_package_info(curr_package, curr_time)

    def show_all_statuses_at_time(self):
        packages_list = self._packages.get_all_as_list()
        at_hub_list = []
        en_route_list = []
        delivered_list = []

        curr_time = self._get_user_time()
        if not curr_time:
            return

        print(f'\nAt {self._timedelta_to_time(curr_time)}:')
        for truck in self._trucks.trucks:
            location, mileage, in_transit = truck.get_curr_location_and_mileage(curr_time)
            print(f'Truck #{truck.id}:')
            if not in_transit:
                print(f'    Current Location:  {location}')
            else:
                print(f'    In transit after leaving:  {location}')

        for package in packages_list:
            curr_status = package.get_status(curr_time)

            if curr_status in ['At the Hub', 'At the Hub (Delayed)']:
                at_hub_list.append(package)
            elif curr_status == 'En Route':
                en_route_list.append(package)
            elif curr_status == 'Delivered':
                delivered_list.append(package)
            else:
                raise RuntimeError(f'Issue finding status for Package #{package.id}')

        print(f'\nPackages At the HUB at {curr_time}:')
        for package_at_hub in at_hub_list:
            self._packages.display_package_info(package_at_hub, curr_time)
        print(f'\nPackages En Route at {curr_time}:')
        for package_en_route in en_route_list:
            self._packages.display_package_info(package_en_route, curr_time)
        print(f'\nPackages Delivered by {curr_time}:')
        for package_delivered in delivered_list:
            delivery_time = package_delivered.get_time_of_delivery()
            self._packages.display_package_info(package_delivered, curr_time)
            print(f'\tPackage was delivered at {delivery_time}')
