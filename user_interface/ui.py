from datetime import timedelta, time
import os

from packages.package import Package
from packages.packages import Packages
from trucks.trucks import Trucks


class UI:
    def __init__(self, packages: Packages, trucks: Trucks):
        self._packages = packages
        self._trucks = trucks

    @staticmethod
    def _timedelta_to_time(td: timedelta):
        total_seconds = td.total_seconds()
        hours = total_seconds // 3600
        minutes = (total_seconds % 3600) // 60
        seconds = total_seconds % 60
        return time(int(hours), int(minutes), int(seconds))

    @staticmethod
    def _get_user_time() -> timedelta:
        try:
            user_time = input('Enter (military) time in HH:MM format: ')
            hours, minutes = map(int, user_time.split(':'))
            curr_time = timedelta(hours=hours, minutes=minutes)
            return curr_time
        except ValueError:
            print('Please enter a valid time in HH:MM format.')

    def display_trucks_mileage(self):
        for truck in self._trucks.trucks:
            print(f'Truck #{truck.id} total mileage = {round(truck.miles_traveled, ndigits=1)}')
        print('----------------------------------------------------------')

    def execute(self):
        self.display_trucks_mileage()

        while True:
            print('\nOption 1: Display all packages')
            print('Option 2: Search by package ID')
            user_choice = input('Please enter "1" or "2" (or "q" to quit): ')
            if user_choice == 'q':
                return
            try:
                if int(user_choice) == 1:
                    self.show_all_statuses_at_time()
                elif int(user_choice) == 2:
                    self.show_package_status_at_time()
            except ValueError:
                print(f'Please enter valid choice.')

    def show_package_status_at_time(self):
        try:
            packages_table = self._packages.get_all_as_table()
            user_package_id = input('Enter package ID: ')
            package_id = int(user_package_id)
            if not packages_table[package_id]:
                print('Please enter valid Package ID.')
                return

            curr_package: Package = packages_table[package_id].value

        except ValueError:
            print('Please enter a valid integer for Package ID.')
            return
        except KeyError:
            print('Please enter a valid Package ID.')
            return

        curr_time = self._get_user_time()
        if not curr_time:
            return

        curr_status = curr_package.get_status(curr_time)

        curr_package.display_info()
        print(f'        At {self._timedelta_to_time(curr_time)}, package is {curr_status}')

    def show_all_statuses_at_time(self):
        packages_list = self._packages.get_all_as_list()
        at_hub_list = []
        delayed_list = []
        en_route_list = []
        delivered_list = []

        curr_time = self._get_user_time()
        if not curr_time:
            return

        for package in packages_list:
            curr_status = package.get_status(curr_time)

            match curr_status:
                case 'At Hub':
                    at_hub_list.append(package.id)
                case 'Delayed':
                    delayed_list.append(package.id)
                case 'En Route':
                    en_route_list.append(package.id)
                case 'Delivered':
                    delivered_list.append(package.id)

        print(f'Packages at the HUB:  {at_hub_list}')
        print(f'Packages delayed on plane:  {delayed_list}')
        print(f'Packages loaded and en route:  {en_route_list}')
        print(f'Delivered packages:  {delivered_list}')

        return






