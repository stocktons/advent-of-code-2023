from part_1 import make_cards


def score_card(card):
    """
    Finds matches between winning numbers and elf's numbers.
    Calculates and returns number of matches.

    A card is a list of two sets. The first set is the winning numbers,
    the second set is the elf's numbers.
    """

    winning_nums, elf_nums = card

    num_matches = len(winning_nums & elf_nums)

    return num_matches


def create_hand(cards):
    """
    incoming cards look like:
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
    calculate all the cards' matches and store them in a dictionary like:
    {
        "Card 1": [4, 1],
        "Card 2": [2, 1],
        "Card 3": [2, 1],
        "Card 4": [1, 1],
        "Card 5": [0, 1],
        "Card 6": [0, 1],
    }
    """

    scored_cards = {}

    for card in cards:
        score = score_card(cards[card])
        scored_cards[card] = [score, 1]

    return scored_cards


def hand_out_cards(cards):
    """
    Takes in a set of scratchcards and performs the convoluted logic spelled
    out in today's puzzle prompt.

    {
        "Card 1": [4, 1],
        "Card 2": [2, 1],
        "Card 3": [2, 1],
        "Card 4": [1, 1],
        "Card 5": [0, 1],
        "Card 6": [0, 1],
    }

    transforms into:

    {
        "Card 1": [4, 1],
        "Card 2": [2, 2],
        "Card 3": [2, 4],
        "Card 4": [1, 8],
        "Card 5": [0, 14],
        "Card 6": [0, 1],
    }
    """

    updated_cards = cards

    for card_num, card in enumerate(cards, 1):
        matches, copies = cards[card]

        for i in range(1, matches + 1):
            target_card_num = card_num + i
            updated_cards[f'Card {target_card_num}'][1] = (
                cards[f'Card {target_card_num}'][1] + copies
            )

    return updated_cards


def count_cards(cards: dict):
    """Count the total number of cards."""

    total_cards = sum(value[-1] for value in cards.values())

    return total_cards


def find_total_cards():
    """Conductor function."""

    cards = make_cards()
    scored_cards = create_hand(cards)
    all_cards = hand_out_cards(scored_cards)
    total = count_cards(all_cards)

    return total


print(find_total_cards())
