from graph.dijkstra import Dijkstra
from data.locations_loader import LocationsLoader
from .location import Location
from data_structures.hash import HashTable
from graph.graph import Graph


class Locations:

    def __init__(self, distance_table_csv):
        self.distance_table_csv = distance_table_csv
        self.locations_table = HashTable(60)
        self.graph = Graph()
        self.loader = LocationsLoader(self.distance_table_csv)
        self._add_all_locations()
        self._add_adjacencies_from_data()
        self._add_all_vertices_and_edges()

    def _add_all_locations(self):
        for address, zip_code in self.loader.get_address_zip_pairs():
            self.add(address, zip_code)

    def _add_adjacencies_from_data(self):
        for source_location, target_location, distance in self.loader.extract_source_target_weights():
            source_node = self.locations_table.get_node(source_location)
            target_node = self.locations_table.get_node(target_location)
            source_node.value.add_adjacent(target_node.value, distance)
            target_node.value.add_adjacent(source_node.value, distance)

    def _add_all_vertices_and_edges(self):
        for loc_object in self.get_all_locations():
            self.graph.add_vertex(loc_object)
        for source_node in self.locations_table.get_all():
            for adjacency_info in source_node.value.adjacency_list:
                target_loc = adjacency_info[0]
                weight = adjacency_info[1]
                self.graph.add_weighted_edge(source_node.value, target_loc, weight)

    def add(self, address, zip_code):
        new_loc = Location(address.strip(), zip_code)
        self.locations_table.add_node(new_loc.get_key(), new_loc)

    def get_location(self, address):
        try:
            return self.locations_table.get_node(address.strip()).value
        except AttributeError:
            for location in self.get_all_locations():
                full_address = location.get_key()
                if address.startswith(full_address[:5]):
                    return location
            return None

    def get_all_locations(self):
        return [loc_node.value for loc_node in self.locations_table.get_all()]

    def get_graph(self):
        return self.graph
