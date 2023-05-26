# Kyle Fanene - 006246401

from logistics_manager.logistics_manager import LogisticsManager

if __name__ == '__main__':
    locations_file = 'data/distance_table.csv'
    packages_file = 'data/package_file.csv'

    logistics_manager = LogisticsManager(locations_file, packages_file)
    logistics_manager.load_packages()
    logistics_manager.deliver_packages()
