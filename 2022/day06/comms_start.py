#! python3
"""
Puzzle link: https://adventofcode.com/2022/day/6
"""

import os

def main(filename):
    """Solve the problem!"""
    script_dir = os.path.dirname(__file__)
    file_path = os.path.join(script_dir, filename)
    data_stream = ''
    with open(file_path) as input_file:
        data_stream : str = input_file.readline()
    cursor = 0
    while True:
        sequence = data_stream[cursor:cursor+4]
        if len(set(sequence)) == 4:
            break
        else:
            cursor += 1
    print(cursor+4)

if __name__ == "__main__":
    main('example1.txt')
    main('example2.txt')
    main('example3.txt')
    main('example4.txt')
    main('input.txt')
