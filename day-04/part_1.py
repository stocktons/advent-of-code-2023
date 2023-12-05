def make_cards():
    """
    Read text input, strip newlines, and make a dictionary of card names with
    a list of sets of the winning numbers and the elf's numbers as the keys.

    Card 1: 41 48 83 86 17 | 83 86  6 31 17  9 48 53
    Card 2: 13 32 20 16 61 | 61 30 68 82 17 32 24 19

    becomes:

    {
        'Card 1': [
            {'41', '48', '83', '86', '17'},
            {'83', '86', '6', '31', '17', '9', '48', '53'}
        ],
        'Card 2': [
            {'13', '32', '20', '16', '61'},
            {'61', '30', '68', '82', '17', '32', '24', '19'}
        ]
    }
    """

    cards = {}

    with open('input.txt', 'r', encoding="utf-8") as f:
        lines = f.readlines()

        for line in lines:
            if line.strip() != "":
                stripped = line.strip()
                colon = stripped.index(":")
                pipe = stripped.index("|")
                card_name = line[:colon]
                # remove extra whitespace like "Card   2" --> "Card 2"
                card_name_cleaned = ' '.join(card_name.split())
                winning_nums = set(line[colon + 2:pipe - 1].split())
                elf_nums = set(line[pipe + 2:].split())

                cards = cards | {card_name_cleaned: [winning_nums, elf_nums]}

    return cards


def score_card(card):
    """
    Finds matches between winning numbers and elf's numbers.
    Calculates and returns score.

    A card is a list of two sets. The first set is the winning numbers,
    the second set is the elf's numbers.
    """

    winning_nums, elf_nums = card

    num_matches = len(winning_nums & elf_nums)

    if num_matches:
        return 2 ** (num_matches - 1)

    return 0


def find_matches_and_calculate_points(cards):
    """
    Takes in a dictionary of scratch cards and determines how many of the
    elf's numbers match the winning numbers, and returns the total points.

    {
        'Card 1': [
            {'41', '48', '83', '86', '17'},
            {'83', '86', '6', '31', '17', '9', '48', '53'}
        ],
        'Card 2': [
            {'13', '32', '20', '16', '61'},
            {'61', '30', '68', '82', '17', '32', '24', '19'}
        ],
        'Card 3': [
            {'1', '21', '53', '59', '44'},
            {'69', '82', '63', '72', '16', '21', '14', '1'}
        ],
        'Card 4': [
            {'41', '92', '73', '84', '69'},
            {'59', '84', '76', '51', '58', '5', '54', '83'}
        ],
        'Card 5': [
            {'87', '83', '26', '28', '32'},
            {'88', '30', '70', '12', '93', '22', '82', '36'}
        ],
        'Card 6': [
            {'31', '18', '13', '56', '72'},
            {'74', '77', '10', '23', '35', '67', '36', '11'}
        ]
    }

    Card 1 has five winning numbers (41, 48, 83, 86, and 17) and eight numbers
    the elf has (83, 86, 6, 31, 17, 9, 48, and 53). Of the numbers the elf has,
    four of them (48, 83, 17, and 86) are winning numbers.

    Card 2 has two winning numbers (32 and 61), so it is worth 2 points.
    Card 3 has two winning numbers (1 and 21), so it is worth 2 points.
    Card 4 has one winning number (84), so it is worth 1 point.
    Card 5 has no winning numbers, so it is worth no points.
    Card 6 has no winning numbers, so it is worth no points.

    So, in this example, the Elf's pile of scratchcards is worth 13 points.
    """

    total_points = 0

    for card in cards:
        score = score_card(cards[card])
        total_points += score

    return total_points


def score_scratchcards():
    """Conductor function. See other docstrings for details."""

    cards = make_cards()
    score = find_matches_and_calculate_points(cards)

    return score


print(score_scratchcards())
