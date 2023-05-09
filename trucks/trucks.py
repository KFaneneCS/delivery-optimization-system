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

        note_handling_methods = [self.special_note_1,
                                 self.special_note_2,
                                 self.special_note_3,
                                 self.special_note_4]

        for i in range(len(special_notes)):
            self.special_cases.add_node(unhashed_key=special_notes[i], value=note_handling_methods[i])

        return self.special_cases

    def special_note_1(self):
        print('Special note 1')

    def special_note_2(self):
        print('Special note 2')

    def special_note_3(self):
        print('Special note 3')

    def special_note_4(self):
        print('Special note 4')

    def load_packages(self, packages: List[Package]):
        priority_queue = priority_logic.prioritize_packages(packages)

        while not priority_queue.is_empty():
            curr_package = priority_queue.get()
            curr_notes = curr_package.get_special_notes()
            for note, method in self.special_cases.items():
                if curr_notes.startswith(note):
                    print(f'Note [ {curr_notes} ] triggered on package [ {curr_package} ]')

    def get_packages_by_truck_id(self, truck_id: int):
        if truck_id < 0 or truck_id > len(self.trucks) - 1:
            print('Invalid truck ID.')

        truck = self.trucks[truck_id - 1]
        return truck.get_packages()
