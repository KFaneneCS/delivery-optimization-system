import csv


class Loader:
    def __init__(self, csv_file):
        self.csv_file = csv_file
        self.data = self.load_csv_data()
        self.full_addresses = self.extract_full_addresses()

    def load_csv_data(self):
        if self.csv_file.lower().endswith('.csv'):
            with open(self.csv_file, 'r') as file:
                reader = csv.reader(file)
                return [row for row in reader]
        else:
            raise ValueError('Extension must be .csv')

    def extract_full_addresses(self):
        # First element is an empty space to represent first empty cell of the data
        full_addresses = ['']
        # Getting the first column of the data which contains each address without the name of the location
        first_col = list(map(list, zip(*self.data)))[0]
        for col_address in first_col:
            full_addresses.append(col_address)
        return full_addresses[2:]

    def extract_address_zip_pairs(self):
        for full in self.full_addresses:
            address = full.split('(')[0].strip()
            zip_code = full.split('(')[1][:5]
            yield address, zip_code

    def extract_source_target_weights(self):
        # Adding the addresses from the first column to the first row of our data
        self.data.insert(0, self.full_addresses)

        for row in range(1, len(self.data)):
            source_address = self.data[row][0].split('(')[0].strip()
            for col in range(1, len(self.data[0])):
                target_address = self.data[0][col].split('(')[0].strip()
                weight = float(self.data[row][col])
                # Once we hit "0.0," we are doubly referencing an address, so we move on to the next row
                if weight == 0.0:
                    break
                yield source_address, target_address, weight
