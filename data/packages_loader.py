import csv

from data_structures.hash import HashTable


class PackagesLoader:
    """
    A class that handles packages data extraction from applicable csv file.
    """
    def __init__(self, csv_file: str):
        """
        Initializes a new instance of the PackagesLoader class.
        :param csv_file:  The location of the csv file.
        """
        self.csv_file = csv_file
        self.packages_table = HashTable(80)
        self.data = self.load_csv_data()

    def load_csv_data(self):
        """
        Loads and returns data from csv file.
        :return: Extracted data as list.
        :raises ValueError: If file extension is not ".csv".
        """
        if self.csv_file.lower().endswith('.csv'):
            with open(self.csv_file, 'r') as file:
                reader = csv.reader(file)
                return [row for row in reader]
        else:
            raise ValueError('Extension must be .csv')

    def get_data(self):
        """
        Returns extracted data.
        :return: Extracted data.
        """
        return self.data[1:]
