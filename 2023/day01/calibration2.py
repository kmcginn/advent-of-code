#! python3
"""
from: https://adventofcode.com/2023/day/1

<PUZZLE TEXT>

"""

import os
import re

def str_to_num(s : str):
  if s == "one":
    return 1
  elif s == "two":
    return 2
  elif s == "three":
    return 3
  elif s == "four":
    return 4
  elif s == "five":
    return 5
  elif s == "six":
    return 6
  elif s == "seven":
    return 7
  elif s == "eight":
    return 8
  elif s == "nine":
    return 9
  else:
    return 0

def extract_numbers(s : str):
  nums = []
  pattern = "[1-9]|one|two|three|four|five|six|seven|eight|nine"
  extracted_nums = re.findall(pattern, s)
  for n in extracted_nums:
    if n.isnumeric():
      nums.append(int(n))
    else:
      nums.append(str_to_num(n))

  return nums

def main(filename):
    """Solve the problem!"""
    script_dir = os.path.dirname(__file__)
    file_path = os.path.join(script_dir, filename)
    total = 0
    with open(file_path) as input_file:
        for line in input_file:
          nums = extract_numbers(line)
          val = (nums[0] * 10) + nums[len(nums) - 1]
          total += val
    print(total)



if __name__ == "__main__":
    main('example2.txt')
    main('input.txt')
