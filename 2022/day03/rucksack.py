#! python3
"""
from: https://adventofcode.com/2022/day/3
"""

import os

def get_priority(letter: str):
    # a-z are priority 1-26, A-Z are priority 27-52
    if letter.islower():
        # ASCII value of 'a' is 97
        return ord(letter) - 96
    else:
        # ASCII value of 'A' is 65
        return ord(letter) - 38

def split_rucksack(input: str):
    """Given the string representation of the rucksack, return two sets of its contents"""
    return (set(input[:len(input)//2]), set(input[len(input)//2:]))

def main(filename):
    """Solve the problem!"""
    script_dir = os.path.dirname(__file__)
    file_path = os.path.join(script_dir, filename)
    priority_sum = 0
    with open(file_path) as input_file:
        for line in input_file:
            one, two = split_rucksack(line)
            # set intersection
            common = (one & two).pop()
            priority_sum += get_priority(common)
    print(priority_sum)

if __name__ == "__main__":
    main('example.txt')
    main('input.txt')
