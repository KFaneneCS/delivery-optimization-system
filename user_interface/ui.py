from datetime import timedelta, time

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
            print(f'\nTruck #{truck.id} total mileage = {round(truck.miles_traveled, ndigits=1)}')
            print('    Route: ', end='  ')
            for location, _, _ in truck.location_by_time_list:
                print(f'-> {location.address}', end=' ')
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

            curr_package: Package = packages_table[package_id].value

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
        print(f'At {self._timedelta_to_time(curr_time)}, package is {curr_status}')
        curr_package.display_info()

    def show_all_statuses_at_time(self):
        packages_list = self._packages.get_all_as_list()
        at_hub_list = []
        delayed_list = []
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
            print(f'    Current Mileage:  {round(mileage, ndigits=1)}')

        for package in packages_list:
            curr_status = package.get_status(curr_time)

            match curr_status:
                case 'At the Hub':
                    at_hub_list.append(package.id)
                case 'Delayed':
                    delayed_list.append(package.id)
                case 'En Route':
                    en_route_list.append(package.id)
                case 'Delivered':
                    delivered_list.append(package.id)

        print(f'\nPackages at the HUB:  {at_hub_list if at_hub_list else None}')
        print(f'Packages delayed on plane:  {delayed_list if delayed_list else None}')
        print(f'Packages loaded and en route:  {en_route_list if en_route_list else None}')
        print(f'Packages delivered:  {delivered_list if delivered_list else None}')
