from locations.location import Location
from data_structures.hash import HashTable
import datetime


class Package:
    def __init__(self, id_: int, destination: Location, deadline: datetime, kilos: int, notes: str):
        self._id = id_
        self._destination = destination
        self._deadline = deadline
        self._kilos = kilos
        self._notes = notes
        self._truck_id = None
        self._delayed = False
        self._priority = None

    def __str__(self):
        return f'Package(ID={self._id} | destination={self.destination} | deadline={self._deadline} | ' \
               f'priority={self._priority})'

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
    def delayed(self):
        return self._delayed

    @delayed.setter
    def delayed(self, is_delayed: bool):
        self._delayed = is_delayed


