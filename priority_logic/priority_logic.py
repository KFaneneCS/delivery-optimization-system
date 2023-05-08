from data_structures.priority_queue import MaxPriorityQueue
from packages.package import Package
import datetime as dt

# Weighting coefficient
RELATIVE_WEIGHT = 0.25


def get_package_weight(distance: float, deadline: dt.time, max_distance_value: float, opening: dt.time = dt.time(8, 0),
                       closing: dt.time = dt.time(17, 0)):
    assert isinstance(distance, (int, float)) and distance >= 0, 'Invalid distance value provided.'
    assert isinstance(max_distance_value, (int, float)) and max_distance_value >= 0, 'Invalid max distance value ' \
                                                                                     'provided. '
    assert isinstance(opening, dt.time) and isinstance(closing, dt.time), 'Invalid opening and/or closing time ' \
                                                                          'provided. '

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
    time_weight = 1 - ((max_time_value - deadline_value) / max_time_value)
    package_weight = (dist_weight * RELATIVE_WEIGHT) + (time_weight * (1 - RELATIVE_WEIGHT))

    return package_weight


def prioritize_packages(packages):
    return
