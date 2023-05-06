import bisect


class Location:
    def __init__(self, address=None, zip_code=None):
        self.address = address
        self.zip_code = zip_code
        self.adjacency_list = []

    def __repr__(self):
        return f'Location(address={self.address} | zip={self.zip_code})'

    def get_key(self):
        return f'{self.address}'

    def add_adjacent(self, target, weight):
        bisect.insort(self.adjacency_list, (target, weight), key=lambda adj: adj[1])
        return self

    def get_adjacency_list(self):
        return self.adjacency_list
