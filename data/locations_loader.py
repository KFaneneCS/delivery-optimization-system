import csv
from typing import List


class LocationsLoader:
    """
    A class that handles location data extraction from applicable csv file.
    """

    def __init__(self, csv_file: str):
        """
        Initializes a new instance of the LocationsLoader class.
        :param csv_file: The location of the csv file.
        """
        self.csv_file = csv_file
        self.data = self.load_csv_data()
        self.full_addresses = self.extract_full_addresses()
        self.address_zip_pairs = self.extract_address_zip_pairs()

    def load_csv_data(self) -> List:
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

    def extract_full_addresses(self) -> List:
        """
        Extracts each location's full address from our loaded data.

        The initial "HUB" location is manually added for simplicity.
        :return: Full addresses as list.
        """
        full_addresses = ['HUB\n(84107)']
        first_col = list(map(list, zip(*self.data)))[0]
        for col_address in first_col[1:]:
            full_addresses.append(col_address)
        return full_addresses

    def extract_address_zip_pairs(self) -> List:
        """
        Extracts the address and zip code from each full address and stores them as tuples.
        :return: address: str, zip_code: str tuples as list.
        """
        pairs = []
        for full in self.full_addresses:
            address = full.split('(')[0].strip()
            zip_code = full.split('(')[1][:5]
            pairs.append((address, zip_code))
        return pairs

    def extract_source_target_weights(self):
        """
        Extracts each weight (distance) value from each location pairing.
        :return: Source address, target address, and their associated weight value as tuples.
        """
        for source_index, tuple_val in enumerate(self.address_zip_pairs):
            source_address = tuple_val[0]
            for target_index in range(len(self.data)):
                target_address = self.address_zip_pairs[target_index][0]
                weight = float(self.data[source_index][target_index + 1])
                if weight == 0.0:
                    break
                yield source_address, target_address, weight

    def get_address_zip_pairs(self) -> List:
        """
        Returns address-zip pairing list.
        :return: Address-zip pairing list.
        """
        return self.address_zip_pairs
