word_nums = [
    "zero",
    "one",
    "two",
    "three",
    "four",
    "five",
    "six",
    "seven",
    "eight",
    "nine"
]


def get_first_number_and_idx(line):
    """
    Takes in a line of input, finds first number if it exists and returns
    a dictionary with it and its index.

    >>> get_first_number_and_idx('seven5seven8one')
    {5: '5'}
    """

    for i, char in enumerate(line):
        if char.isdigit():
            return {i: char}


def get_last_number_and_idx(line):
    """
    Takes in a line of input, finds last number if it exists and returns
    a dictionary with it and its index.

    >>> get_last_number_and_idx('seven5seven8one')
    {11: '8'}
    >>> get_last_number_and_idx('2sevensevenone')
    {0: '2'}
    >>> get_last_number_and_idx('seven5seven8one4')
    {15: '4'}
    """

    for i, char in enumerate(reversed(line)):
        if char.isdigit():
            forward_i = len(line) - i - 1
            return {forward_i: char}


def find_number_strings(line):
    """
    Iterates through list of word_nums and if that word_num is found in the
    line, adds the index(es) and the word to a dictionary.
    Returns dictionary.

    >>> find_number_strings('seven5seven8one')
    {12: 'one', 0: 'seven', 6: 'seven'}
    """

    idxs_to_num_strings = {}

    for wn in word_nums:
        idxs_to_wn = {
            i: wn for i in range(len(line)) if line.startswith(wn, i)
        }

        # combine current dictionary into main dictionary
        idxs_to_num_strings = idxs_to_num_strings | idxs_to_wn

    return idxs_to_num_strings


def build_number_ref(first, last, words):
    """
    Takes in three dictionaries:
        - first: {2: "3"}
        - last: {7: "4"}
        - words: {3: "one", 8: "nine"}

    and combines them into one dictionary like:
    {
        2: "3",
        7: "4",
        3: "one",
        8: "nine"
    }

    >>> build_number_ref({2: "3"}, {7: "4"}, {3: "one", 8: "nine"})
    {2: '3', 7: '4', 3: 'one', 8: 'nine'}
    """

    return first | last | words


def find_first_and_last_numbers(number_ref):
    """
    Takes in a dictionary and returns the values associated with the highest
    and lowest keys.

    >>> find_first_and_last_numbers({7: '4', 2: '3', 3: 'one', 8: 'nine'})
    ('3', 'nine')
    """

    idxs = number_ref.keys()
    first = min(idxs)
    last = max(idxs)

    return number_ref[first], number_ref[last]


def convert_word_to_str_digit(word):
    """
    Takes in a string like 'one' or '1' and if it's a word,
    converts it to '1', otherwise preserves the value.

    >>> convert_word_to_str_digit('one')
    '1'
    >>> convert_word_to_str_digit('5')
    '5'
    """

    if len(word) == 1:
        return word

    return str(word_nums.index(word))


def build_number_string(first, last):
    """
    Takes in two numbers, which could be words like "four" or a string number
    like "2".
    Combine these two values into a single integer, like "four" and "2" --> 42

    >>> build_number_string("four", "2")
    42
    """

    f = convert_word_to_str_digit(first)
    l = convert_word_to_str_digit(last)
    
    return int(f + l)


def sum_calibration_values():
    """
    Reads lines from calibration list, finds first and last numbers
    hidden in each line (either a word or numeric), and totals them all.

    two1nine
    eightwothree
    abcone2threexyz
    xtwone3four
    4nineeightseven2
    zoneight234
    7pqrstsixteen

    In this example, the calibration values are 29, 83, 13, 24, 42, 14,
    and 76. Adding these together produces 281.
    """

    calibration_sum = 0

    # read the numbers from the data file
    with open('input.txt', 'r', encoding="utf-8") as f:
        lines = f.readlines()

        for line in lines:
            if line.strip() != "":
                idx_to_first = get_first_number_and_idx(line)
                idx_to_last = get_last_number_and_idx(line)
                idxs_to_num_strs = find_number_strings(line)
                num_ref = build_number_ref(
                    idx_to_first,
                    idx_to_last,
                    idxs_to_num_strs
                )
                first_num_wd, last_num_wd = find_first_and_last_numbers(num_ref)
                line_val = build_number_string(first_num_wd, last_num_wd)

                calibration_sum += line_val

    return calibration_sum


print(sum_calibration_values())
