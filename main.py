# Kyle Fanene - 006246401

from logistics_manager.logistics_manager import LogisticsManager
from user_interface.ui import UI

if __name__ == '__main__':
    locations_file = 'data/distance_table.csv'
    packages_file = 'data/package_file.csv'

    logistics_manager = LogisticsManager(locations_file, packages_file)
    logistics_manager.load_packages()
    logistics_manager.deliver_packages()
    packages = logistics_manager.get_packages()
    trucks = logistics_manager.get_trucks()

    ui = UI(packages, trucks)
    ui.execute()
