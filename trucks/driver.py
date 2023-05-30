class Driver:
    """
    A simple class representing a truck driver.
    """

    def __init__(self, id_: int):
        """
        Initializes a new instance of the Driver class.
        :param id_: The ID number of the driver.
        """
        self._id = id_

    def __str__(self):
        """
        Returns the string representation of the Driver object.
        :return: The string representation of the Driver object.
        """
        return f'Driver(ID={self.id})'

    @property
    def id(self):
        """
        Returns the ID of the driver.
        :return: The ID of the driver.
        """
        return self._id
