import csv
from data_structures.hash import HashTable


class PackagesLoader:
    def __init__(self, csv_file):
        self.csv_file = csv_file
        self.packages_table = HashTable(80)
        self.data = self.load_csv_data()

    def load_csv_data(self):
        if self.csv_file.lower().endswith('.csv'):
            with open(self.csv_file, 'r') as file:
                reader = csv.reader(file)
                return [row for row in reader]
        else:
            raise ValueError('Extension must be .csv')

    def get_data(self):
        return self.data[1:]
