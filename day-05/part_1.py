from pathlib import Path


def organize_maps(almanac_data):
    """
    Read almanac, sort list of dictionaries by source numbers.
    [
        { "destination": 52, "source": 50, "range": 48 },
        { "destination": 50, "source": 98, "range": 2 },
    ]
    Return sorted almanac.
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
    if it's not, look ahead to the next middle number. If it's
    between the last number of the previous range and the middle number,
    it's self-referential.
    ... continue
    if we hit the end without matching the number, it's self-referential
    """
    ...


def seed_to_location(seeds, almanac):
    for seed in seeds:
        soil = convert_source_to_destination(seed, almanac["seed_to_soil"])


def create_almanac_and_find_locations():
    almanac = {}
    map_names = []

    map_files = Path("./sample_data").iterdir()

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
                            "destination": destination,
                            "source": source,
                            "range": range_
                        })
                        map_names.append(map_name)

    return almanac, map_names


almanac_data = create_almanac_and_find_locations()
organize_maps(almanac_data)
