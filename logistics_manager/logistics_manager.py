import re
from typing import List
from priority_logic import priority_logic
from data_structures.priority_queue import MinPriorityQueue
from data_structures.hash import HashTable
from data_structures.linked_list import LinkedList
from packages.packages import Package, Packages
from trucks.trucks import Truck, Trucks, Driver
from graph.dijkstra import Dijkstra
from locations.locations import Location, Locations
from datetime import datetime, date, time, timedelta

LOCATIONS_FILE = 'data/distance_table.csv'
PACKAGES_FILE = 'data/package_file.csv'
TRUCK_SPEED = 18
START_TIME = timedelta(hours=8, minutes=0)
CLOSING_TIME = timedelta(hours=17, minutes=0)


class LogisticsManager:
    def __init__(self):
        self._locations = Locations(LOCATIONS_FILE)
        self._hub = self._locations.get_location('HUB')
        self._graph = self._locations.get_graph()
        self._all_shortest_paths = HashTable()
        self._ordered_locations = MinPriorityQueue()
        self._find_all_shortest_paths()
        self._find_full_ideal_route()
        self._hub_shortest_paths = self._all_shortest_paths.get_node(self._hub).value
        self._packages = Packages(PACKAGES_FILE, self._hub_shortest_paths,
                                  self._locations)  # TODO:  Need to reconsider parameters
        self._locations_to_packages_table = self._packages.locations_to_packages_table
        self._trucks = Trucks(num_trucks=3, num_drivers=2, start_location=self._hub, curr_time=START_TIME)
        self._early_departure_set = False
        self._special_cases = HashTable(10)
        self._grouped_packages = []
        self._group_assigned = False
        self._seen_packages = HashTable()
        self._delayed_packages = []
        self._delayed_packages_arrival_time = timedelta(hours=23, minutes=59)
        self._truck_handling_delayed = None
        self._leftover_packages = []
        self._handle_special_cases()
        self._load_packages()

    def _find_all_shortest_paths(self):
        for location in self._locations.get_all_locations():
            shortest_path = Dijkstra(location, self._graph)
            self._all_shortest_paths.add_node(location, shortest_path)
        return

    def _find_full_ideal_route(self):
        current: Dijkstra = self._all_shortest_paths.get_node(self._hub).value
        total_distance = 0
        visited = {self._hub}
        self._ordered_locations.insert(0, (current.start, total_distance))

        for x in range(current.distance_table.get_size() - 1):
            next_location, distance = current.get_closest_from_start(visited)
            self._ordered_locations.insert(x + 1, (next_location, distance))
            visited.add(next_location)
            total_distance += distance
            current = self._all_shortest_paths.get_node(next_location).value

    def _handle_special_cases(self):
        def note_1_handling(pckg: Package):
            pckg.truck_id = 2
            truck_2 = self._trucks.get_truck_by_id(2)

            # Decreasing truck capacity, but not yet adding package to truck since packages must be added in order of
            # their priority
            truck_2.current_capacity -= 1
            pckg.space_already_allocated = True

        # TODO: Cite: https://www.tutorialspoint.com/python/python_reg_expressions.htm
        # TODO: Cite: https://www.programiz.com/python-programming/datetime/strptime
        def note_2_handling(pckg: Package):
            pckg.status = Package.STATUSES[1]
            self._trucks.add_delayed_package(pckg)

            special_note = pckg.special_notes
            time_format = r'\d{1,2}:\d{2} [a,p]m'
            extracted_time_string = re.search(time_format, special_note).group()
            time_obj = datetime.strptime(extracted_time_string, '%H:%M %p').time()
            time_td = timedelta(hours=time_obj.hour, minutes=time_obj.minute)
            if time_td < self._delayed_packages_arrival_time:
                self._delayed_packages_arrival_time = time_td
                self._early_departure_set = False
            if not self._early_departure_set:
                for truck in self._trucks.trucks[1:]:
                    if truck.driver:
                        truck.departure_time = self._delayed_packages_arrival_time
                        self._truck_handling_delayed = truck
                        self._early_departure_set = True
                        break

        def note_3_handling(pckg: Package):
            pckg.wrong_address = True

        def note_4_handling(pckg: Package):
            special_note = pckg.special_notes
            curr_id = int(pckg.id)

            other_package_nums = re.findall(r'\d+', special_note)
            other_package_ids = [int(num) for num in other_package_nums]
            combined_ids = other_package_ids + [curr_id]
            for package_id in combined_ids:
                package_to_add: Package = self._packages.get_package_by_id(package_id)
                if package_to_add not in self._grouped_packages:
                    package_to_add.space_already_allocated = True
                    self._grouped_packages.append(package_to_add)

        special_notes = ['Can only be on truck 2',
                         'Delayed on flight',
                         'Wrong address listed',
                         'Must be delivered with']

        note_handling_methods = [note_1_handling,
                                 note_2_handling,
                                 note_3_handling,
                                 note_4_handling]

        for i in range(len(special_notes)):
            self._special_cases.add_node(unhashed_key=special_notes[i], value=note_handling_methods[i])

        for package in self._packages.packages:
            curr_notes = package.special_notes
            for note, handling_method in self._special_cases.items():
                if curr_notes.startswith(note):
                    handling_method(package)

        return self._special_cases

    def _load_packages(self):
        def dist_to_time_conversion(dist: float):
            return timedelta(hours=(dist / TRUCK_SPEED))

        curr_time = START_TIME
        curr_truck = None
        curr_priority_value = 1
        group_leader_found = False
        extra_capacity_allocated = False

        while not self._ordered_locations.is_empty():
            location, distance = self._ordered_locations.get()

            travel_time = dist_to_time_conversion(distance)

            if location.address == 'HUB':
                continue
            # All packages with current location as destination
            assoc_packages = self._locations_to_packages_table.get_node(location).value
            num_packages = len(assoc_packages)
            if not group_leader_found:
                # If any of the associated packages are part of the group of packages that must be delivered
                # together,then we need to ensure there is enough capacity in the upcoming truck assignment for
                # all of them.
                for package in assoc_packages:
                    if package in self._grouped_packages:
                        num_packages += len(self._grouped_packages)
                        group_leader_found = True
                        break
            for package in assoc_packages:
                package.priority = curr_priority_value
                curr_priority_value += 1
                # Delayed?
                if package.status == 'Delayed' or package.wrong_address:
                    curr_truck = self._truck_handling_delayed
                # Truck ID already assigned?
                elif package.truck_id:
                    curr_truck: Truck = self._trucks.get_truck_by_id(package.truck_id)
                else:
                    curr_truck: Truck = self._trucks.find_available_truck(current_time=curr_time,
                                                                          num_packages=num_packages)
                    if not curr_truck:
                        raise ValueError('No trucks available.')

            print(f'TRUCK:  {curr_truck}')
            print(f'PACKAGES:  {assoc_packages}')
            if curr_truck:
                # TODO:  Continue here - fixing load pckg method
                self._trucks.load_packages(truck=curr_truck, packages=assoc_packages, travel_time=travel_time)
                if group_leader_found and not extra_capacity_allocated:
                    curr_truck.current_capacity -= num_packages
                    extra_capacity_allocated = True

                # Increment time after package is loaded
                curr_time += travel_time
            curr_truck = None
        # FIXME: Testing
        print('~~~~DELAYED PACKAGES~~~~')
        for p in self._grouped_packages:
            print(p)

        return

        # def load_into_optimal_truck(curr_package: Package):
        #     trucks_with_drivers = [truck for truck in self._trucks.trucks if
        #                            truck.driver and truck.current_capacity > 0]
        #     if not trucks_with_drivers:
        #         self._leftover_packages.append(package)
        #         # trucks_without_drivers = [truck for truck in self.trucks.trucks if
        #         #                           not truck.driver and truck.current_capacity > 0]
        #         # if not trucks_without_drivers:
        #         #     raise ValueError('No space in any trucks.')
        #         # optimal_truck: Truck = max(trucks_without_drivers, key=lambda t: t.current_capacity)
        #     else:
        #         optimal_truck: Truck = max(trucks_with_drivers, key=lambda t: t.current_capacity)
        #         curr_package.truck_id = optimal_truck.id
        #         optimal_truck.load_package(curr_package)
        #
        # priority_queue = priority_logic.prioritize_packages(self._packages.packages)
        #
        # while not priority_queue.is_empty():
        #     current_package: Package = priority_queue.get()
        #     # Delayed?
        #     if current_package.status == 'Delayed':
        #         self._delayed_packages.append(current_package)
        #     # Truck ID already assigned?
        #     elif current_package.truck_id is not None:
        #         if current_package not in self._grouped_packages:
        #             assigned_truck: Truck = self._trucks.get_truck_by_id(current_package.truck_id)
        #             assigned_truck.load_package(package=current_package, is_preassigned=True)
        #             self._seen_packages.add_node(unhashed_key=current_package.destination, value=assigned_truck)
        #     # Package part of group list?
        #     elif current_package in self._grouped_packages and not self._group_assigned:
        #         for truck in self._trucks.trucks:
        #             if truck.current_capacity >= len(self._grouped_packages) and truck.driver:
        #                 for package in self._grouped_packages:
        #                     package.truck_id = truck.id
        #                     truck.load_package(package)
        #                     self._seen_packages.add_node(unhashed_key=package.destination, value=truck)
        #                 self._group_assigned = True
        #                 break
        #     # Truck already carrying package with same address?
        #     elif self._seen_packages.has_node(unhashed_key=current_package.destination):
        #         truck_with_same_destination: Truck = self._seen_packages.get_node(current_package.destination).value
        #         if truck_with_same_destination.current_capacity > 0:
        #             current_package.truck_id = truck_with_same_destination.id
        #             truck_with_same_destination.load_package(current_package)
        #         else:
        #             # Unable to load package to truck already containing another package with same destination
        #             load_into_optimal_truck(current_package)
        #
        #     else:
        #         load_into_optimal_truck(current_package)
        #
        # # Assign return time per delayed packages' hub arrival time to truck with driver and lowest cumulative
        # # priority value
        # truck_for_late_arrivals: Truck = min((truck for truck in self._trucks.trucks if truck.driver),
        #                                      key=lambda t: t.cumulative_priority_value)
        # truck_for_late_arrivals.return_time = datetime.combine(date.today(), self._return_time_for_delayed_packages)
        #
        # # for truck in self._trucks.trucks:
        # #     print(truck)
        # #     while not truck.packages_queue.is_empty():
        # #         print(truck.packages_queue.get())

    def deliver_packages(self):
        return
        # # Clear our "seen packages" hash table so that we can use it again in this method.
        # for node in self._seen_packages.get_all():
        #     self._seen_packages.delete(node.key)

        # print('------------------------------------------------------------------------')
        # loaded_trucks = [truck for truck in self._trucks.trucks if not truck.packages_queue.is_empty()]
        # curr_time = timedelta(hours=START_TIME.hour, minutes=START_TIME.minute)
        # total_miles = 0  # FIXME:  testing
        # for truck in loaded_trucks:
        #     if truck.return_time is None:
        #         print(f'Current truck #{truck.id}')
        #         curr_location = truck.current_location
        #         while not truck.packages_queue.is_empty():
        #             shortest_paths: Dijkstra = self._all_shortest_paths.get_node(curr_location).value
        #             curr_package: Package = truck.packages_queue.get()
        #             destination: Location = curr_package.destination
        #             route = shortest_paths.get_shortest_path(destination)
        #             print(f'     Route:  {route}')
        #             # Check if route has any additional locations in between start and end
        #             if len(route) > 2:
        #                 for intermediate_location in route[1:len(route) - 1]:
        #                     if truck.locations_to_packages_table.get_node(intermediate_location):
        #                         print('TODO:  also deliver this package')
        #             distance = route[-1][1]
        #             total_miles += distance
        #             travel_time_in_hours = distance / TRUCK_SPEED
        #             travel_time = timedelta(hours=travel_time_in_hours)
        #             print(f'Distance: {distance} ----->  {travel_time}')
        #             curr_time += travel_time
        #             print(f' ** Current time:  {curr_time} |||  Miles:   {total_miles}')
        #
        #             # print(route)
        #             curr_location = destination
