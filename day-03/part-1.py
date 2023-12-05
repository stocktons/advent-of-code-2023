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


def search_around_coords(grid, coords):
    """
    Takes in a grid and a grid coord and searches all eight points around it
    for a symbol that isn't a digit or a ".".

    Returns True if a symbol is found
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
                if grid[r][c].isdigit() or grid[r][c] == ".":
                    continue
                else:
                    return True
            except IndexError:
                continue


def determine_validity_and_tally(grid, coords: dict):
    """
    Determine if number is adjacent to a symbol. If so, concatenate and
    return a valid integer. Otherwise, return 0.
    """

    is_keeper = search_around_coords(grid, coords)

    if is_keeper:
        # concatenate values and add to sum
        valid_num = int(''.join(coords.values()))
        return valid_num

    return 0


def sum_engine_part_numbers(grid):
    """
    The engine schematic (the grid) consists of a visual representation of
    the engine. Any number adjacent to a symbol, even diagonally, is a
    "part number" and should be included in the sum. (Periods (.) do not
    count as a symbol.)

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

    In this schematic, two numbers are not part numbers because they are not
    adjacent to a symbol: 114 (top right) and 58 (middle right). Every other
    number is adjacent to a symbol and so is a part number; their sum is 4361.
    """

    total = 0

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
                    valid_num = determine_validity_and_tally(grid, num_coords)
                    total += valid_num

            else:
                if len(num_coords):
                    valid_num = determine_validity_and_tally(grid, num_coords)
                    total += valid_num
                # we aren't done with the row yet, but we're done with the
                # current number
                num_coords = {}
    return total


new_grid = make_grid()
print(sum_engine_part_numbers(new_grid))
