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

def main(filename):
    """Solve the problem!"""
    script_dir = os.path.dirname(__file__)
    file_path = os.path.join(script_dir, filename)
    priority_sum = 0
    elf_group = list()
    with open(file_path) as input_file:
        for line in input_file:
            # add the elf's rucksack to the group as a set
            elf_group.append(set(line.strip()))
            # full group
            if len(elf_group) == 3:
                common_item = (elf_group[0] & elf_group[1] & elf_group[2]).pop()
                priority_sum += get_priority(common_item)
                elf_group = list()
    print(priority_sum)

if __name__ == "__main__":
    main('example.txt')
    main('input.txt')
