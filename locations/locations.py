from data.locations_loader import LocationsLoader
from data_structures.hash import HashTable
from graph.graph import Graph
from .location import Location


class Locations:
    """
    A class that instantiates and manages a collection of Location objects and provides a means of interacting with
    all Location objects.
    """

    def __init__(self, distance_table_csv):
        """
        Initializes a new instance of the Locations class.

        A number of initialization functions are called to set up each location and their relationship to each other
        using a Graph data structure.
        :param distance_table_csv: The csv file from which data for all locations is found.
        """
        self.distance_table_csv = distance_table_csv
        self.locations_table = HashTable(70)
        self.graph = Graph()
        self.loader = LocationsLoader(self.distance_table_csv)
        self._add_all_locations()
        self._add_adjacencies_from_data()
        self._add_all_vertices_and_edges()

    def _add_all_locations(self):
        """
        Initialization function that calls the loader to add all locations to the locations hash table from the csv
        file.
        """
        for address, zip_code in self.loader.get_address_zip_pairs():
            self.add(address, zip_code)

    def _add_adjacencies_from_data(self):
        """
        Initialization function that calls the loader to extract each weight/distance for each location to every other
        location.
        """
        for source_location, target_location, distance in self.loader.extract_source_target_weights():
            source_node = self.locations_table[source_location]
            target_node = self.locations_table[target_location]
            source_node.value.add_adjacent(target_node.value, distance)
            target_node.value.add_adjacent(source_node.value, distance)

    def _add_all_vertices_and_edges(self):
        """
        Initialization function that inputs the data obtained from the csv file via the loader into the graph,
        including all vertices and weighted edges, amounting to a weighted, undirected complete graph.
        """
        for loc_object in self.get_all_locations():
            self.graph.add_vertex(loc_object)
        for source_node in self.locations_table.get_all():
            for adjacency_info in source_node.value.adjacency_list:
                target_loc = adjacency_info[0]
                weight = adjacency_info[1]
                self.graph.add_weighted_edge(source_node.value, target_loc, weight)

    def add(self, address: str, zip_code: str):
        """
        Instantiates a new Location object with the provided address and zip code and adds it to the locations table.
        :param address: The address of the location.
        :param zip_code: The zip code of the location.
        """
        new_loc = Location(address.strip(), zip_code)
        self.locations_table[new_loc.get_key()] = new_loc

    def get_location(self, address):
        """
        Returns the Location object with the address provided, otherwise None.
        :param address: The address of the desired Location object.
        :return: The Location object with the provided address.
        :raises AttributeError:  If the stripped address is not an exact match, it will take the first 5 characters of
        the address passed as a parameter and, if those match with a Location object's address, will return that
        Location.  If user anticipates any two locations having the same initial 5 characters, this value should be
        adjusted, or this portion of the logic should be removed altogether, which would require an exact match.
        """
        try:
            return self.locations_table[address.strip()].value
        except AttributeError:
            for location in self.get_all_locations():
                full_address = location.get_key()
                if address.startswith(full_address[:5]):
                    return location
            return None

    def get_all_locations(self):
        """
        Returns each Location object from the locations table as a list.
        :return: Each location object as a list.
        """
        return [loc_node.value for loc_node in self.locations_table.get_all()]

    def get_graph(self):
        """
        Returns the Locations graph.
        :return: The Locations graph.
        """
        return self.graph
