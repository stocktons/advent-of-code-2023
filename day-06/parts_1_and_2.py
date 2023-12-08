import math


def calculate_distance(total_time, button_time):
    """
    >>> calculate_distance(7, 0)
    0
    >>> calculate_distance(7, 3)
    12
    """

    travel_time = total_time - button_time
    speed_multiplier = button_time

    race_distance = travel_time * speed_multiplier

    return race_distance


def find_lower_bound(record_dist, time):
    """
    Takes in a record distance and a time representing the length of the race.
    Finds the least number of milliseconds a button has to be pressed to
    beat the record.

    This approach with my puzzle input (vs. just a plain loop that checks every
    possible millisecond in order) reduces the number of operations
    from 38,947,970 to 25.
    """

    leftIdx = 0  # shortest button press
    rightIdx = time  # longest button press

    # for curiosity to see how many operations it takes to find the solution:
    # counter = 0

    while (leftIdx <= rightIdx):
        # counter += 1
        # find the middle value
        middleIdx = (leftIdx + rightIdx) // 2  # // is floor division operator
        distance = calculate_distance(time, middleIdx)

        if (distance < record_dist):
            # distance is too small, look at the right half
            leftIdx = middleIdx + 1
        elif (distance > record_dist):
            # distance is too large, look at the left half
            rightIdx = middleIdx - 1
        else:
            # we found our exact value, so grab next one up
            return middleIdx + 1  # , counter

    # didn't find an exact match, so figure out which
    if distance < record_dist:
        return middleIdx + 1  # , counter

    return middleIdx  # , counter


def find_num_winners(lower_bound, time):
    """
    Since the ways to win are distributed in a bell-curve shape, if we know the
    lower bound, we can calculate the upper bound and count up how many ways to
    win are between them.
    """
    upper_bound = time - lower_bound
    num_ways_to_win = upper_bound - lower_bound + 1

    return num_ways_to_win


def calc_margin_of_error(races):
    """
    Multiply all the ways to win together.
    """

    wins = []

    for race in races:
        record_dist, race_time = race
        lb, counter = find_lower_bound(record_dist, race_time)
        num_ways_to_win = find_num_winners(lb, race_time)
        wins.append(num_ways_to_win)

    return math.prod(wins)  # , counter


# print(calc_margin_of_error([(241, 38), (1549, 94), (1074, 79), (1091, 70)]))
print(calc_margin_of_error([(241154910741091, 38947970)]))
