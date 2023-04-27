from graph.dijkstra import Dijkstra
from data.loader import Loader
from .location import Location
from hash.hash import HashTable
from graph.graph import Graph


class Locations:

    def __init__(self, distance_table_csv):
        self.distance_table_csv = distance_table_csv
        self.locations_table = HashTable(60)
        self.graph = Graph()
        self.loader = Loader(self.distance_table_csv)
        self.add_all_locations()

    def get_location(self, address):
        return self.locations_table.get_node(address).value

    def get_all_locations(self):
        return [loc_node.value for loc_node in self.locations_table.get_all()]

    def add(self, address, zip_code):
        new_loc = Location(address, zip_code)
        return self.locations_table.add(new_loc.get_key(), new_loc)

    def add_all_locations(self):
        # Manually entering our Hub information with address as "HUB" for clarity
        self.add('HUB', '84107')

        for address, zip_code in self.loader.extract_address_zip_pairs():
            self.add(address, zip_code)
        self.add_adjacencies_from_data()
        self.add_all_vertices_and_edges()

    def add_adjacencies_from_data(self):
        for source, target, weight in self.loader.extract_source_target_weights():
            source_node = self.locations_table.get_node(source)
            target_node = self.locations_table.get_node(target)
            source_node.value.add_adjacent(target_node.value, weight)
            target_node.value.add_adjacent(source_node, weight)

    def add_all_vertices_and_edges(self):
        for loc_object in self.get_all_locations():
            self.graph.add_vertex(loc_object.get_key())
        for source_node in self.locations_table.get_all():
            for adj_tuple in source_node.value.get_adjacency_list():
                target_loc = adj_tuple[0]
                weight = adj_tuple[1]
                self.graph.add_weighted_edge(source_node.value, target_loc, weight)

    def get_graph(self):
        return self.graph

