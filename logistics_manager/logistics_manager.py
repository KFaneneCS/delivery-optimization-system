import re
import warnings
from datetime import datetime, timedelta

from data_structures.hash import HashTable
from data_structures.priority_queue import PriorityQueue
from data_structures.linked_list import LinkedList
from graph.dijkstra import Dijkstra
from locations.location import Location
from locations.locations import Locations
from packages.packages import Package, Packages
from trucks.trucks import Truck, Trucks

LOCATIONS_FILE = 'data/distance_table.csv'
PACKAGES_FILE = 'data/package_file.csv'
TRUCK_SPEED = 18
BEGINNING_OF_DAY = timedelta(hours=0, minutes=0)
END_OF_DAY = timedelta(hours=23, minutes=59, seconds=59)
START_TIME = timedelta(hours=8, minutes=0)
CLOSING_TIME = timedelta(hours=17, minutes=0)
CORRECTED_ADDRESS_TIME = timedelta(hours=10, minutes=20)
CORRECTED_ADDRESS = '410 S State St'


class LogisticsManager:
    def __init__(self):
        self._locations = Locations(LOCATIONS_FILE)
        self._hub = self._locations.get_location('HUB')
        self._graph = self._locations.get_graph()
        self._all_shortest_paths = HashTable()
        self._ordered_locations = PriorityQueue(is_max=False)
        self._find_all_shortest_paths()
        # self._find_full_ideal_route()
        self._hub_shortest_paths = self._all_shortest_paths[self._hub].value
        self._packages = Packages(
            package_csv=PACKAGES_FILE,
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
        self._packages_by_destination = HashTable(len(self._locations.get_all_locations()) * 2)
        self._delayed_packages = []
        self._delayed_packages_arrival_time = END_OF_DAY
        self._truck_handling_delayed = None
        self._package_status_by_time_table = HashTable()
        self._handle_special_cases()
        self._combine_packages_with_same_destination()
        self._handle_package_assignments()
        self._load_packages()
        # self._ready_packages()

    def test(self):
        print('\n\n')
        for x, y in self._packages.get_all_statuses_by_time():
            print(
                f'{x.id}  |  Truck #{x.truck_id}  |  {[(self._timedelta_to_dt_formatted(t[0]), t[1]) for t in y]}')

        for truck in self._trucks.trucks:
            print(truck)
            for x, y in truck.location_by_time_list:
                # print(f'{self._timedelta_to_dt_formatted(x)}  | {y}')
                print(f'{x}  |  {y}')

    @staticmethod
    def _timedelta_to_dt_formatted(td: timedelta):
        today = datetime.today().date()
        dt = datetime.combine(today, datetime.min.time()) + td
        return dt.strftime("%H:%M:%S")

    def _find_all_shortest_paths(self):
        for location in self._locations.get_all_locations():
            shortest_path = Dijkstra(location, self._graph)
            self._all_shortest_paths[location] = shortest_path

    # def _find_full_ideal_route(self):
    # current: Dijkstra = self._all_shortest_paths.get_node(self._hub).value
    # total_distance = 0
    # visited = {self._hub}
    # self._ordered_locations.insert(0, (current.start, total_distance))
    #
    # for i in range(current.distance_table.get_size() - 1):
    #     next_location, distance = current.get_closest_from_start(visited)
    #     self._ordered_locations.insert(i + 1, (next_location, distance))
    #     visited.add(next_location)
    #     total_distance += distance
    #     current = self._all_shortest_paths.get_node(next_location).value

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
            pckg.ready_time = self._delayed_packages_arrival_time

        def handle_wrong_address(pckg: Package):
            pckg.wrong_address = True
            pckg.ready_time = CORRECTED_ADDRESS_TIME
            trucks_without_drivers = [t for t in self._trucks.trucks if not t.driver]
            # Assign package to first truck without driver since address will not be known for some time.
            trucks_without_drivers[0].add_assigned_package(pckg)

        def handle_grouped_packages(pckg: Package):
            special_note = pckg.special_notes
            curr_id = int(pckg.id)
            other_package_ids = [int(num) for num in re.findall(r'\d+', special_note)]
            combined_ids = other_package_ids + [curr_id]

            for package_id in combined_ids:
                package_to_add = self._packages.get_package_by_id(package_id)
                if package_to_add and package_to_add not in self._grouped_packages:
                    self._grouped_packages.append(package_to_add)
                    self._seen_addresses[package_to_add.destination] = None
            # for other_package in self._packages.packages:
            #     if (other_package not in self._grouped_packages) and self._seen_addresses.get_node(
            #             other_package.destination):
            #         self._grouped_packages.append(other_package)

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

        for package in self._packages.packages:
            curr_notes = package.special_notes
            for note, handling_method in self._special_cases.items():
                if curr_notes.startswith(note):
                    handling_method(package)

        return self._special_cases

    def _combine_packages_with_same_destination(self):
        for package in self._packages.packages:
            if not package.wrong_address:
                if not self._packages_by_destination[package.destination]:
                    self._packages_by_destination[package.destination] = [package]
                else:
                    self._packages_by_destination[package.destination].value.append(package)
            else:
                self._packages_by_destination['UNKNOWN_DESTINATION'] = package

    def _handle_package_assignments(self):
        def get_current_capacity(truck):
            return truck.current_capacity - len(truck.assigned_packages)

        def get_best_available_truck():
            all_trucks = self._trucks.trucks
            for t in all_trucks:
                if t.driver:
                    if t.current_capacity - len(t.assigned_packages) >= 1:
                        return t
                else:
                    if t.current_capacity - len(t.assigned_packages) >= 1:
                        return t
            raise RuntimeError('No trucks available with enough capacity for package assignment.')

        def test_preassignments():
            for p in self._packages.packages:
                print(p)

            for t in self._trucks.trucks:
                print(t)
                for x in t.assigned_packages:
                    print(x)

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

        # Assign remaining packages with deadlines to truck 1 (earliest to leave) if possible, otherwise truck 2 if
        # possible, otherwise to the first truck without a driver that has capacity.
        remaining_packages_with_deadline = [p for p in self._packages.packages if p.deadline and not p.assigned]
        for package_with_deadline in remaining_packages_with_deadline:
            packages_with_same_destination = self._packages_by_destination[package_with_deadline.destination].value
            packages_to_add = []
            for pckg in [package_with_deadline] + packages_with_same_destination:
                if not pckg.assigned and pckg not in packages_to_add:
                    packages_to_add.append(pckg)
            packages_to_add = [p for p in packages_to_add if not p.assigned]
            num_packages_to_add = len(packages_to_add)
            if get_current_capacity(truck_1) - num_packages_to_add >= 0:
                truck = truck_1
            elif get_current_capacity(truck_2) - num_packages_to_add >= 0:
                truck = truck_2
            else:
                warnings.warn(message='Warning: Package(s) with deadline assigned to truck without driver.')
                other_available_trucks = [t for t in self._trucks.trucks if
                                          not t.driver and t.current_capacity - num_packages_to_add >= 0]
                truck = other_available_trucks[0]
            for pckg_to_add in packages_to_add:
                truck.add_assigned_package(pckg_to_add)
                assigned_packages[pckg_to_add] = truck

        # Assign all remaining packages to trucks where available.
        for package in self._packages.packages:
            if not package.assigned and not assigned_packages[package]:
                truck = get_best_available_truck()
                truck.add_assigned_package(package)
                assigned_packages[package] = truck

        # test_preassignments()

    def _load_packages(self):
        self._locations_to_packages_table.print_all()

        def get_deadline_as_miles(curr_time: timedelta, deadline_time: timedelta):
            remaining_time = deadline_time - curr_time
            remaining_distance = remaining_time.total_seconds() / 3600 * TRUCK_SPEED
            return remaining_distance

        all_trucks = self._trucks.trucks
        for truck in all_trucks:
            truck.packages_linked_list.add_link(value=self._hub, accumulated_distance=0)
            curr_time = truck.departure_time

            # Separate packages with deadlines from packages without.
            subset_with_deadlines = [p.destination for p in truck.assigned_packages if p.deadline]
            subset_without_deadlines = [p.destination for p in truck.assigned_packages if not p.deadline]

            # Find the shortest path within the first subset, starting from the HUB.
            next_closest_loc, distance_to_next = self._hub_shortest_paths.get_closest_from_group(subset_with_deadlines)
            while next_closest_loc:
                # Add next closest location to truck's packages linked list if it wouldn't miss deadline.
                packages_at_next_closest_loc = self._locations_to_packages_table[next_closest_loc].value
                closest_deadline = min(packages_at_next_closest_loc, key=lambda p: p.deadline)
                curr_last_link = truck.packages_linked_list.tail
                deadline_in_miles = get_deadline_as_miles(curr_time, closest_deadline)
                curr_distance_traveled = curr_last_link.accumulated_distance + distance_to_next
                if curr_distance_traveled <= deadline_in_miles:
                    truck.packages_linked_list.add_link(value=next_closest_loc, accumulated_distance=curr_distance_traveled)
                else:
                    # TODO:  Continue here.  Logic will be a bit complicated.

            # Then find the shortest path from last location of previous subset and add on 2nd subset (non-deadlines).

            # Load packages based on entire shortest path

    # def _ready_packages(self):
    # # Iterate over all packages and update their status.
    # for package in self._packages.packages:
    #     if package.status != 'Delayed':
    #         package.set_status(Package.STATUSES[0], BEGINNING_OF_DAY)
    #
    # # Set departure time for trucks without drivers from the start to the default end of day.
    # for truck in self._trucks.trucks:
    #     if not truck.driver:
    #         truck.departure_time = END_OF_DAY
    #
    # delayed_package_truck = self._truck_handling_delayed
    #
    # # Set our initial priority value to the highest possible value of 1.
    # curr_priority_value = 1
    #
    # # Predetermined the truck to take the group of packages that must stay together, then decrement that truck's
    # # capacity so that it doesn't fill up before all packages in the group are ready to be loaded.
    # truck_taking_group = self._trucks.get_truck_by_id(1)
    # truck_taking_group.current_capacity -= len(self._grouped_packages)
    # for package in self._grouped_packages:
    #     package.truck_id = truck_taking_group.id
    #     package.space_already_allocated = True
    #
    # # Fetching all (location, distance) tuples by location based on their priority, the value of which was
    # # determined by proximity previously.
    # while not self._ordered_locations.is_empty():
    #     location, distance = self._ordered_locations.get()
    #
    #     # No need to consider the HUB since we begin there and no package is addressed to it.
    #     if location.address == 'HUB':
    #         continue
    #
    #     # List of packages associated with the current location.
    #     destination_packages = self._locations_to_packages_table.get_node(location).value
    #
    #     # Finding a truck with capacity that could be used for the current set of packages, not accounting for
    #     # other package criteria.
    #     curr_truck = self._trucks.find_available_truck(current_time=START_TIME, assoc_packages=destination_packages)
    #
    #     group_truck_id = -1
    #     destination_packages_assigned = False
    #     for package in destination_packages:
    #         package.priority = curr_priority_value
    #         if package.status == 'Delayed':
    #             curr_truck = delayed_package_truck
    #             package.truck_id = curr_truck.id
    #             group_truck_id = curr_truck.id
    #             destination_packages_assigned = True
    #         if package.deadline and not package.truck_id:
    #             trucks_with_drivers = [t for t in self._trucks.trucks if t.driver]
    #             # truck_index = curr_priority_value % len(trucks_with_drivers)
    #             # package.truck_id = trucks_with_drivers[0].id
    #             onloading_truck = trucks_with_drivers[0]
    #             offloading_truck = None
    #             if onloading_truck.current_capacity > 0:
    #                 package.truck_id = onloading_truck.id
    #             else:
    #                 i = 0
    #                 while not onloading_truck.current_capacity > 0:
    #                     offloading_truck, onloading_truck = onloading_truck, trucks_with_drivers[i + 1]
    #
    #                 offloading_package_node = offloading_truck.packages_without_deadlines_queue.remove_last()
    #                 offloading_truck.current_capacity += 1
    #                 onloading_truck.packages_without_deadlines_queue.insert(offloading_package_node.priority,
    #                                                                         offloading_package_node.information)
    #                 onloading_truck.current_capacity -= 1
    #                 package.truck_id = offloading_truck.id
    #
    #         curr_priority_value += 1
    #
    #     for package in destination_packages:
    #         if destination_packages_assigned and not package.truck_id:
    #             package.truck_id = group_truck_id
    #         elif not package.truck_id:
    #             package.truck_id = curr_truck.id
    #         curr_priority_value += 1
    #
    #         if package.destination in [pckg.destination for pckg in self._grouped_packages]:
    #             package.space_already_allocated = True
    #
    #     self._trucks.load_packages(packages=destination_packages, current_time=START_TIME)
    # for p in self._packages.packages:
    #     print(p)

    # def process_packages(self, truck, curr_time, curr_location, delivered_packages):
    # print(f'Current truck: {truck.id}')
    # print('WITH deadlines')
    # print([x.id for x in truck.packages_with_deadlines_queue])
    # print('WITHOUT deadlines')
    # print([x.id for x in truck.packages_without_deadlines_queue])
    # print(f'Current time == {curr_time}\n')
    # curr_destination = None
    # temp_storage = []
    #
    # while not truck.packages_without_deadlines_queue.is_empty() or not truck.packages_with_deadlines_queue.is_empty() or temp_storage:
    #     if temp_storage:
    #         earliest_ready_time = min(pckg.ready_time for pckg in temp_storage)
    #         deadlines_queue_size = truck.packages_with_deadlines_queue.get_size()
    #         no_deadlines_queue_size = truck.packages_without_deadlines_queue.get_size()
    #
    #         if deadlines_queue_size + no_deadlines_queue_size == 1:
    #             if no_deadlines_queue_size == 1 and truck.packages_without_deadlines_queue.peek().ready_time < earliest_ready_time:
    #                 curr_time = earliest_ready_time
    #             elif deadlines_queue_size == 1 and truck.packages_with_deadlines_queue.peek().ready_time < earliest_ready_time:
    #                 curr_time = earliest_ready_time
    #
    #         for i, stored_package in enumerate(temp_storage):
    #             if not delivered_packages.get_node(stored_package) and stored_package.ready_time <= curr_time:
    #                 if stored_package.deadline:
    #                     truck.packages_with_deadlines_queue.insert(priority=stored_package.priority,
    #                                                                information=stored_package)
    #                 else:
    #                     truck.packages_without_deadlines_queue.insert(priority=stored_package.priority, information=stored_package)
    #                 temp_storage.pop(i)
    #
    #     curr_shortest_paths = self._all_shortest_paths.get_node(curr_location).value
    #
    #     same_destination_packages = []
    #     # print(f'Group before (should be empty): {same_destination_packages}')
    #
    #     next_pckg_with_deadline = truck.packages_with_deadlines_queue.peek()
    #     next_pckg_without_deadline = truck.packages_without_deadlines_queue.peek()
    #     deadline_approaching = False
    #
    #     if next_pckg_with_deadline:
    #         deadline = next_pckg_with_deadline.deadline
    #         hypothetical_route_dist = curr_shortest_paths.get_shortest_path_distance(
    #             next_pckg_with_deadline.destination)
    #         hyp_travel_time = self.dist_to_time_conversion(hypothetical_route_dist)
    #         leeway_time = timedelta(minutes=25)
    #         if deadline - (curr_time + hyp_travel_time) <= leeway_time:
    #             deadline_approaching = True
    #         if not next_pckg_without_deadline or next_pckg_with_deadline.priority < next_pckg_without_deadline.priority or deadline_approaching:
    #             curr_package_with_deadline = next_pckg_with_deadline
    #             same_destination_packages.append(truck.packages_with_deadlines_queue.get())
    #         else:
    #             same_destination_packages.append(truck.packages_without_deadlines_queue.get())
    #     else:
    #         same_destination_packages.append(truck.packages_without_deadlines_queue.get())
    #
    #     next_pckg_with_deadline = truck.packages_with_deadlines_queue.peek()
    #     next_pckg_without_deadline = truck.packages_without_deadlines_queue.peek()
    #
    #     print(f'COMPARING AGAINST:  {same_destination_packages}')
    #     print(f'   Next up w/ deadline --> {next_pckg_with_deadline}')
    #     print(f'   Next up without     --> {next_pckg_without_deadline}')
    #
    #     if deadline_approaching:
    #         matching_packages = []
    #
    #         for package in truck.packages_with_deadlines_queue:
    #             if package.destination == curr_package_with_deadline.destination:
    #                 matching_packages.append(package)
    #
    #         for package in truck.packages_without_deadlines_queue:
    #             if package.destination == curr_package_with_deadline.destination:
    #                 matching_packages.append(package)
    #
    #         if matching_packages:
    #             for matching_package in matching_packages:
    #                 if truck.packages_with_deadlines_queue.contains(matching_package):
    #                     out_of_order_package = truck.packages_with_deadlines_queue.get_by_information(matching_package)
    #                     same_destination_packages.append(out_of_order_package)
    #                 if truck.packages_without_deadlines_queue.contains(matching_package):
    #                     out_of_order_package = truck.packages_without_deadlines_queue.get_by_information(matching_package)
    #                     same_destination_packages.append(out_of_order_package)
    #
    #
    #
    #     while next_pckg_with_deadline and next_pckg_with_deadline.destination == same_destination_packages[0].destination:
    #         same_destination_packages.append(truck.packages_with_deadlines_queue.get())
    #         next_pckg_with_deadline = truck.packages_with_deadlines_queue.peek()
    #
    #     while next_pckg_without_deadline and next_pckg_without_deadline.destination == same_destination_packages[0].destination:
    #         same_destination_packages.append(truck.packages_without_deadlines_queue.get())
    #         next_pckg_without_deadline = truck.packages_without_deadlines_queue.peek()
    #
    #     print(f'After assigning sames:  {[p.id for p in same_destination_packages]}\n')
    #
    #     for package_with_same_destination in same_destination_packages:
    #         curr_package = package_with_same_destination
    #         if curr_package.status == 'Delayed':
    #             curr_package.set_status(Package.STATUSES[2], truck.departure_time)
    #             if curr_package.ready_time > curr_time:
    #                 temp_storage.append(curr_package)
    #                 continue
    #         elif curr_package.wrong_address and not curr_package.ready_time <= curr_time:
    #             print(f'  *** WRONG package triggered for pckg:  {curr_package}')
    #             curr_package.set_status(Package.STATUSES[2], truck.departure_time)
    #             print(f'     ----> Status:  {curr_package.status}')
    #             temp_storage.append(curr_package)
    #             continue
    #         elif curr_package.wrong_address and curr_package.ready_time <= curr_time:
    #             curr_package.wrong_address = False
    #             new_destination = self._locations.get_location(address=CORRECTED_ADDRESS)
    #             curr_package.destination = new_destination
    #         elif curr_package.status != 'En Route':
    #             curr_package.set_status(Package.STATUSES[2], truck.departure_time)
    #
    #         if curr_destination != curr_package.destination:
    #             curr_destination = curr_package.destination
    #             truck.location_by_time_list.append((curr_time, curr_location))
    #             curr_route = curr_shortest_paths.get_shortest_path(curr_destination)
    #             distance = curr_route[-1][1]
    #             truck.miles_traveled += distance
    #             travel_time = timedelta(hours=(distance / TRUCK_SPEED))
    #             curr_time += travel_time
    #             truck.current_time += travel_time
    #             curr_location = curr_destination
    #
    #         # if curr_package.deadline:
    #         #     if curr_time > curr_package.deadline:
    #         #         raise RuntimeError(f'Missed deadline for package #{curr_package.id}')
    #
    #         curr_package.set_status(Package.STATUSES[3], curr_time)
    #         delivered_packages.add_node(unhashed_key=curr_package, value=(truck, curr_time))
    #         truck.delivered_packages.append(curr_package)
    #         truck.current_location = curr_location
    #
    # return curr_time, curr_location

    # def deliver_packages(self):
    # delivered_packages = HashTable()
    # trucks_with_drivers = [tr for tr in self._trucks.trucks if tr.driver]
    # trucks_without_drivers = [tr for tr in self._trucks.trucks if not tr.driver]
    # print('\n')
    # print(trucks_with_drivers)
    # print(trucks_without_drivers)
    #
    # for truck in trucks_with_drivers:
    #     # print(f'Truck #{truck.id} heading out.')
    #     curr_time = truck.current_time = truck.departure_time
    #     # print(f'@ {curr_time}')
    #     curr_location = truck.current_location
    #     # print(f'location:  {curr_location}')
    #     curr_time, curr_location = self.process_packages(truck, curr_time, curr_location, delivered_packages)
    #     truck.current_time, truck.current_location = curr_time, curr_location
    #     # print('**************')
    #     # print(f'After delivery, curr time: {curr_time} and loc:  {curr_location}')
    #
    #     if trucks_without_drivers:
    #         curr_shortest_paths = self._all_shortest_paths.get_node(curr_location).value
    #         route_to_hub = curr_shortest_paths.get_shortest_path(self._hub)
    #         # print(f'route home:  {route_to_hub}')
    #         distance_to_hub = route_to_hub[-1][1]
    #         truck.miles_traveled += distance_to_hub
    #         travel_time = timedelta(hours=(distance_to_hub / TRUCK_SPEED))
    #         curr_time += travel_time
    #         # print(f'new time:  {curr_time}')
    #         truck.current_time += travel_time
    #         curr_location = truck.current_location = self._hub
    #
    #         new_truck = trucks_without_drivers.pop(0)
    #         new_truck.driver = truck.driver
    #         new_truck.departure_time = new_truck.current_time = curr_time
    #         # print(f'NEW truck:  {new_truck}  departing at {new_truck.departure_time}')
    #         truck.driver = None
    #
    #         curr_time, curr_location = self.process_packages(new_truck, curr_time, curr_location, delivered_packages)
    #         new_truck.current_time, new_truck.current_location = curr_time, curr_location
