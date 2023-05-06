from data_structures.priority_queue import MaxPriorityQueue
from packages.package import Package
import datetime

# The maximum value attributed to the difference between 5pm closing and the delivery deadline, where each 30 minute
# increment receives a unit value of 1.0, up to 9am (1 hour after opening and the earliest delivery time)
MAX_TIME_VALUE = 16.0
# A value representing the relative importance of distance versus delivery deadline (50% for both)
RELATIVE_WEIGHT = 0.5


def get_package_weight(distance, deadline: datetime.time, max_distance_value):
    if distance < 0 or not isinstance(distance, (int, float)):
        raise ValueError('Invalid distance value provided.')
    # The number of miles between the HUB and its farthest delivery location per Dijkstra
    if max_distance_value < 0 or not isinstance(max_distance_value, (int, float)):
        raise ValueError('Invalid max distance value provided.')
    if not isinstance(deadline, (str, datetime.time)):
        raise ValueError('Invalid deadline value provided.')

    # Close of business is at 5pm
    closing = datetime.time(17, 0)
    if deadline == 'EOD':
        deadline_value = 0
    else:
        # Each 30 min. increment before 5pm adds a weight unit of 1
        d1 = datetime.datetime(2020, 1, 1, deadline.hour, deadline.minute)
        d2 = datetime.datetime(2020, 1, 1, closing.hour, closing.minute)
        diff = d2 - d1
        deadline_value = diff / datetime.timedelta(minutes=30)

    package_weight = ((1 - (distance / max_distance_value)) * RELATIVE_WEIGHT) \
        + (1 - (deadline_value / MAX_TIME_VALUE) * RELATIVE_WEIGHT)
    return package_weight


def prioritize_packages(packages):
    return
