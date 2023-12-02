#! python3
"""
from: https://adventofcode.com/2023/day/1

<PUZZLE TEXT>

"""

import os

def extract_numbers(s : str):
  nums = []
  for c in s:
    if c.isnumeric():
      nums.append(int(c))
  return nums

def main(filename):
    """Solve the problem!"""
    script_dir = os.path.dirname(__file__)
    file_path = os.path.join(script_dir, filename)
    total = 0
    with open(file_path) as input_file:
        for line in input_file:
          nums = extract_numbers(line)
          total += (nums[0] * 10) + nums[len(nums) - 1]
    print(total)



if __name__ == "__main__":
    main('example.txt')
    main('input.txt')
