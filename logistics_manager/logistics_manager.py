import re
from priority_logic import priority_logic
from packages.packages import Package, Packages
from trucks.trucks import Truck, Trucks, Driver
from graph.dijkstra import Dijkstra
from locations.locations import Locations
from data_structures.hash import HashTable
from datetime import datetime, date, time, timedelta

TRUCK_SPEED = 18
START_TIME = time(8, 0)


class LogisticsManager:
    def __init__(self):
        self.locations_file = 'data/distance_table.csv'
        self.packages_file = 'data/package_file.csv'
        self.locations = Locations(self.locations_file)
        self.hub = self.locations.get_location('HUB')
        self.graph = self.locations.get_graph()
        self.hub_shortest_paths = Dijkstra(self.hub, self.graph)
        self.all_shortest_paths = HashTable()
        self.all_shortest_paths.add_node(self.hub, self.hub_shortest_paths)
        self.packages = Packages(self.packages_file, self.hub_shortest_paths, self.locations)
        self.trucks = Trucks(3, 2, self.hub)
        self.special_cases = HashTable(10)
        self.grouped_packages = []
        self.group_assigned = False
        self.seen_packages = HashTable()
        self.delayed_packages = []
        self.current_time = datetime.combine(date.today(), START_TIME)
        self.handle_special_cases()
        self.load_packages()

    def handle_special_cases(self):

        def note_1_handling(pckg: Package):
            pckg.truck_id = 2
            truck_2 = self.trucks.get_truck_by_id(2)

            # Decreasing truck capacity, but not yet adding package to truck since packages must be added in order of
            # their priority
            truck_2.current_capacity -= 1

        def note_2_handling(pckg: Package):
            pckg.status = Package.STATUSES[1]

        def note_3_handling(pckg: Package):
            pckg.wrong_address = True

        def note_4_handling(pckg: Package):
            note = pckg.special_notes
            curr_id = int(pckg.id)

            # TODO: Cite: https://www.tutorialspoint.com/python/python_reg_expressions.htm
            other_package_nums = re.findall(r'\d+', note)
            other_package_ids = [int(num) for num in other_package_nums]
            combined_ids = other_package_ids + [curr_id]
            for package_id in combined_ids:
                package_to_add = self.packages.get_package_by_id(package_id)
                if package_to_add not in self.grouped_packages:
                    self.grouped_packages.append(package_to_add)

        special_notes = ['Can only be on truck 2',
                         'Delayed on flight',
                         'Wrong address listed',
                         'Must be delivered with']

        note_handling_methods = [note_1_handling,
                                 note_2_handling,
                                 note_3_handling,
                                 note_4_handling]

        for i in range(len(special_notes)):
            self.special_cases.add_node(unhashed_key=special_notes[i], value=note_handling_methods[i])

        for package in self.packages.packages:
            curr_notes = package.special_notes
            for note, handling_method in self.special_cases.items():
                if curr_notes.startswith(note):
                    handling_method(package)

        return self.special_cases

        # self.grouped_packages.append(package)

    def load_packages(self):
        priority_queue = priority_logic.prioritize_packages(self.packages.packages)

        while not priority_queue.is_empty():
            current_package: Package = priority_queue.get()

            # print(f'PCKG: {current_package}\nTruck 1 CAP: {self.trucks.get_truck_by_id(1).current_capacity}')
            # Delayed?
            if current_package.status == 'Delayed':
                self.delayed_packages.append(current_package)
            # Truck ID already assigned?
            elif current_package.truck_id is not None:
                if current_package not in self.grouped_packages:
                    assigned_truck: Truck = self.trucks.get_truck_by_id(current_package.truck_id)
                    assigned_truck.load_package(package=current_package, is_preassigned=True)
            # Package part of group list?
            elif current_package in self.grouped_packages and not self.group_assigned:
                for truck in self.trucks.trucks:
                    if truck.current_capacity >= len(self.grouped_packages) and truck.driver:
                        for package in self.grouped_packages:
                            package.truck_id = truck.id
                            truck.load_package(package)
                        self.group_assigned = True
                        break
            else:
                trucks_with_drivers = [truck for truck in self.trucks.trucks if
                                       truck.driver and truck.current_capacity > 0]
                # print(f' ~~  Trucks with drivers:  {trucks_with_drivers}')
                if not trucks_with_drivers:
                    trucks_without_drivers = [truck for truck in self.trucks.trucks if
                                              not truck.driver and truck.current_capacity > 0]
                    if not trucks_without_drivers:
                        raise ValueError('No space in any trucks.')
                    optimal_truck: Truck = max(trucks_without_drivers, key=lambda t: t.current_capacity)
                else:
                    optimal_truck: Truck = max(trucks_with_drivers, key=lambda t: t.current_capacity)

                # optimal_truck: Truck = min((truck for truck in self.trucks.trucks if truck.driver and truck.current_capacity > 0), key=lambda t: t.current_capacity)
                # if not optimal_truck:
                #     optimal_truck: Truck = min((truck for truck in self.trucks.trucks if not truck.driver and truck.current_capacity > 0), key=lambda t: t.current_capacity)
                current_package.truck_id = optimal_truck.id
                optimal_truck.load_package(current_package)

        for truck in self.trucks.trucks:
            print(f'-------------------------\nTRUCK:  {truck}')
            count = 0
            while not truck.packages.is_empty():
                print(truck.packages.get())
                count += 1
            print(f'TOTAL COUNT = {count}')

