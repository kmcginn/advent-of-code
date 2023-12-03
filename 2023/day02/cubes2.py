#! python3
"""
from: https://adventofcode.com/2023/day/2

<PUZZLE TEXT>

"""

import os

def main(filename):
    """Solve the problem!"""
    script_dir = os.path.dirname(__file__)
    file_path = os.path.join(script_dir, filename)
    cube_power_sum = 0
    with open(file_path) as input_file:
        for game in input_file:
          cube_min_counts = { "red": 0, "green": 0, "blue": 0}
          game_label, round_str = game.split(":")
          game_num = int(game_label.split(" ")[1])
          rounds = round_str.strip().split(";")
          for r in rounds:
            cubes = r.split(",")
            for cube in cubes:
              n, color = cube.strip().split(" ")
              if int(n) > cube_min_counts[color]:
                cube_min_counts[color] = int(n)
          cube_power_sum += cube_min_counts["red"] * cube_min_counts["green"] * cube_min_counts["blue"]
    print(cube_power_sum)

if __name__ == "__main__":
    main('example.txt')
    main('input.txt')
