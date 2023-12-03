#! python3
"""
from: https://adventofcode.com/2023/day/2

<PUZZLE TEXT>

"""

import os

def main(filename):
    """Solve the problem!"""
    cube_counts = { "red": 12, "green": 13, "blue": 14 }
    script_dir = os.path.dirname(__file__)
    file_path = os.path.join(script_dir, filename)
    valid_game_id_sum = 0
    with open(file_path) as input_file:
        for game in input_file:
          game_valid = True
          game_label, round_str = game.split(":")
          game_num = int(game_label.split(" ")[1])
          rounds = round_str.strip().split(";")
          for r in rounds:
            cubes = r.split(",")
            for cube in cubes:
              n, color = cube.strip().split(" ")
              if int(n) > cube_counts[color]:
                game_valid = False
          if game_valid:
            valid_game_id_sum += game_num
    print(valid_game_id_sum)

if __name__ == "__main__":
    main('example.txt')
    main('input.txt')
