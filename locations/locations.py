import csv

from .location import Location
from hash.hash import HashTable
from graph.graph import Graph


def read_csv(csv_file):
    if not csv_file.lower().endswith('.csv'):
        print('Please use correct file type')
        return None
    with open(csv_file, 'r') as file:
        reader = csv.reader(file)
        return [row for row in reader]


class Locations:

    def __init__(self):
        self.locations_table = HashTable(60)
        self.graph = Graph()

    def get_location(self, address):
        return self.locations_table.get_node(address)

    def get_all_locations(self):
        return [loc_node.value for loc_node in self.locations_table.get_all()]

    def add(self, address, zip_code):
        new_loc = Location(address, zip_code)
        # key = 'HUB' if new_loc.get_key() == 'HUB' else key = new_loc.get_key()
        return self.locations_table.add(new_loc.get_key(), new_loc)

    def add_all_locations(self, csv_file):
        data = read_csv(csv_file)
        # Manually entering our Hub information with address as "HUB" for clarity
        self.add('HUB', '84107')
        # First element is an empty space to represent first empty cell of the data
        full_addresses = ['']
        # Getting the first column of the data which contains each address without the name of the location
        first_col = list(map(list, zip(*data)))[0]
        for col_address in first_col:
            full_addresses.append(col_address)

        for full in full_addresses[2:]:
            address = full.split('(')[0].strip()
            zip_code = full.split('(')[1][:5]
            self.add(address, zip_code)

        # Adding the addresses from the first column to the first row of our data
        data.insert(0, full_addresses)
        self.add_adjacencies_from_data(data)
        self.add_all_vertices_and_edges()
        # for x in self.graph.get_all_adjacencies():      # FIXME: *** Not working as intended ***
        #     print(x)

    def add_adjacencies_from_data(self, data):
        for row in range(1, len(data)):
            source_address = data[row][0].split('(')[0].strip()
            source_node = self.locations_table.get_node(source_address)
            count = 0
            for col in range(1, len(data[0])):
                count += 1
                target_address = data[0][col].split('(')[0].strip()
                weight = float(data[row][col])
                # Once we hit "0.0," we are doubly referencing an address, so we move on to the next row
                if weight == 0.0:
                    break

                target_node = self.locations_table.get_node(target_address)
                # Adding weighted adjacency tuple to source and target nodes' adjacency lists
                source_node.value.add_adjacent(target_node.value, weight)
                target_node.value.add_adjacent(source_node.value, weight)

    def add_all_vertices_and_edges(self):
        for location in self.get_all_locations():
            self.graph.add_vertex(location)
        for source_node in self.locations_table.get_all():
            for adj_tuple in source_node.value.get_adjacency_list():
                target_loc = adj_tuple[0]
                weight = adj_tuple[1]
                # print(f'target loc: {target_loc}, weight {weight}')
                self.graph.add_weighted_edge(source_node.value, target_loc, weight)

        self.graph.show_all_connections()






        # addresses = []
        # zip_codes = []
        #
        # addresses.append('HUB')
        # zip_codes.append('HUB')
        # # Iterating through each row of csv file starting after 1st row.  Each odd numbered row contains the
        # # street address, while each even numbered row contains our zip.  We remove any junk information
        # # resulting from converting xlsx file to csv.
        # for row in data[1:]:
        #     if row[0] == '"':
        #         addresses.append(row[2:].strip())
        #     #
        #     else:
        #         zip_codes.append(row[1:6])
        # # 1-1 relationship between address and zip code, so we can zip the 'addresses' and 'zip_codes' lists
        # # to get our full address, then add each full address to our 'locations' hash table.
        # full_addresses = zip(addresses, zip_codes)
        # for full in full_addresses:
        #     self.add(full[0], full[1])
        #
        # self.add_all_adjacencies(data)

    # def add_all_adjacencies(self, data):
    #     print(data)
    # all_edge_weights = []
    # for row in data[2:8:2]:  # FIXME:  8 is for testing only; remove
    #     row_list = row.split(',')[1:]
    #
    #     # Creates list of tuples of hashed location and its edge weight per "distance table" file
    #     # stopping at '0.0' for each row
    #     edge_weights = [
    #         (self.hashed_locations.get_value(self.locations[i + 1]), float(val)) for (i, val) in
    #         enumerate(row_list[0:row_list.index('0.0')])
    #     ]
    #
    #     all_edge_weights.append(edge_weights)
    #
    # print(all_edge_weights)

    # for row in range(1, len(all_edge_weights)):
    #     for col in range(1, len(all_edge_weights)):
    #         print(all_edge_weights[row][col])

    # loc_index = 1
    # for row in all_edge_weights:
    #     curr_row_loc = self.hashed_locations.get_value(self.locations[loc_index])
    #
    #     for tup in row:
    #
    #         curr_col_loc = tup[0]
    #         weight = tup[1]
    #
    #         # print(curr_row_loc, curr_col_loc)
    #
    #         curr_row_loc.add_adjacent(curr_col_loc, weight)
    #         curr_col_loc.add_adjacent(curr_row_loc, weight)
    #
    #     loc_index += 1
