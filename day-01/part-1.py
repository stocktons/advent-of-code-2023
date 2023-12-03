def get_first_number(line):
    """
    Takes in a line of input, finds first number if it exists and returns it.
    """

    for char in line:
        if char.isdigit():
            return char


def get_last_number(line):
    """
    Takes in a line of input, finds last number if it exists and returns it.
    """

    for char in reversed(line):
        if char.isdigit():
            return char


def build_number_string(first, last):
    """
    Concatenates a string of the two number strings, then converts it to an
    integer, like "4" and "2" --> 42
    """

    return int(first + last)


def sum_calibration_values():
    """
    Reads lines from calibration list, returns total of two-digit numbers
    hidden in each line.

    1abc2 --> 12
    pqr3stu8vwx --> 38
    a1b2c3d4e5f --> 15
    treb7uchet -- 77

    12 + 38 + 15 + 77 = 142
    """

    calibration_sum = 0

    # read the numbers from the data file
    with open('input.txt', 'r', encoding="utf-8") as f:
        lines = f.readlines()

        for line in lines:
            print(line)
            if line.strip() != "":
                num_string = build_number_string(
                    get_first_number(line),
                    get_last_number(line)
                )
                calibration_sum += int(num_string)

    return calibration_sum


print(sum_calibration_values())
