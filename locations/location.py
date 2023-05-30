import bisect


class Location:
    """
    A class representing a location consisting of an address, node, and list of adjacent locations and their
    known distances.
    """

    def __init__(self, address: str = None, zip_code: str = None):
        """
        Initializes a new instance of the Location class.
        :param address: The street address of the location.
        :param zip_code: The zip code of the location.
        """
        self._address = address
        self._zip_code = zip_code
        self._adjacency_list = []

    def __repr__(self):
        """
        Returns the string representation of the Location object.
        :return: The string representation of the Location object.
        """
        return f'Location(address={self._address} | zip={self._zip_code})'

    @property
    def address(self):
        """
        Returns the address associated with the Location.
        :return: The address associated with the Location.
        """
        return self._address

    @property
    def zip_code(self):
        """
        Returns the zip code associated with the Location.
        :return: The zip code associated with the Location.
        """
        return self._zip_code

    @property
    def adjacency_list(self):
        """
        Returns the list of adjacent locations and their known distances.
        :return: The list of adjacent locations and their known distances as tuples.
        """
        return self._adjacency_list

    def get_key(self):
        """
        Returns the string address of the Location, which can be used as a key in a hash function.
        :return: The string address of the Location.
        """
        return f'{self._address}'

    def add_adjacent(self, target, weight):
        """
        Adds another target Location and its weight/distance to this Location's adjacency list.  The new information
        is inserted such that the adjacency list remains sorted.
        :param target: The target Location object.
        :param weight: The target Location's weight/distance from current Location.
        """
        bisect.insort(self._adjacency_list, (target, weight), key=lambda adj: adj[1])
