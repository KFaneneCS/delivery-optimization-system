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
        self._ordered_locations = MinPriorityQueue()
        self._find_all_shortest_paths()
        self._find_full_ideal_route()
        self._hub_shortest_paths = self._all_shortest_paths.get_node(self._hub).value
        self._packages = Packages(
            package_csv=PACKAGES_FILE,
            shortest_paths=self._hub_shortest_paths,  # FIXME
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
        self._delayed_packages_arrival_time = END_OF_DAY
        self._truck_handling_delayed = None
        self._package_status_by_time_table = HashTable()
        self._handle_special_cases()
        self._load_packages()

    @staticmethod
    def _timedelta_to_dt_formatted(td: timedelta):
        today = datetime.today().date()
        dt = datetime.combine(today, datetime.min.time()) + td
        return dt.strftime("%H:%M:%S")

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

        def handle_grouped_packages(pckg: Package):
            special_note = pckg.special_notes
            curr_id = int(pckg.id)
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

        for package in self._packages.packages:
            if package.status != 'Delayed':
                package.set_status(Package.STATUSES[0], BEGINNING_OF_DAY)

        for truck in self._trucks.trucks:
            if not truck.driver:
                truck.departure_time = END_OF_DAY

        delayed_package_truck = self._truck_handling_delayed
        curr_priority_value = 1

        truck_taking_group = self._trucks.get_truck_by_id(1)
        truck_taking_group.current_capacity -= len(self._grouped_packages)
        for package in self._grouped_packages:
            package.truck_id = truck_taking_group.id
            package.space_already_allocated = True

        while not self._ordered_locations.is_empty():
            location, distance = self._ordered_locations.get()

            if location.address == 'HUB':
                continue

            destination_packages = self._locations_to_packages_table.get_node(location).value
            curr_truck = self._trucks.find_available_truck(current_time=START_TIME, assoc_packages=destination_packages)
            for package in destination_packages:
                package.priority = curr_priority_value
                if package.status == 'Delayed' or package.wrong_address:
                    curr_truck = delayed_package_truck
                    package.truck_id = curr_truck.id
                if not package.truck_id:
                    package.truck_id = curr_truck.id
                curr_priority_value += 1

                if package.destination in [pckg.destination for pckg in self._grouped_packages]:
                    package.space_already_allocated = True

            self._trucks.load_packages(packages=destination_packages, current_time=START_TIME)

    def deliver_packages(self):
        def process_package(truck, curr_loc, curr_destination, curr_time, temp_storage):
            curr_package: Package = truck.packages_queue.get()

            if curr_package.status == 'Delayed':
                curr_package.set_status(Package.STATUSES[2], truck.departure_time)
                if curr_package.ready_time > curr_time:
                    temp_storage.append(curr_package)
                    return curr_loc, curr_destination, curr_time

            if curr_package.wrong_address:
                if not curr_package.ready_time <= curr_time:
                    curr_package.set_status(Package.STATUSES[2], truck.departure_time)
                    temp_storage.append(curr_package)
                    return curr_loc, curr_destination, curr_time
                curr_package.wrong_address = False
                new_destination = self._locations.get_location(address=CORRECTED_ADDRESS)
                curr_package.destination = new_destination

            elif curr_package.status != 'En Route':
                curr_package.set_status(Package.STATUSES[2], truck.departure_time)

            if curr_destination != curr_package.destination:
                curr_shortest_paths: Dijkstra = self._all_shortest_paths.get_node(curr_loc).value
                curr_destination: Location = curr_package.destination
                truck.location_by_time_list.append((curr_time, curr_loc))

                curr_route = curr_shortest_paths.get_shortest_path(curr_destination)
                distance = curr_route[-1][1]
                truck.miles_traveled += distance

                travel_time = timedelta(hours=(distance / TRUCK_SPEED))
                curr_time += travel_time
                truck.current_time += travel_time

                curr_loc = curr_destination

            curr_package.set_status(Package.STATUSES[3], curr_time)
            delivered_packages.add_node(unhashed_key=curr_package, value=(truck, curr_time))
            truck.delivered_packages.append(curr_package)
            truck.current_location = curr_loc

            return curr_loc, curr_destination, curr_time

        def return_and_switch_trucks(truck, curr_loc, curr_time):
            print(f'RETURN + SWITCHING:  Truck #{truck.id} @ {curr_time}  starting at -> {curr_loc}')
            curr_shortest_paths = self._all_shortest_paths.get_node(curr_loc).value
            route_to_hub = curr_shortest_paths.get_shortest_path(self._hub)
            distance = route_to_hub[-1][1]
            truck.miles_traveled += distance
            travel_time = timedelta(hours=(distance / TRUCK_SPEED))
            curr_time += travel_time
            truck.current_time += travel_time
            curr_loc = self._hub

            new_truck = trucks_without_drivers.pop(0)
            new_truck.driver = truck.driver
            new_truck.departure_time = curr_time
            truck.driver = None

            return new_truck, curr_loc, curr_time

        def process_truck(truck, curr_time, curr_location, curr_destination, temp_storage):
            while not truck.packages_queue.is_empty() or temp_storage:
                if temp_storage:
                    earliest_ready_time = min(pckg.ready_time for pckg in temp_storage)
                    if truck.packages_queue.get_size() == 1 and truck.packages_queue.peek().ready_time < earliest_ready_time:
                        curr_time = earliest_ready_time
                    for i, stored_package in enumerate(temp_storage):
                        if not delivered_packages.get_node(stored_package) and stored_package.ready_time <= curr_time:
                            truck.packages_queue.insert(priority=stored_package.priority, information=stored_package)
                            temp_storage.pop(i)

                curr_location, curr_destination, curr_time = process_package(truck, curr_location, curr_destination, curr_time, temp_storage)
            return curr_location, curr_destination, curr_time

        delivered_packages = HashTable()
        trucks_with_drivers = [tr for tr in self._trucks.trucks if tr.driver]
        trucks_without_drivers = [tr for tr in self._trucks.trucks if not tr.driver]

        finished_trucks = MinPriorityQueue()

        for truck in trucks_with_drivers:
            curr_time = truck.departure_time
            curr_location = truck.current_location
            curr_destination = None
            temp_storage = []

            curr_location, curr_destination, curr_time = process_truck(truck, curr_time, curr_location,
                                                                       curr_destination, temp_storage)

            # Add truck/driver to queue after finishing root; finish time is priority value.
            finished_trucks.insert(curr_time, truck)

        while trucks_without_drivers and not finished_trucks.is_empty():
            # First truck/driver to have finished their route.
            finished_truck = finished_trucks.get()

            finished_truck, curr_location, curr_time = return_and_switch_trucks(finished_truck, curr_location,
                                                                                curr_time)
            curr_destination = None
            temp_storage = []

            curr_location, curr_destination, curr_time = process_truck(finished_truck, curr_time, curr_location,
                                                                       curr_destination, temp_storage)

            finished_trucks.insert(curr_time, finished_truck)

        # FIXME:  Testing
        print('\n\n')
        for x, y in self._packages.get_all_statuses_by_time():
            print(f'{x.id}  |  Truck #{x.truck_id}  |  {[(self._timedelta_to_dt_formatted(t[0]), t[1]) for t in y]}')

        for truck in self._trucks.trucks:
            print(truck)
            for x, y in truck.location_by_time_list:
                print(f'{self._timedelta_to_dt_formatted(x)}  | {y}')

    # def deliver_packages(self):
    #     delivered_packages = HashTable()
    #     trucks_with_drivers = [tr for tr in self._trucks.trucks if tr.driver]
    #     trucks_without_drivers = [tr for tr in self._trucks.trucks if not tr.driver]
    #
    #     for truck in trucks_with_drivers:
    #         # print(f'CURRENT TRUCK:  {truck}')
    #         curr_time = truck.departure_time
    #         curr_location = truck.current_location
    #         curr_destination = None
    #         temp_storage = []
    #
    #         while not truck.packages_queue.is_empty() or temp_storage:
    #
    #             if temp_storage:
    #                 # print('TEMP triggered')
    #                 earliest_ready_time = min(pckg.ready_time for pckg in temp_storage)
    #                 # print(f'Earliest ready time == {earliest_ready_time}')
    #                 if truck.packages_queue.get_size() == 1 and truck.packages_queue.peek().ready_time < earliest_ready_time:
    #                     curr_time = earliest_ready_time
    #                     # print('  Part 2')
    #                 for i, stored_package in enumerate(temp_storage):
    #                     if not delivered_packages.get_node(stored_package) and stored_package.ready_time <= curr_time:
    #                         truck.packages_queue.insert(priority=stored_package.priority, information=stored_package)
    #                         temp_storage.pop(i)
    #                         # print('  Part 3')
    #
    #             curr_package: Package = truck.packages_queue.get()
    #
    #             if curr_package.status == 'Delayed':
    #                 curr_package.set_status(Package.STATUSES[2], truck.departure_time)
    #                 if curr_package.ready_time > curr_time:
    #                     temp_storage.append(curr_package)
    #                     continue
    #             elif curr_package.wrong_address and not curr_package.ready_time <= curr_time:
    #                 curr_package.set_status(Package.STATUSES[2], truck.departure_time)
    #                 temp_storage.append(curr_package)
    #                 continue
    #             elif curr_package.wrong_address and curr_package.ready_time <= curr_time:
    #                 curr_package.wrong_address = False
    #                 new_destination = self._locations.get_location(address=CORRECTED_ADDRESS)
    #                 curr_package.destination = new_destination
    #             elif curr_package.status != 'En Route':
    #                 curr_package.set_status(Package.STATUSES[2], truck.departure_time)
    #
    #             if curr_destination != curr_package.destination:
    #                 curr_shortest_paths: Dijkstra = self._all_shortest_paths.get_node(curr_location).value
    #                 curr_destination: Location = curr_package.destination
    #                 truck.location_by_time_list.append((curr_time, curr_location))
    #
    #                 curr_route = curr_shortest_paths.get_shortest_path(curr_destination)
    #                 distance = curr_route[-1][1]
    #                 truck.miles_traveled += distance
    #
    #                 travel_time = timedelta(hours=(distance / TRUCK_SPEED))
    #                 curr_time += travel_time
    #                 truck.current_time += travel_time
    #
    #                 curr_location = curr_destination
    #
    #             curr_package.set_status(Package.STATUSES[3], curr_time)
    #             delivered_packages.add_node(unhashed_key=curr_package, value=(truck, curr_time))
    #             truck.delivered_packages.append(curr_package)
    #             truck.current_location = curr_location
    #
    #         if trucks_without_drivers:
    #             # Head back to HUB
    #             curr_shortest_paths = self._all_shortest_paths.get_node(curr_location).value
    #             route_to_hub = curr_shortest_paths.get_shortest_path(self._hub)
    #             distance = route_to_hub[-1][1]
    #             truck.miles_traveled += distance
    #             travel_time = timedelta(hours=(distance / TRUCK_SPEED))
    #             curr_time += travel_time
    #             truck.current_time += travel_time
    #             curr_location = self._hub
    #
    #             #Switch trucks
    #             new_truck = trucks_without_drivers.pop(0)
    #             new_truck.driver = truck.driver
    #             truck.driver = None
    #
    #             curr_location = truck.current_location
    #             curr_destination = None
    #             temp_storage = []
    #             truck = new_truck
    #
    #             while not truck.packages_queue.is_empty() or temp_storage:
    #
    #                 if temp_storage:
    #                     earliest_ready_time = min(pckg.ready_time for pckg in temp_storage)
    #                     if truck.packages_queue.get_size() == 1 and truck.packages_queue.peek().ready_time < earliest_ready_time:
    #                         curr_time = earliest_ready_time
    #                     for i, stored_package in enumerate(temp_storage):
    #                         if not delivered_packages.get_node(
    #                                 stored_package) and stored_package.ready_time <= curr_time:
    #                             truck.packages_queue.insert(priority=stored_package.priority,
    #                                                         information=stored_package)
    #                             temp_storage.pop(i)
    #
    #                 curr_package: Package = truck.packages_queue.get()
    #
    #                 if curr_package.status == 'Delayed':
    #                     curr_package.set_status(Package.STATUSES[2], truck.departure_time)
    #                     if curr_package.ready_time > curr_time:
    #                         temp_storage.append(curr_package)
    #                         continue
    #                 elif curr_package.wrong_address and not curr_package.ready_time <= curr_time:
    #                     curr_package.set_status(Package.STATUSES[2], truck.departure_time)
    #                     temp_storage.append(curr_package)
    #                     continue
    #                 elif curr_package.wrong_address and curr_package.ready_time <= curr_time:
    #                     curr_package.wrong_address = False
    #                     new_destination = self._locations.get_location(address=CORRECTED_ADDRESS)
    #                     curr_package.destination = new_destination
    #                 elif curr_package.status != 'En Route':
    #                     curr_package.set_status(Package.STATUSES[2], truck.departure_time)
    #
    #                 if curr_destination != curr_package.destination:
    #                     curr_shortest_paths: Dijkstra = self._all_shortest_paths.get_node(curr_location).value
    #                     curr_destination: Location = curr_package.destination
    #                     truck.location_by_time_list.append((curr_time, curr_location))
    #
    #                     curr_route = curr_shortest_paths.get_shortest_path(curr_destination)
    #                     distance = curr_route[-1][1]
    #                     truck.miles_traveled += distance
    #
    #                     travel_time = timedelta(hours=(distance / TRUCK_SPEED))
    #                     curr_time += travel_time
    #                     truck.current_time += travel_time
    #
    #                     curr_location = curr_destination
    #
    #                 curr_package.set_status(Package.STATUSES[3], curr_time)
    #                 delivered_packages.add_node(unhashed_key=curr_package, value=(truck, curr_time))
    #                 truck.delivered_packages.append(curr_package)
    #                 truck.current_location = curr_location
    #
    #     # FIXME:  Testing
    #     print('\n\n')
    #     for x, y in self._packages.get_all_statuses_by_time():
    #         print(f'{x.id}  |  Truck #{x.truck_id}  |  {[(self._timedelta_to_dt_formatted(t[0]), t[1]) for t in y]}')
    #
    #     for truck in self._trucks.trucks:
    #         print(truck)
    #         for x, y in truck.location_by_time_list:
    #             print(f'{self._timedelta_to_dt_formatted(x)} | {y}')
