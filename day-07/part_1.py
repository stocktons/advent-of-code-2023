"""
Takes in raw hands, and scores them using group_cards and find_hand_type.
score_and_sort_hands gathers the hands by score into a dictionary.


"""

CARDS_TO_STRENGTHS = {
    "A": 14,
    "K": 13,
    "Q": 12,
    "J": 11,
    "T": 10,
    "9": 9,
    "8": 8,
    "7": 7,
    "6": 6,
    "5": 5,
    "4": 4,
    "3": 3,
    "2": 2,
}

def read_file_and_parse_data():
    """
    Reads a text file with data like:
    32T3K 765
    T55J5 684
    KK677 28
    KTJJT 220
    QQQJA 483

    and creates a dictionary from the data like:

    {
    "32T3K": 765,
    "T55J5": 684,
    "KK677": 28,
    "KTJJT": 220,
    "QQQJA": 483,
    }
    """

    cards_and_bids = {}
    # read the numbers from the data file
    with open('input.txt', 'r', encoding="utf-8") as f:
        lines = f.readlines()

        print("num lines", len(lines))
        for line in lines:
            if line.strip() != "":
                card, bid = line.strip().split()
                cards_and_bids[card] = int(bid)

    print("num cards and bids", len(cards_and_bids))
    # print(cards_and_bids)
    return cards_and_bids

# read_file_and_parse_data()


def group_cards(hands):
    """Takes in a list of hands of cards and creates freq counters out
     of each of them by value.

    ["32T3K", "T55J5", "KK677", "KTJJT", "QQQJA"] becomes:

    {
        '32T3K': {'3': 2, '2': 1, 'T': 1, 'K': 1},
        'T55J5': {'T': 1, '5': 3, 'J': 1},
        'KK677': {'K': 2, '6': 1, '7': 2},
        'KTJJT': {'K': 1, 'T': 2, 'J': 2},
        'QQQJA': {'Q': 3, 'J': 1, 'A': 1}
    }

    IDEA: if you have trouble later, hands may not be unique
    """

    grouped_hands = {}

    for hand in hands:
        # make a freq counter for each hand
        counts = {}

        for card in hand:
            if not counts.get(card):
                counts[card] = 1
            else:
                counts[card] += 1

        grouped_hands[hand] = counts

    print("num_grouped_hands", len(grouped_hands))
    return grouped_hands


def find_hand_type(hand_counts: dict):
    """Assign value to hand.

    >>> find_hand_type({"3": 5})
    5
    >>> find_hand_type({"3": 4, "2": 1})
    4
    >>> find_hand_type({"T": 2, "5": 3})
    3
    >>> find_hand_type({"T": 1, "5": 3, "J": 1})
    3
    >>> find_hand_type({"T": 2, "J": 2, "K": 1})
    2
    >>> find_hand_type({"3": 2, "2": 1, "T": 1, "K": 1})
    1
    >>> find_hand_type({"3": 1, "2": 1, "T": 1, "J": 1, "K": 1})
    0
    """

    rough_hand_type = len(hand_counts)

    if rough_hand_type == 1:
        # five of a kind: xxxxx
        return 5

    if rough_hand_type == 2:
        # four of a kind: xxxxy
        if max(hand_counts.values()) == 4:
            return 4
        # three of a kind: xxxyy
        return 3

    if rough_hand_type == 3:
        # three of a kind: xxxyz
        if max(hand_counts.values()) == 3:
            return 3
        # two pairs: xxyyz
        return 2

    if rough_hand_type == 4:
        # one pair: wxyzz
        return 1

    if rough_hand_type == 5:
        # all unique: vwxyz
        return 0


def score_and_sort_hands(hands):
    """
    Scores hands and categorizes them by their scores.

    hands: ["32T3K", "T55J5", "KK677", "KTJJT", "QQQJA"]

    returns:
    {
        'type_0s': [],
        'type_1s': ['32T3K'],
        'type_2s': ['KK677', 'KTJJT'],
        'type_3s': ['T55J5', 'QQQJA'],
        'type_4s': [],
        'type_5s': []
    }
    """

    grouped_hands = group_cards(hands)

    categorized_hands = {
        "type_0s": [],
        "type_1s": [],
        "type_2s": [],
        "type_3s": [],
        "type_4s": [],
        "type_5s": [],
    }

    for hand in grouped_hands:
        hand_type = find_hand_type(grouped_hands[hand])
        categorized_hands[f"type_{hand_type}s"].append(hand)

    return categorized_hands


def sort_helper(hand1, hand2):
    """
    Looks at two hands and returns True if they are already in order from
    strongest to weakest.

    'KTJJT' 'KK677'
    """

    if hand1 == hand2:
        return True

    for i in range(0, len(hand1)):
        if CARDS_TO_STRENGTHS[hand1[i]] < CARDS_TO_STRENGTHS[hand2[i]]:
            return False
        if CARDS_TO_STRENGTHS[hand1[i]] > CARDS_TO_STRENGTHS[hand2[i]]:
            return True
        # if they are equal, keep looping

    return True


def card_bubblesort(elements):
    """
    Bubblesort, but with the power to compare and custom-sort card hands like
    'KK677' and 'KTJJT'.

    Credit for base bubblesort: GeeksForGeeks
    """

    swapped = False
    # Looping from size of array from last index[-1] to index [0]
    for n in range(len(elements)-1, 0, -1):
        for i in range(n):
            if not sort_helper(elements[i], elements[i + 1]):
                elements[i], elements[i + 1] = elements[i + 1], elements[i]
                swapped = True
        if not swapped:
            # exiting the function if we didn't make a single swap
            # meaning that the array is already sorted.
            return elements

    return elements


def sort_cards(categorized_hands):
    """Takes in categorized hands and sorts each list by strength low to high.

    {
        'type_0s': [],
        'type_1s': ['32T3K'],
        'type_2s': ['KK677', 'KTJJT'],
        'type_3s': ['QQQJA', 'T55J5'],
        'type_4s': [],
        'type_5s': []
    }

    becomes:
    {
        'type_0s': [],
        'type_1s': ['32T3K'],
        'type_2s': ['KTJJT', 'KK677'],
        'type_3s': ['T55J5', 'QQQJA'],
        'type_4s': [],
        'type_5s': []
    }
    """

    categorized_and_sorted_hands = {}

    for type in categorized_hands:
        categorized_and_sorted_hands[type] = (
            card_bubblesort(categorized_hands[type])
        )
        categorized_hands[type].reverse()

    return categorized_and_sorted_hands


def calculate_winnings():
    cards_and_bids = read_file_and_parse_data()
    cards = cards_and_bids.keys()
    categorized_hands = score_and_sort_hands(cards)
    sorted_hands = sort_cards(categorized_hands)

    all_cards = sum(sorted_hands.values(), [])

    total_winnings = 0

    for rank, card in enumerate(all_cards, start=1):
        total_winnings += cards_and_bids[card] * rank

    print(total_winnings)


calculate_winnings()