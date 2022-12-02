#! python3
"""
Puzzle link: https://adventofcode.com/2022/day/1

"""

import os
from collections import Counter

def main(filename):
    """Find the total calorie amount of the top three elves carrying the highest total calories."""
    script_dir = os.path.dirname(__file__)
    file_path = os.path.join(script_dir, filename)
    calorie_totals = Counter()
    elf_index = 0
    with open(file_path) as input_file:
        for line in input_file:
            if line.isspace():
                elf_index += 1
            else:
                calorie_totals[elf_index] += int(line)
    print(calorie_totals.most_common(3))
    top_three = calorie_totals.most_common(3)
    print(sum([x[1] for x in top_three]))


if __name__ == "__main__":
    main('example.txt')
    main('input.txt')
