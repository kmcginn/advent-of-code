#! python3
"""
Puzzle link: https://adventofcode.com/2022/day/1

"""

import os

def main(filename):
    """Find the total calorie amount of the elf carrying the highest total calories."""
    script_dir = os.path.dirname(__file__)
    file_path = os.path.join(script_dir, filename)
    total_calories = 0
    highest_calorie_count = 0
    with open(file_path) as input_file:
        for line in input_file:
            if line.isspace():
                if total_calories > highest_calorie_count:
                    highest_calorie_count = total_calories
                total_calories = 0
            else:
                total_calories = total_calories + int(line)
    print(highest_calorie_count)


if __name__ == "__main__":
    main('example.txt')
    main('input.txt')
