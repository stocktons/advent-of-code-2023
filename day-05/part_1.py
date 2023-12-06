from pathlib import Path


def organize_maps(almanac_data):
    """
    Read almanac, sort each list of dictionaries by source numbers.

    Return sorted almanac.

    {
        'soil_to_fertilizer': [
            {'destination': '39', 'source': '0', 'range': '15'},
            {'destination': '0', 'source': '15', 'range': '37'},
            {'destination': '37', 'source': '52', 'range': '2'}
        ],
        'fertilizer_to_water': [
            {'destination': '42', 'source': '0', 'range': '7'},
            {'destination': '0', 'source': '11', 'range': '42'},
            {'destination': '49', 'source': '53', 'range': '8'},
            {'destination': '57', 'source': '7', 'range': '4'}
        ],
        'water_to_light': [
            {'destination': '88', 'source': '18', 'range': '7'},
            {'destination': '18', 'source': '25', 'range': '70'}
        ],
        'humidity_to_location': [
            {'destination': '60', 'source': '56', 'range': '37'},
            {'destination': '56', 'source': '93', 'range': '4'}
        ],
        'seed_to_soil': [
            {'destination': '52', 'source': '50', 'range': '48'},
            {'destination': '50', 'source': '98', 'range': '2'}
        ],
        'temperature_to_humidity': [
            {'destination': '1', 'source': '0', 'range': '69'},
            {'destination': '0', 'source': '69', 'range': '1'}
        ],
        'light_to_temperature': [
            {'destination': '81', 'source': '45', 'range': '19'},
            {'destination': '68', 'source': '64', 'range': '13'},
            {'destination': '45', 'source': '77', 'range': '23'}
        ]
    }
    """

    sorted_almanac = {}

    almanac, map_names = almanac_data
    for map_name in map_names:
        data = almanac[map_name]
        sorted_maps = sorted(data, key=lambda d: d["source"])
        sorted_almanac[map_name] = sorted_maps

    return sorted_almanac


def convert_source_to_destination(source_number, conversion_map):
    """
    if the number is less than the first middle number:
    it's self-referential.
    if it's greater than or equal to, check the last number
    and see if the seed number falls in that range. If yes,
    look to the left and calculate the difference and add that
    to the seed number
    (if it's not, look ahead to the next middle number. If it's
    between the last number of the previous range and the middle number,
    it's self-referential.) <-- don't need this because if we don't match, just
    catch it with the next less than!
    ... continue
    if we hit the end without matching the number, it's self-referential

    Takes in a source number and a conversion map for that source. Finds the
    next number and returns it.

    Conversion map is like:

    'seed_to_soil':
    [
        {'destination': '52', 'source': '50', 'range': '48'},
        {'destination': '50', 'source': '98', 'range': '2'}
    ],

    >>> convert_source_to_destination(98, [{'destination': '52', 'source': '50', 'range': '48'}, {'destination': '50', 'source': '98', 'range': '2'}])
    50
    >>> convert_source_to_destination(14, [{'destination': '52', 'source': '50', 'range': '48'}, {'destination': '50', 'source': '98', 'range': '2'}])
    14
    >>> convert_source_to_destination(55, [{'destination': '52', 'source': '50', 'range': '48'}, {'destination': '50', 'source': '98', 'range': '2'}])
    57
    >>> convert_source_to_destination(100, [{'destination': '52', 'source': '50', 'range': '48'}, {'destination': '50', 'source': '98', 'range': '2'}])
    100
    """

    for data in conversion_map:
        src = data["source"]
        rng = data["range"]
        dst = data["destination"]
        if source_number < src:
            return source_number
        elif source_number >= src:
            upper_limit = src + rng
            if source_number < upper_limit:
                diff = dst - src
                return source_number + diff

    return source_number


def seed_to_location(seeds, almanac):
    """
    Takes in a list of seed numbers, and the almanac. Controls the process
    of converting from seed -> soil -> fertilizer -> water -> light ->
    temperature -> humidity -> location
    """

    locations = []

    for seed in seeds:
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


def get_seeds():
    """
    Read seed numbers from file, convert to ints, store in a list. Return list.
    """

    with open('./data/seeds.txt', 'r', encoding="utf-8") as f:
        lines = f.readlines()

        for line in lines:
            if line.strip() != "":
                data = line.strip().split()

    return [int(d) for d in data]


def create_almanac():
    almanac = {}
    map_names = []

    map_files = Path("./data").iterdir()

    for file in map_files:
        if file.name != "seeds.txt":
            # trim .txt off of the file name
            map_name = file.name[:-4]
            almanac[map_name] = []

            with open(file, 'r', encoding="utf-8") as f:
                lines = f.readlines()

                for line in lines:
                    if line.strip() != "":
                        data = line.strip().split()
                        destination, source, range_ = data
                        almanac[map_name].append({
                            "destination": int(destination),
                            "source": int(source),
                            "range": int(range_)
                        })
                        map_names.append(map_name)

    return almanac, map_names


def find_nearest_location():
    """
    Finds the lowest corresponding location from the seed data provided.
    """

    seeds = get_seeds()
    almanac_data = create_almanac()
    sorted_almanac = organize_maps(almanac_data)
    locations = seed_to_location(seeds, sorted_almanac)

    return min(locations)


print(find_nearest_location())
