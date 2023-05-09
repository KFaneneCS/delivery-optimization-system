from locations.location import Location
from data_structures.hash import HashTable
import datetime


class Package:
    def __init__(self, id_: int, destination: Location, deadline: datetime, kilos: int, requirements: str):
        self.id_ = id_
        self.destination = destination
        self.deadline = deadline
        self.kilos = kilos
        self.requirements = requirements
        self.priority = None

    def __repr__(self):
        return f'Package(ID={self.id_} | destination={self.destination} | deadline={self.deadline} | ' \
               f'priority={self.priority})'

    def get_id(self):
        return self.id_

    def get_destination(self):
        return self.destination

    def get_deadline(self):
        return self.deadline

    def get_special_notes(self):
        return self.requirements

    def get_priority(self):
        return self.priority

    def set_priority(self, priority_value: float):
        self.priority = priority_value
        return self.priority
