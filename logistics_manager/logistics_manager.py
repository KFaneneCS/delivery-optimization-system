import re
from packages.packages import Package, Packages
from trucks.trucks import Truck, Trucks, Driver
from graph.dijkstra import Dijkstra
from locations.locations import Locations
from data_structures.hash import HashTable
from datetime import datetime, date, time, timedelta


class LogisticsManager:
    def __init__(self):
        self.locations_file = 'data/distance_table.csv'
        self.packages_file = 'data/package_file.csv'
        self.start_of_day = datetime.combine(date.today(), time(8, 0))
        self.end_of_day = datetime.combine(date.today(), time(17, 0))
        self.locations = Locations(self.locations_file)
        self.hub = self.locations.get_location('HUB')
        self.graph = self.locations.get_graph()
        self.hub_shortest_paths = Dijkstra(self.hub, self.graph)
        self.all_shortest_paths = HashTable()
        self.all_shortest_paths.add_node(self.hub, self.hub_shortest_paths)
        self.packages = Packages(self.packages_file, self.hub_shortest_paths, self.locations)
        self.trucks = Trucks(3, 2)
        self.special_cases = HashTable(10)
        self.grouped_ids = []
        self.grouped_packages = []
        self.handle_special_cases()
        self.load_packages()

    def handle_special_cases(self):

        def note_1_handling(package: Package):
            package.truck_id = 2
            truck_2 = self.trucks.get_truck_by_id(2)

            # Decreasing truck capacity, but not yet adding package to truck since packages must be added in order of
            # their priority
            truck_2.curr_capacity -= 1
            print(f'current truck 2 [ {truck_2} ] capacity: [ {truck_2.curr_capacity} ]')

        def note_2_handling(package: Package):
            package.status = Package.STATUSES[1]

        def note_3_handling(package: Package):
            package.wrong_address = True

        def note_4_handling(package: Package):
            note = package.special_notes
            curr_id = int(package.id)

            # TODO: Cite: https://www.tutorialspoint.com/python/python_reg_expressions.htm
            other_package_nums = re.findall(r'\d+', note)
            other_package_ids = [int(num) for num in other_package_nums]
            combined_ids = other_package_ids + [curr_id]
            for package_id in combined_ids:
                if package_id not in self.grouped_ids:
                    self.grouped_ids.append(package_id)

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

        return self.special_cases

        # self.grouped_packages.append(package)

    def load_packages(self):
        for package in self.packages.packages:
            curr_notes = package.special_notes
            for note, handling_method in self.special_cases.items():
                if curr_notes.startswith(note):
                    handling_method(package)
            print(f'Current package {package}')

        # priority_queue = priority_logic.prioritize_packages(packages)

        # while not priority_queue.is_empty():
        # curr_package = priority_queue.get()
        # curr_notes = curr_package.special_notes
        # for note, handling_method in self.special_cases.items():
        #     if curr_notes.startswith(note):
        #         handling_method(curr_package)
