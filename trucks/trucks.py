from packages.packages import Package
from priority_logic import priority_logic
from data_structures.hash import HashTable
from .truck import Truck, Driver
from typing import List


class Trucks:
    def __init__(self, num_trucks: int, num_drivers: int):
        self.num_trucks = num_trucks
        self.num_drivers = num_drivers
        self.trucks = []
        self.special_cases = HashTable(10)
        self.initialize_drivers_and_trucks()
        self.handle_special_cases()

    def initialize_drivers_and_trucks(self):
        for i in range(1, self.num_drivers + 1):
            driver = Driver(i)
            self.trucks.append(Truck(i, driver))

        for i in range(self.num_trucks - self.num_drivers):
            self.trucks.append(Truck(i + self.num_drivers + 1, None))

    def handle_special_cases(self):
        special_notes = ['Can only be on truck 2',
                         'Delayed on flight',
                         'Wrong address listed',
                         'Must be delivered with']

        note_handling_methods = [self.note_1_handling,
                                 self.note_2_handling,
                                 self.note_3_handling,
                                 self.note_4_handling]

        for i in range(len(special_notes)):
            self.special_cases.add_node(unhashed_key=special_notes[i], value=note_handling_methods[i])

        return self.special_cases

    def note_1_handling(self, package: Package):
        package.truck_id = 2

    def note_2_handling(self, package: Package):
        package.delayed = True

    def note_3_handling(self, package: Package):
        print('Special note 3')

    def note_4_handling(self, package: Package):
        print('Special note 4')

    def load_packages(self, packages: List[Package]):
        priority_queue = priority_logic.prioritize_packages(packages)

        while not priority_queue.is_empty():
            curr_package = priority_queue.get()
            curr_notes = curr_package.special_notes
            for note, handling_method in self.special_cases.items():
                if curr_notes.startswith(note):
                    handling_method(curr_package)

    def get_packages_by_truck_id(self, truck_id: int):
        if truck_id < 0 or truck_id > len(self.trucks) - 1:
            print('Invalid truck ID.')

        truck = self.trucks[truck_id - 1]
        return truck._packages
