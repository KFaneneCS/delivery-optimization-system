import math
import re
import warnings
from datetime import datetime, timedelta, time

from data_structures.hash import HashTable
from graph.dijkstra import Dijkstra
from locations.locations import Locations
from packages.packages import Package, Packages
from trucks.trucks import Truck, Trucks

TRUCK_SPEED = 18
BEGINNING_OF_DAY = timedelta(hours=0, minutes=0)
END_OF_DAY = timedelta(hours=23, minutes=59, seconds=59)
START_TIME = timedelta(hours=8, minutes=0)
CLOSING_TIME = timedelta(hours=17, minutes=0)
CORRECTED_ADDRESS_TIME = timedelta(hours=10, minutes=20)
CORRECTED_ADDRESS = '410 S State St'


class LogisticsManager:
    def __init__(self, locations_file, packages_file):
        self._locations = None
        self._hub = None
        self._graph = None
        self._all_shortest_paths = None
        self._packages = None
        self._trucks = None
        self._initialize(locations_file, packages_file)

    def _initialize(self, locations_file, packages_file):
        self._locations = Locations(locations_file)
        self._hub = self._locations.get_location('HUB')
        self._graph = self._locations.get_graph()
        self._all_shortest_paths = HashTable()
        self._calculate_all_shortest_paths()
        self._hub_shortest_paths = self._all_shortest_paths[self._hub].value
        self._packages = Packages(package_csv=packages_file, locations=self._locations)
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
        self._seen_addresses = HashTable()
        self._packages_by_destination = HashTable(len(self._locations.get_all_locations()) * 2)
        self._delayed_packages = []
        self._delayed_packages_arrival_time = END_OF_DAY
        self._truck_handling_delayed = None
        self._handle_special_cases()
        self._group_packages_by_destination()
        self._assign_packages_to_trucks()

    @staticmethod
    def calculate_time_from_miles(miles: float):
        time_hours = miles / TRUCK_SPEED
        return timedelta(seconds=time_hours * 60 * 60)

    def _calculate_all_shortest_paths(self):
        for location in self._locations.get_all_locations():
            shortest_path = Dijkstra(location, self._graph)
            self._all_shortest_paths[location] = shortest_path

    def _handle_special_cases(self):
        def handle_only_truck_2(pckg: Package):
            truck_2 = self._trucks.get_truck_by_id(2)
            truck_2.add_assigned_package(pckg)

        def handle_delayed_packages(pckg: Package):
            # TODO: Cite: https://www.tutorialspoint.com/python/python_reg_expressions.htm
            # TODO: Cite: https://www.programiz.com/python-programming/datetime/strptime
            pckg.set_status(Package.STATUSES[1], BEGINNING_OF_DAY)
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
            self._delayed_packages.append(pckg)

        def handle_wrong_address(pckg: Package):
            pckg.wrong_address = True
            trucks_without_drivers = [t for t in self._trucks.trucks if not t.driver]
            # Assign package to first truck without driver since address will not be known for some time.
            trucks_without_drivers[0].add_assigned_package(pckg)

        def handle_grouped_packages(pckg: Package):
            special_note = pckg.special_notes
            curr_id = int(pckg.id)
            other_package_ids = [int(num) for num in re.findall(r'\d+', special_note)]
            combined_ids = other_package_ids + [curr_id]

            for package_id in combined_ids:
                package_to_add = self._packages.get_by_id(package_id)
                if package_to_add and package_to_add not in self._grouped_packages:
                    self._grouped_packages.append(package_to_add)
                    self._seen_addresses[package_to_add.destination] = None

        special_notes = ['Can only be on truck 2',
                         'Delayed on flight',
                         'Wrong address listed',
                         'Must be delivered with']

        special_note_handlers = [handle_only_truck_2,
                                 handle_delayed_packages,
                                 handle_wrong_address,
                                 handle_grouped_packages]

        for i in range(len(special_notes)):
            self._special_cases[special_notes[i]] = special_note_handlers[i]

        for package in self._packages.get_all_as_list():
            curr_notes = package.special_notes
            for note, handling_method in self._special_cases.items():
                if curr_notes.startswith(note):
                    handling_method(package)
            if not package.status:
                package.set_status(Package.STATUSES[0], BEGINNING_OF_DAY)

        for delayed_package in self._delayed_packages:
            self._truck_handling_delayed.add_assigned_package(delayed_package)

        return self._special_cases

    def _group_packages_by_destination(self):
        for package in self._packages.get_all_as_list():
            if not package.wrong_address:
                if not self._packages_by_destination[package.destination]:
                    self._packages_by_destination[package.destination] = [package]
                else:
                    self._packages_by_destination[package.destination].value.append(package)
            else:
                self._packages_by_destination['UNKNOWN_DESTINATION'] = package

    def _assign_packages_to_trucks(self):
        def get_current_capacity(truck):
            return truck.current_capacity - len(truck.assigned_packages)

        def get_best_available_truck(packages):
            all_trucks = self._trucks.trucks
            num_packages = len(packages)
            for t in all_trucks:
                if t.driver:
                    if get_current_capacity(t) >= num_packages:
                        return t
                else:
                    if get_current_capacity(t) >= num_packages:
                        return t
            raise RuntimeError('No trucks available with enough capacity for package assignment.')

        # Create new hash table tracking packages that have already been assigned.
        assigned_packages = HashTable()

        # Assign all grouped packages (and other packages sharing same destination) to our earliest-leaving truck (#1).
        truck_1: Truck = self._trucks.get_truck_by_id(1)
        for package_in_group in self._grouped_packages:
            curr_destination = package_in_group.destination
            for pckg_with_same_destination in self._packages_by_destination[curr_destination].value:
                if not pckg_with_same_destination.assigned:
                    truck_1.add_assigned_package(pckg_with_same_destination)
                    assigned_packages[pckg_with_same_destination] = truck_1

        # Assign packages with same destinations to existing assignments for truck #2.
        truck_2: Truck = self._trucks.get_truck_by_id(2)
        for pre_package in truck_2.assigned_packages:
            curr_destination = pre_package.destination
            for pckg_with_same_destination in self._packages_by_destination[curr_destination].value:
                if not pckg_with_same_destination.assigned:
                    truck_2.add_assigned_package(pckg_with_same_destination)
                    assigned_packages[pckg_with_same_destination] = truck_2

        assign_to_truck_1 = True
        # Assign remaining packages with deadlines to truck 1 (earliest to leave) if possible, otherwise truck 2 if
        # possible, otherwise to the first truck without a driver that has capacity.
        remaining_packages_with_deadline = [p for p in self._packages.get_all_as_list() if p.deadline and not p.assigned]
        for package_with_deadline in remaining_packages_with_deadline:
            packages_with_same_destination = self._packages_by_destination[package_with_deadline.destination].value
            packages_to_add = []
            for pckg in packages_with_same_destination:
                if not pckg.assigned and pckg not in packages_to_add:
                    packages_to_add.append(pckg)
            num_packages_to_add = len(packages_to_add)
            if get_current_capacity(truck_1) - num_packages_to_add >= 0 and assign_to_truck_1:
                truck = truck_1
                assign_to_truck_1 = False
            elif get_current_capacity(truck_2) - num_packages_to_add >= 0:
                truck = truck_2
                assign_to_truck_1 = True
            else:
                warnings.warn(message='Warning: Package(s) with deadline assigned to truck without driver.')
                other_available_trucks = [t for t in self._trucks.trucks if
                                          not t.driver and t.current_capacity - num_packages_to_add >= 0]
                if not other_available_trucks:
                    raise RuntimeError('No more trucks available!')
                truck = other_available_trucks[0]
            for pckg_to_add in packages_to_add:
                truck.add_assigned_package(pckg_to_add)
                assigned_packages[pckg_to_add] = truck

        # Assign all remaining packages to trucks where available.
        for package in self._packages.get_all_as_list():
            if not package.assigned and not assigned_packages[package]:
                group_by_destination = self._packages_by_destination[package.destination].value
                truck = get_best_available_truck(group_by_destination)
                for package_in_group in group_by_destination:
                    if len(group_by_destination) == 1:
                        package_in_group.not_special = True
                    if not package_in_group.assigned and not assigned_packages[package_in_group]:
                        truck.add_assigned_package(package_in_group)
                        assigned_packages[package_in_group] = truck

    def _load_packages_subset(self, subset, curr_truck, has_deadlines=False):
        locations_to_packages_table = self._packages.locations_to_packages_table
        excessive_distance = 5.0
        # Chain previous subset (if it exists) with current subset.
        if not has_deadlines and curr_truck.packages_queue.get_size() > 1:
            most_recent_packages_loaded, _ = curr_truck.packages_queue.peek_last()
            most_recent_destination = most_recent_packages_loaded[0].destination
            start_shortest_paths = self._all_shortest_paths[most_recent_destination].value
            next_closest_loc, distance_to_next = start_shortest_paths.get_closest_from_group(subset)
        else:
            # Find the shortest path within the first subset, starting from the HUB.
            next_closest_loc, distance_to_next = self._hub_shortest_paths.get_closest_from_group(subset)
        while next_closest_loc:
            curr_time = curr_truck.tracked_current_time
            curr_loc = next_closest_loc
            # Add next closest location to truck's packages linked list if it wouldn't miss deadline.
            packages_at_next_closest_loc = [p for p in locations_to_packages_table[curr_loc].value
                                            if not p.wrong_address]
            truck_3: Truck = self._trucks.get_truck_by_id(3)
            if (
                    curr_truck != truck_3
                    and len(packages_at_next_closest_loc) == 1
                    and packages_at_next_closest_loc[0].not_special
                    and len(truck_3.assigned_packages) - 1 >= 0
                    and distance_to_next >= excessive_distance
            ):
                for package_at_next in packages_at_next_closest_loc:
                    curr_truck.remove_assigned_package(package_at_next)
                    truck_3.add_assigned_package(package_at_next)
                subset.remove(curr_loc)
                next_shortest_paths = self._all_shortest_paths[curr_loc].value
                next_closest_loc, distance_to_next = next_shortest_paths.get_closest_from_group(subset)
                continue

            closest_deadline_package = None

            if has_deadlines:
                curr_packages_with_deadlines = [p for p in packages_at_next_closest_loc if p.deadline]
                closest_deadline_package = min(curr_packages_with_deadlines, key=lambda p: p.deadline)

            travel_time = self.calculate_time_from_miles(distance_to_next)
            curr_travel_distance = sum(info[1] for info in curr_truck.packages_queue) + distance_to_next

            if not has_deadlines or \
                    (has_deadlines and curr_time + travel_time <= closest_deadline_package.deadline):
                curr_truck.load_bundle(packages_at_next_closest_loc, distance_to_next, curr_travel_distance)
                curr_truck.assigned_packages = [p for p in curr_truck.assigned_packages
                                                if p.destination != next_closest_loc]
            else:
                raise RuntimeError('Deadline will be missed for current group of packages!')
            # Remove current location from current subset
            subset.remove(curr_loc)
            curr_time += self.calculate_time_from_miles(distance_to_next)
            curr_truck.tracked_current_time = curr_time

            next_shortest_paths = self._all_shortest_paths[curr_loc].value
            next_closest_loc, distance_to_next = next_shortest_paths.get_closest_from_group(subset)

    def load_packages(self):
        trucks_with_drivers = [t for t in self._trucks.trucks if t.driver]
        for current_truck in trucks_with_drivers:
            current_truck.load_bundle(packages=None, distance_to_next=0, curr_travel_distance=-1)

            # Separate packages with deadlines from packages without.
            subset_with_deadlines = list(set(p.destination for p in current_truck.assigned_packages if p.deadline))
            subset_without_deadlines = list(set(p.destination for p in current_truck.assigned_packages if not p.deadline
                                                and p.destination not in subset_with_deadlines))

            self._load_packages_subset(subset_with_deadlines, current_truck, has_deadlines=True)
            self._load_packages_subset(subset_without_deadlines, current_truck, has_deadlines=False)

    def deliver_packages(self):
        def update_wrong_address_packages():
            packages_to_update = [p for p in self._packages.get_all_as_list() if p.wrong_address]
            for package in packages_to_update:
                package.destination = self._locations.get_location(CORRECTED_ADDRESS)
                package.wrong_address = False

        def update_travel_distance(prev_location, curr_location):
            prev_paths = self._all_shortest_paths[prev_location].value
            path_to_curr = prev_paths.get_shortest_path(curr_location)
            new_travel_distance = path_to_curr[-1][1]
            return new_travel_distance

        def load_idle_truck(truck):
            truck.load_bundle(packages=None, distance_to_next=0, curr_travel_distance=-1)
            full_set = list(set(p.destination for p in truck.assigned_packages if not p.wrong_address))
            self._load_packages_subset(full_set, truck, has_deadlines=False)

            wrong_address_packages = list(set(p for p in truck.assigned_packages if p.wrong_address))
            for package in wrong_address_packages:
                truck.load_bundle(packages=[package], distance_to_next=math.inf, curr_travel_distance=math.inf)

        def complete_route(truck, time, location):
            while not truck.packages_queue.is_empty():
                prev_location = location

                if time >= CORRECTED_ADDRESS_TIME:
                    update_wrong_address_packages()

                # Get bundle of packages addressed to next destination in queue.
                packages_bundle, travel_distance = truck.packages_queue.get()
                # Ignore destination if it's our current location.
                if travel_distance == 0:
                    continue

                # Infinity travel distance was previously given to package(s) with wrong destination address.
                if math.isinf(travel_distance):
                    curr_corrected_location = packages_bundle[0].destination
                    travel_distance = update_travel_distance(prev_location, curr_corrected_location)

                travel_time = self.calculate_time_from_miles(travel_distance)
                time += travel_time
                location = packages_bundle[0].destination

                # Update current truck's current time, location, and total mileage.
                truck.current_time = time
                truck.miles_traveled += travel_distance
                truck.set_current_location(location, time, truck.miles_traveled)

                for package in packages_bundle:
                    truck.deliver_package(package, time)

            return time, location

        trucks_with_drivers = [t for t in self._trucks.trucks if t.driver]

        for truck in trucks_with_drivers:
            curr_time = truck.current_time = truck.departure_time
            curr_location = truck.current_location

            curr_time, curr_location = complete_route(truck, curr_time, curr_location)

            trucks_without_drivers = [t for t in self._trucks.trucks if not t.driver and t.assigned_packages]
            # If there are trucks with packages at HUB, current driver will return to HUB to pick it up and deliver.
            if not trucks_without_drivers:
                continue

            # Get path and distance to hub from current location after completing route.
            paths_from_curr_location = self._all_shortest_paths[curr_location].value
            path_to_hub = paths_from_curr_location.get_shortest_path(self._hub)
            distance_to_hub = path_to_hub[-1][1]

            # Update time and truck's location and mileage
            travel_time_to_hub = self.calculate_time_from_miles(distance_to_hub)
            curr_time += travel_time_to_hub
            curr_location = self._hub
            truck.current_time = curr_time
            truck.miles_traveled += distance_to_hub
            truck.set_current_location(curr_location, curr_time, truck.miles_traveled)

            # Switch drivers and load idle truck at hub.
            next_truck = trucks_without_drivers[0]
            next_truck.current_time = next_truck.departure_time = next_truck.tracked_current_time = curr_time
            next_truck.driver, truck.driver = truck.driver, None
            load_idle_truck(next_truck)

            complete_route(next_truck, curr_time, curr_location)

        # def timedelta_to_time(td: timedelta):
        #     total_seconds = td.total_seconds()
        #     hours = total_seconds // 3600
        #     minutes = (total_seconds % 3600) // 60
        #     seconds = total_seconds % 60
        #     return time(int(hours), int(minutes), int(seconds))
        #
        # def calculate_miles_from_time(time: timedelta):
        #     return time.total_seconds() / 3600 * TRUCK_SPEED
        #
        # for truck in self._trucks.trucks:
        #     print(truck)
        #     for loc, t, m in truck.location_by_time_list:
        #         print(f'{loc} | {timedelta_to_time(t)} | {m}')
        #
        # for package in self._packages.get_all():
        #     print(f'Package #{package.id}  on Truck #{package.truck_id}')
        #     for td, status in package.status_at_times:
        #         print(f'{timedelta_to_time(td)} | {status}')

    def get_packages(self):
        return self._packages

    def get_trucks(self):
        return self._trucks
