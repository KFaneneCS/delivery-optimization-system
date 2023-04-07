class Location:
    def __init__(self, address, zip_code):
        self.address = address
        self.zip_code = zip_code
        self.adjacency_list = []

    def __str__(self):
        return f'Location(address={self.address} | zip={self.zip_code})'

    def get_address(self):
        return self.address

    def add_adjacent(self, x, y):
        self.adjacency_list.append((x, y))
        # TODO:  cite "https://stackoverflow.com/questions/10695139/sort-a-list-of-tuples-by-2nd-item-integer-value"
        self.adjacency_list.sort(key=lambda t: t[1])
        return self

    def get_adjacency_list(self):
        return self.adjacency_list
