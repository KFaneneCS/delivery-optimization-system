import datetime
from locations.location import Location


class Package:
    STATUSES = ['At Hub', 'Delayed', 'In Transit', 'Delivered']

    def __init__(self, id_: int, destination: Location, deadline: datetime, kilos: int, notes: str):
        self._id = id_
        self._destination = destination
        self._deadline = deadline
        self._kilos = kilos
        self._notes = notes
        self._truck_id = None
        self._wrong_address = False
        self._priority = None
        self._status = Package.STATUSES[0]

    def __str__(self):
        return f'Package(ID={self._id} | destination={self.destination} | deadline={self._deadline} |\n ' \
               f'        priority={self._priority} | status={self._status}) | truck={self._truck_id}'

    # TODO:  Cite:  https://stackoverflow.com/questions/2627002/whats-the-pythonic-way-to-use-getters-and-setters
    @property
    def id(self):
        return self._id

    @property
    def destination(self):
        return self._destination

    @property
    def deadline(self):
        return self._deadline

    @property
    def special_notes(self):
        return self._notes

    @property
    def priority(self):
        return self._priority

    @priority.setter
    def priority(self, priority_value: float):
        self._priority = priority_value

    @property
    def truck_id(self):
        return self._truck_id

    @truck_id.setter
    def truck_id(self, truck_id: int):
        if truck_id < 0:
            raise ValueError('Invalid truck ID value.')
        self._truck_id = truck_id

    @property
    def wrong_address(self):
        return self._wrong_address

    @wrong_address.setter
    def wrong_address(self, has_wrong_address: bool):
        self._wrong_address = has_wrong_address

    @classmethod
    def get_statuses(cls):
        return cls.STATUSES

    @property
    def status(self):
        return self._status

    @status.setter
    def status(self, new_status):
        if new_status not in self.STATUSES:
            raise ValueError(f'Invalid status: {new_status}.')
        self._status = new_status
