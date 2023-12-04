# power of minimum cubes
# in each line make a frequency counter, king of the hill style
# at the end of each line, multiply red, green, and blue together
# add this to the running total
def strip_punctuation(color: str):
    """
    Strip trailing ';' or ',' from colors.

    >>> strip_punctuation("green;")
    'green'

    >>> strip_punctuation("red")
    'red'
    """

    if color.endswith(",") or color.endswith(";"):
        return color[:-1]

    return color


def find_highest_dice_in_game(game_data):
    """
    Loops over a single game and finds the greatest number of red, blue, and
    green dice respectively. Returns a dictionary with these values.

    >>> find_highest_dice_in_game(["Game", "1:", "3", "blue,", "4", "red;", "1", "red,", "2", "green,", "6", "blue;", "2", "green"]) # noqa: E501
    {'red': 4, 'blue': 6, 'green': 2}
    """

    highest_dice_in_game = {"red": 0, "blue": 0, "green": 0}

    # loop starting at index 2, only landing on even indexes (ints)
    for i in range(2, len(game_data), 2):
        die_color_raw = game_data[i + 1]
        die_color = strip_punctuation(die_color_raw)
        die_count = int(game_data[i])

        if die_count > highest_dice_in_game[die_color]:
            highest_dice_in_game[die_color] = die_count

    return highest_dice_in_game


def calculate_cube_power(highest_dice):
    """
    Takes in an object representing colored dice counts. Multiplies the
    counts and returns the result.

    >>> calculate_cube_power({"red": 4, "blue": 6, "green": 2})
    48
    """

    cubes_power = 1

    for dice in highest_dice:
        cubes_power *= highest_dice[dice]

    return cubes_power


def sum_powers_of_minimum_cubes():
    """
    In each game you played, what is the fewest number of cubes of each color
    that could have been in the bag to make the game possible? Find these
    numbers and multiply them together for each game--we'll call this the
    power. Return the sum of the powers for all the games.

    Input like:
    Game 1: 3 blue, 4 red; 1 red, 2 green, 6 blue; 2 green
    Game 2: 1 blue, 2 green; 3 green, 4 blue, 1 red; 1 green, 1 blue
    Game 3: 8 green, 6 blue, 20 red; 5 blue, 4 red, 13 green; 5 green, 1 red
    Game 4: 1 green, 3 red, 6 blue; 3 green, 6 red; 3 green, 15 blue, 14 red
    Game 5: 6 red, 1 blue, 3 green; 2 blue, 1 red, 2 green

    The power of the minimum set of cubes in game 1 is 48:
    6 blue * 2 green * 4 red.
    In games 2-5 it was 12, 1560, 630, and 36, respectively. Adding up these
    five powers produces the sum 2286.
    """

    with open('input.txt', 'r', encoding="utf-8") as f:
        lines = f.readlines()

        game_total = 0

        for line in lines:
            if line.strip() != "":
                game_data = line.split()
                highest_dice_in_game = find_highest_dice_in_game(game_data)
                cubes_power = calculate_cube_power(highest_dice_in_game)

                game_total += cubes_power

    return game_total


print(sum_powers_of_minimum_cubes())
