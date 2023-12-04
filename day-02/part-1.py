def sum_possible_games():
    """
    Loop over input, eliminate any games that are not possible, i.e., any
    where there are more than 12 red dice, 13 green dice, or 14 blue dice

    Add up the valid game numbers and return the sum.

    Input like:
    Game 1: 3 blue, 4 red; 1 red, 2 green, 6 blue; 2 green
    Game 2: 1 blue, 2 green; 3 green, 4 blue, 1 red; 1 green, 1 blue
    Game 3: 8 green, 6 blue, 20 red; 5 blue, 4 red, 13 green; 5 green, 1 red
    Game 4: 1 green, 3 red, 6 blue; 3 green, 6 red; 3 green, 15 blue, 14 red
    Game 5: 6 red, 1 blue, 3 green; 2 blue, 1 red, 2 green

    This data would return 8: Games 1, 2, and 5 are valid games.
    """

    with open('input.txt', 'r', encoding="utf-8") as f:
        lines = f.readlines()

        game_total = 0

        for line in lines:
            if line.strip() != "":
                game_data = line.split()
                # loop starting at index 2, only landing on even indexes (ints)
                for i in range(2, len(game_data), 2):
                    die_color = game_data[i + 1]
                    die_count = int(game_data[i])
                    if die_count > 15:
                        break
                    # using startswith because die_color can end with
                    # ";" or "," or nothing at all
                    elif die_count > 12 and die_color.startswith("red"):
                        break
                    elif die_count > 13 and die_color.startswith("green"):
                        break
                    elif die_count > 14 and die_color.startswith("blue"):
                        break
                    elif i == len(game_data) - 2:
                        print(game_data)
                        # we've made it to the last dice and all are valid
                        # grab game number, slice of trailing ":", add to total
                        game_total += int(game_data[1][:-1])

    return game_total


print(sum_possible_games())
