#! python3
"""
from: https://adventofcode.com/2022/day/4
"""

import os

def parse_sectors(input: str):
    """Given a string like '7-9,10-13', return two sets containing the sectors in each range"""
    first, second = input.split(sep=",")
    first_start, first_end = [int(x) for x in first.split(sep="-")]
    second_start, second_end = [int(x) for x in second.split(sep="-")]
    return (set(range(first_start, first_end + 1)), set(range(second_start, second_end + 1)))

def main(filename):
    """Solve the problem!"""
    script_dir = os.path.dirname(__file__)
    file_path = os.path.join(script_dir, filename)
    total_full_overlaps = 0
    with open(file_path) as input_file:
        for line in input_file:
            first_sectors, second_sectors = parse_sectors(line)
            if first_sectors.issubset(second_sectors) or second_sectors.issubset(first_sectors):
                total_full_overlaps += 1
    print(total_full_overlaps)


if __name__ == "__main__":
    main('example.txt')
    main('input.txt')
