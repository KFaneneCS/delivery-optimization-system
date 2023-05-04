from .package import Package
from data_structures.priority_queue import MaxPriorityQueue
from data.packages_loader import PackagesLoader


class Packages:
    def __init__(self, package_csv):
        self.packages = []
        self.loader = PackagesLoader(package_csv)

    def add_package(self, package):
        self.packages.append(package)


