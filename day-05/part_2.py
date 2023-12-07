from part_1 import (
    get_seeds,
    create_almanac,
    organize_maps,
    convert_source_to_destination,
)


def create_seed_table(seed_data):
    """
    seed_data is a list of integers like:
    [79, 14, 55, 13]

    Even indexes are the start of the seed number's range, and odd indexes
    are the length of the range.

    The first range starts with seed number 79 and contains 14 values: 79, 80,
    ..., 91, 92. The second range starts with seed number 55 and contains 13
    values: 55, 56, ..., 66, 67.

    Returns a list of tuples with start/end values of the seed's number range.

    >>> create_seed_table([79, 14, 55, 13])
    [(79, 92), (55, 67)]
    """

    seed_ranges = []

    for i in range(0, len(seed_data), 2):
        start = seed_data[i]
        end = start + seed_data[i + 1] - 1
        seed_ranges.append((start, end))

    return seed_ranges


def seeds_to_location(seed_ranges, almanac):
    """
    Takes in a list of seed ranges, and the almanac. Controls the process
    of converting from seed -> soil -> fertilizer -> water -> light ->
    temperature -> humidity -> location
    """

    locations = []

    for seed_range in seed_ranges:
        start, stop = seed_range
        for seed in range(start, stop + 1):
            soil = convert_source_to_destination(
                seed, almanac["seed_to_soil"])
            fertilizer = convert_source_to_destination(
                soil, almanac["soil_to_fertilizer"])
            water = convert_source_to_destination(
                fertilizer, almanac["fertilizer_to_water"])
            light = convert_source_to_destination(
                water, almanac["water_to_light"])
            temperature = convert_source_to_destination(
                light, almanac["light_to_temperature"])
            humidity = convert_source_to_destination(
                temperature, almanac["temperature_to_humidity"])
            location = convert_source_to_destination(
                humidity, almanac["humidity_to_location"])
            locations.append(location)

    return locations


def find_nearest_location():
    """
    Finds the lowest corresponding location from the seed data provided.
    """

    seeds = get_seeds()
    seed_ranges = create_seed_table(seeds)
    almanac_data = create_almanac()
    sorted_almanac = organize_maps(almanac_data)
    locations = seeds_to_location(seed_ranges, sorted_almanac)

    return min(locations)


print(find_nearest_location())
