def make_grid():
    """
    Read text input, strip newlines, and make a list of all characters
    separated by a comma. Add each line-as-a-list to the grid and return
    the resulting matrix.
    """

    grid = []

    with open('input.txt', 'r', encoding="utf-8") as f:
        lines = f.readlines()

        for line in lines:
            if line.strip() != "":
                stripped = line.strip()
                grid.append([*stripped])

    return grid


def search_around_coords_for_star(grid, coords):
    """
    Takes in a grid and a row of grid coords where a number is located and
    searches all eight points around each one for a star.

    Returns star coordinates if one is found, otherwise None.
    """

    for coord in coords:

        row, col = coord

        back = col - 1
        forward = col + 1
        above = row - 1
        below = row + 1

        all_points = {
            "left": (row, back),
            "left_top": (above, back),
            "top": (above, col),
            "right_top": (above, forward),
            "right": (row, forward),
            "right_bottom": (below, forward),
            "bottom": (below, col),
            "left_bottom": (below, back),
        }

        for point in all_points:
            r, c = all_points[point]
            try:
                if grid[r][c] == "*":
                    return r, c
            except IndexError:
                continue


def get_star_coords_and_number(grid, coords: dict):
    """
    Determine if number is adjacent to a symbol. If so, concatenate and
    return a valid integer. Otherwise, return None.
    """

    star_coords = search_around_coords_for_star(grid, coords)

    if star_coords:
        # concatenate values and add to sum
        valid_num = int(''.join(coords.values()))
        return star_coords, valid_num

    return None


def make_star_map(grid):
    """
    Creates a map of the locations of all of the stars (gears) in the engine.
    The values are all the numbers within touching distance of the gear.

    Here is an example engine schematic:

    467..114..
    ...*......
    ..35..633.
    ......#...
    617*......
    .....+.58.
    ..592.....
    ......755.
    ...$.*....
    .664.598..

    And the star map generated from this:

    {(1, 3): [467, 35], (4, 3): [617], (8, 5): [755, 598]}
    """

    star_map = {}

    for row, _ in enumerate(grid):
        num_coords = {}
        for col, col_item in enumerate(grid[row]):
            if col_item.isdigit():
                # build up num_coords like:
                # {(4, 2): '2', (4, 3): '2', (4, 4): '2'}
                num_coords = num_coords | {(row, col): col_item}

                # handle last thing in row being a number
                if col == len(grid[row]) - 1:
                    # print("last item", col, col_item)
                    if get_star_coords_and_number(grid, num_coords):
                        star_coords, valid_num = get_star_coords_and_number(
                            grid, num_coords)
                        if star_map.get(star_coords):
                            star_map[star_coords].append(valid_num)
                        else:
                            star_map[star_coords] = [valid_num]
            else:
                if len(num_coords):
                    if get_star_coords_and_number(grid, num_coords):
                        star_coords, valid_num = get_star_coords_and_number(
                            grid, num_coords)
                        if star_map.get(star_coords):
                            star_map[star_coords].append(valid_num)
                        else:
                            star_map[star_coords] = [valid_num]

                # we aren't done with the row yet, but we're done with the
                # current number
                num_coords = {}

    return star_map


def process_star_map_and_calc_ratios(star_map):
    """
    Takes in a dictionary of star coordinates with a list the numbers that are
    nearby it, like:

    {(1, 3): [467, 35], (4, 3): [617], (8, 5): [755, 598]}

    Goes through the dictionary and finds all values that are lists of
    length 2 and multiplies those values together.

    Returns the sum of all of these multiplied values.
    """

    gear_ratios = [
        star_map[star][0] * star_map[star][1]
        for star in star_map
        if len(star_map[star]) == 2
    ]

    replacement_gear_part_number = 0

    for ratio in gear_ratios:
        replacement_gear_part_number += ratio

    return replacement_gear_part_number


def calculate_replacement_part_gear_num():
    """
    The engine schematic (the grid) consists of a visual representation of
    the engine. A gear is any * symbol that is adjacent to exactly two part
    numbers. Its gear ratio is the result of multiplying those two
    numbers together.

    This time, you need to find the gear ratio of every gear and add them all
    up so that the engineer can figure out which gear needs to be replaced.

    Here is an example engine schematic:

    467..114..
    ...*......
    ..35..633.
    ......#...
    617*......
    .....+.58.
    ..592.....
    ......755.
    ...$.*....
    .664.598..

    This returns part number 467835.
    """

    new_grid = make_grid()
    star_map = make_star_map(new_grid)
    gear_part_number = process_star_map_and_calc_ratios(star_map)

    return gear_part_number


print(calculate_replacement_part_gear_num())
