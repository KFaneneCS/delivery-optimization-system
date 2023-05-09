import bisect


class Location:
    def __init__(self, address=None, zip_code=None):
        self._address = address
        self._zip_code = zip_code
        self._adjacency_list = []

    def __repr__(self):
        return f'Location(address={self._address} | zip={self._zip_code})'

    @property
    def address(self):
        return self._address

    @property
    def zip_code(self):
        return self._zip_code

    @property
    def adjacency_list(self):
        return self._adjacency_list

    def get_key(self):
        return f'{self._address}'

    def add_adjacent(self, target, weight):
        bisect.insort(self._adjacency_list, (target, weight), key=lambda adj: adj[1])
        return self
