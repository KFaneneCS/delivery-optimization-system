from datetime import timedelta
from locations.location import Location


class Package:
    STATUSES = ['At Hub', 'Delayed', 'En Route', 'Delivered']

    def __init__(self, id_: int, destination: Location, deadline: timedelta, kilos: int, notes: str):
        self._id = id_
        self._destination = destination
        self._deadline = deadline
        self._kilos = kilos
        self._notes = notes
        self._space_already_allocated = False
        self._truck_id = None
        self._wrong_address = False
        self._priority = None
        self._status = None
        self._ready_time = timedelta(hours=0, minutes=0)
        self._status_at_times = []

    def __repr__(self):
        return f'Package(ID={self._id} | destination={self.destination} | deadline={self._deadline} | ' \
               f'priority={self._priority} | status={self._status} | truck={self._truck_id})'

    # TODO:  Cite:  https://stackoverflow.com/questions/2627002/whats-the-pythonic-way-to-use-getters-and-setters
    @property
    def id(self):
        return self._id

    @property
    def destination(self):
        return self._destination

    @destination.setter
    def destination(self, new_destination: Location):
        if not isinstance(new_destination, Location):
            raise ValueError('Invalid "destination" value.')
        self._destination = new_destination

    @property
    def deadline(self):
        return self._deadline

    @property
    def special_notes(self):
        return self._notes

    @property
    def space_already_allocated(self):
        return self._space_already_allocated

    @space_already_allocated.setter
    def space_already_allocated(self, space_allocated: bool):
        self._space_already_allocated = space_allocated

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

    @property
    def ready_time(self):
        return self._ready_time

    @ready_time.setter
    def ready_time(self, ready_time: timedelta):
        if not isinstance(ready_time, timedelta):
            raise ValueError('Invalid "ready time" value.')
        self._ready_time = ready_time

    @property
    def status_at_times(self):
        return self._status_at_times

    def set_status(self, new_status: STATUSES, curr_time: timedelta):
        if new_status not in self.STATUSES:
            raise ValueError(f'Invalid status: {new_status}.')
        self._status = new_status
        self._status_at_times.append((curr_time, new_status))
