class Driver:
    def __init__(self, id_):
        self.id_ = id_

    def get_id(self):
        return self.id_


class Truck:
    def __init__(self, id_, driver):
        self.id_ = id_
        self.driver = driver
        self.packages = []
        self.MAX_CAPACITY = 16
        self.SPEED = 18
