from .package import Package


class Packages:
    def __init__(self):
        self.packages = []

    def add_package(self, package):
        self.packages.append(package)
