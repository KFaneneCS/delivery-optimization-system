from data_structures.priority_queue import MaxPriorityQueue
from packages.package import Package
from typing import List
import datetime as dt

# Weighting coefficient
RELATIVE_WEIGHT = 0.75


def get_package_weight(distance: float, deadline: dt.time, max_distance_value: float, opening: dt.time = dt.time(8, 0),
                       closing: dt.time = dt.time(17, 0)):
    if not isinstance(distance, (int, float)) or distance < 0:
        raise ValueError('Invalid "distance" value.')
    if not isinstance(max_distance_value, (int, float)) or max_distance_value < 0:
        raise ValueError('Invalid "max distance value".')
    if not isinstance(opening, dt.time) or not isinstance(closing, dt.time):
        raise ValueError('Invalid "opening" and/or "closing" time value.')

    # Number of half-hour increments between opening and closing
    time_diff = ((closing.hour - opening.hour) * 60 + (closing.minute - opening.minute)) / 30
    # Removing 2 half-hour increments to account for earliest delivery time of 1 hour after opening
    max_time_value = time_diff - 2.0

    if deadline is None:
        deadline_value = 0
    else:
        # TODO:  Cite: https://stackoverflow.com/questions/8474670/pythonic-way-to-combine-datetime-date-and-datetime-time-objects
        diff = dt.datetime.combine(dt.date.today(), closing) - dt.datetime.combine(dt.date.today(), deadline)
        deadline_value = diff / dt.timedelta(minutes=30)

    dist_weight = 1 - (distance / max_distance_value)
    time_weight = deadline_value / max_time_value
    package_weight = round((dist_weight * RELATIVE_WEIGHT) + (time_weight * (1 - RELATIVE_WEIGHT)), 3)

    return package_weight


def prioritize_packages(packages: List[Package]):
    queue = MaxPriorityQueue()
    for package in packages:
        if package.wrong_address:
            package.priority = 0
        queue.insert(priority=package.priority, information=package)
    return queue
