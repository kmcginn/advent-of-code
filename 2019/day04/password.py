#! python3
"""
from: https://adventofcode.com/2019/day/4

--- Day 4: Secure Container ---
You arrive at the Venus fuel depot only to discover it's protected by a password. The Elves had
written the password on a sticky note, but someone threw it out.

However, they do remember a few key facts about the password:

It is a six-digit number.
The value is within the range given in your puzzle input.
Two adjacent digits are the same (like 22 in 122345).
Going from left to right, the digits never decrease; they only ever increase or stay the same
(like 111123 or 135679).
Other than the range rule, the following are true:

111111 meets these criteria (double 11, never decreases).
223450 does not meet these criteria (decreasing pair of digits 50).
123789 does not meet these criteria (no double).
How many different passwords within the range given in your puzzle input meet these criteria?

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
    has_adjacent_matches = False
    for i in range(1, len(digits)):
        # invalidate password if previous digit is greater than current digit
        if digits[i] < digits[i - 1]:
            return False
        if digits[i] == digits[i-1]:
            has_adjacent_matches = True
    return has_adjacent_matches

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
