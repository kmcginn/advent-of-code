#! python3
"""
from: https://adventofcode.com/2019/day/4

--- Part Two ---
An Elf just remembered one more important detail: the two adjacent matching digits are not part of
a larger group of matching digits.

Given this additional criterion, but still ignoring the range rule, the following are now true:

112233 meets these criteria because the digits never decrease and all repeated digits are exactly
two digits long.
123444 no longer meets the criteria (the repeated 44 is part of a larger group of 444).
111122 meets the criteria (even though 1 is repeated more than twice, it still contains a
double 22).
How many different passwords within the range given in your puzzle input meet all of the criteria?

"""

import os

def list_digits(password):
    """Takes a 6 digit int and returns a list of each digit in order"""
    factor = 100000
    digits = list()
    while factor > 1:
        digits.append(password // factor)
        password = password % factor
        factor //= 10
    digits.append(password)
    return digits

def is_valid(password):
    """Determines whether or not a given password is valid"""
    digits = list_digits(password)
    # initialize count of digits with digits[0] since it is not in the for loop
    number_counts = {digits[0]: 1}
    for i in range(1, len(digits)):
        # invalidate password if previous digit is greater than current digit
        if digits[i] < digits[i - 1]:
            return False
        # count the number of times a digit has appeared in the password
        if digits[i] in number_counts:
            number_counts[digits[i]] += 1
        else:
            number_counts[digits[i]] = 1
    # password is valid only if at least one digit appears exactly twice
    # since we invalidate passwords which are not strictly even or increasing,
    # a count of 2 indicates two identical digits next to each other
    return 2 in number_counts.values()

def main():
    """Solve the problem!"""
    script_dir = os.path.dirname(__file__)
    file_path = os.path.join(script_dir, './input.txt')
    with open(file_path) as input_file:
        password_range = input_file.readline().split("-")
    min_value = int(password_range[0])
    max_value = int(password_range[1])
    attempted_password = min_value
    total_valid = 0
    while attempted_password <= max_value:
        if is_valid(attempted_password):
            total_valid += 1
        attempted_password += 1
    print(total_valid)

if __name__ == "__main__":
    main()
