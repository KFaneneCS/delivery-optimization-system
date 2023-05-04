import csv


class LocationsLoader:
    def __init__(self, csv_file):
        self.csv_file = csv_file
        self.data = self.load_csv_data()
        self.full_addresses = self.extract_full_addresses()
        self.address_zip_pairs = self.extract_address_zip_pairs()

    def load_csv_data(self):
        if self.csv_file.lower().endswith('.csv'):
            with open(self.csv_file, 'r') as file:
                reader = csv.reader(file)
                return [row for row in reader]
        else:
            raise ValueError('Extension must be .csv')

    def extract_full_addresses(self):
        # FIXME:  Redo this comment to reflect changes
        # First element is an empty space to represent first empty cell of the data
        full_addresses = ['HUB\n(84107)']
        # Getting the first column of the data which contains each address without the name of the location
        first_col = list(map(list, zip(*self.data)))[0]
        for col_address in first_col[1:]:
            full_addresses.append(col_address)
        return full_addresses

    def extract_address_zip_pairs(self):
        # self.full_addresses.insert(0, ('HUB', '84107'))
        pairs = []
        for full in self.full_addresses:
            address = full.split('(')[0].strip()
            zip_code = full.split('(')[1][:5]
            pairs.append((address, zip_code))
        return pairs

    def extract_source_target_weights(self):
        for source_index, tuple_val in enumerate(self.address_zip_pairs):
            source_address = tuple_val[0]
            for target_index in range(len(self.data)):
                target_address = self.address_zip_pairs[target_index][0]
                weight = float(self.data[source_index][target_index + 1])
                if weight == 0.0:
                    break
                yield source_address, target_address, weight

    def get_address_zip_pairs(self):
        return self.address_zip_pairs
