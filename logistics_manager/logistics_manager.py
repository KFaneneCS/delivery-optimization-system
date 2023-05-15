import re
from datetime import datetime, timedelta

from data_structures.hash import HashTable
from data_structures.priority_queue import MinPriorityQueue
from graph.dijkstra import Dijkstra
from locations.location import Location
from locations.locations import Locations
from packages.packages import Package, Packages
from trucks.trucks import Truck, Trucks

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
        self._packages = Packages(
            package_csv=PACKAGES_FILE,
            shortest_paths=self._hub_shortest_paths,   # FIXME
            locations=self._locations
        )
        self._locations_to_packages_table = self._packages.locations_to_packages_table
        self._trucks = Trucks(
            num_trucks=3,
            num_drivers=2,
            start_location=self._hub,
            start_time=START_TIME,
            curr_time=START_TIME,
        )
        self._early_departure_set = False
        self._special_cases = HashTable(10)
        self._grouped_packages = []
        self._group_assigned = False
        self._seen_addresses = HashTable()
        self._delayed_packages = []
        self._delayed_packages_arrival_time = timedelta(hours=23, minutes=59)
        self._truck_handling_delayed = None
        self._leftover_packages = []
        self._packages_locations_by_time = HashTable()
        self._truck_locations_by_time = HashTable()
        self._handle_special_cases()
        self._load_packages()

    def _find_all_shortest_paths(self):
        for location in self._locations.get_all_locations():
            shortest_path = Dijkstra(location, self._graph)
            self._all_shortest_paths.add_node(location, shortest_path)

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
        def handle_only_truck_2(pckg: Package):
            pckg.truck_id = 2
            truck_2 = self._trucks.get_truck_by_id(2)
            truck_2.current_capacity -= 1
            pckg.space_already_allocated = True

        # TODO: Cite: https://www.tutorialspoint.com/python/python_reg_expressions.htm
        # TODO: Cite: https://www.programiz.com/python-programming/datetime/strptime
        def handle_delayed_packages(pckg: Package):
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

        def handle_wrong_address(pckg: Package):
            pckg.wrong_address = True
            pckg.status = Package.STATUSES[1]

        def handle_grouped_packages(pckg: Package):
            special_note = pckg.special_notes
            curr_id = int(pckg.id)
            # other_package_nums = re.findall(r'\d+', special_note)
            # other_package_ids = [int(num) for num in other_package_nums]
            other_package_ids = [int(num) for num in re.findall(r'\d+', special_note)]
            combined_ids = other_package_ids + [curr_id]

            for package_id in combined_ids:
                package_to_add = self._packages.get_package_by_id(package_id)
                if package_to_add and package_to_add not in self._grouped_packages:
                    package_to_add.space_already_allocated = True
                    self._grouped_packages.append(package_to_add)
                    self._seen_addresses.add_node(package_to_add.destination, None)
            for other_package in self._packages.packages:
                if (other_package not in self._grouped_packages) and self._seen_addresses.get_node(
                        other_package.destination):
                    self._grouped_packages.append(other_package)

        special_notes = ['Can only be on truck 2',
                         'Delayed on flight',
                         'Wrong address listed',
                         'Must be delivered with']

        special_note_handlers = [handle_only_truck_2,
                                 handle_delayed_packages,
                                 handle_wrong_address,
                                 handle_grouped_packages]

        for i in range(len(special_notes)):
            self._special_cases.add_node(unhashed_key=special_notes[i], value=special_note_handlers[i])

        for package in self._packages.packages:
            curr_notes = package.special_notes
            for note, handling_method in self._special_cases.items():
                if curr_notes.startswith(note):
                    handling_method(package)

        return self._special_cases

    def _load_packages(self):
        def dist_to_time_conversion(dist: float):
            return timedelta(hours=(dist / TRUCK_SPEED))

        def time_to_dist_conversion(t: timedelta):
            return t.total_seconds() / 3600 * TRUCK_SPEED

        for truck in self._trucks.trucks:
            if not truck.driver:
                truck.departure_time = timedelta(hours=23, minutes=59, seconds=59)

        curr_time = START_TIME
        delayed_package_truck = self._truck_handling_delayed
        curr_priority_value = 1

        truck_taking_group = self._trucks.get_truck_by_id(1)
        truck_taking_group.current_capacity -= len(self._grouped_packages)
        for package in self._grouped_packages:
            package.truck_id = truck_taking_group.id
            package.space_already_allocated = True

        while not self._ordered_locations.is_empty():
            location, distance = self._ordered_locations.get()
            travel_time = dist_to_time_conversion(distance)

            if location.address == 'HUB':
                continue

            destination_packages = self._locations_to_packages_table.get_node(location).value
            curr_truck = self._trucks.find_available_truck(current_time=curr_time, assoc_packages=destination_packages)
            for package in destination_packages:
                # Setup for delivering packages.  Not strictly necessary for this method's logic.
                self._packages_locations_by_time.add_node(unhashed_key=package.id, value=[])

                package.priority = curr_priority_value
                if package.status == 'Delayed' or package.wrong_address:
                    curr_truck = delayed_package_truck
                    package.truck_id = curr_truck.id
                if not package.truck_id:
                    package.truck_id = curr_truck.id
                curr_priority_value += 1

            # assoc_packages = self._locations_to_packages_table.get_node(location).value
            # curr_truck: Truck = self._trucks.find_available_truck(current_time=curr_time, assoc_packages=assoc_packages)
            #
            # for package in assoc_packages:
            #     package.priority = curr_priority_value
            #     curr_priority_value += 1
            #     if package.status == 'Delayed' or package.wrong_address:
            #         curr_truck = self._truck_handling_delayed
            #         package.truck_id = curr_truck.id
            #     elif not package.truck_id:
            #         package.truck_id = curr_truck.id

            self._trucks.load_packages(packages=destination_packages, travel_time=travel_time, current_time=curr_time)
            curr_time += travel_time

        # # FIXME:  for testing
        # for truck in self._trucks.trucks:
        #     print(truck)
        #     for x in truck.packages_list:
        #         print(x.package.id)
        # return

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
        for truck in self._trucks.trucks[0:2]:
            curr_time = truck.departure_time
            curr_location = truck.current_location
            self._truck_locations_by_time.add_node(unhashed_key=truck.id, value=[(curr_time, curr_location)])
            curr_destination = None
            while not truck.packages_queue.is_empty():
                curr_package: Package = truck.packages_queue.get()
                if curr_destination != curr_package.destination:
                    curr_shortest_paths: Dijkstra = self._all_shortest_paths.get_node(curr_location).value
                    curr_destination: Location = curr_package.destination

                    curr_route = curr_shortest_paths.get_shortest_path(curr_destination)
                    distance = curr_route[-1][1]
                    truck.miles_traveled += distance

                    travel_time = timedelta(hours=(distance / TRUCK_SPEED))
                    curr_time += travel_time
                    truck.current_time += travel_time
                    truck_loc_by_time_list = self._truck_locations_by_time.get_node(truck.id).value
                    truck_loc_by_time_list.append((curr_time, curr_location))

                    curr_location = curr_destination

                pckg_loc_by_time_list = self._packages_locations_by_time.get_node(curr_package.id).value
                pckg_loc_by_time_list.append((curr_time, curr_location))
                truck.delivered_packages.append(curr_package)

                truck.current_location = curr_location
        print(self._trucks.get_truck_by_id(1))
        print(self._trucks.get_truck_by_id(2))

        print(self._packages_locations_by_time.print_all())

