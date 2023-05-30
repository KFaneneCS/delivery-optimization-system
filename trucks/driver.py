class Driver:
    """
    A simple class representing a truck driver.
    """
    def __init__(self, id_: int):
        self._id = id_

    def __str__(self):
        return f'Driver(ID={self.id})'

    @property
    def id(self):
        return self._id
