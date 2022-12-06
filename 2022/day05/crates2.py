#! python3
"""
Puzzle link: https://adventofcode.com/2022/day/5
"""

import os
from collections import deque

# manually create the initial crate layouts
# index 0 of the deque is the ground
example_crates = [deque('ZN'), deque('MCD'), deque('P')]
input_crates = [deque('SZPDLBFC'), deque('NVGPHWB'), deque('FWBJG'), deque('GJNFLWCS'), deque('WJLTPMSH'), deque('BCWGFS'), deque('HTPMQBW'), deque('FSWT'), deque('NCR')]

def main(filename, crates):
    """Solve the problem!"""
    script_dir = os.path.dirname(__file__)
    file_path = os.path.join(script_dir, filename)
    with open(file_path) as input_file:
        for line in input_file:
            split_instruction = line.split(sep=" ")
            amount = int(split_instruction[1])
            source = int(split_instruction[3]) - 1
            destination = int(split_instruction[5]) - 1
            # create the stack to move
            stack = deque()
            for x in range(amount):
                crate = crates[source].pop()
                stack.append(crate)
            # apply the stack
            for x in range(amount):
                crate = stack.pop()
                crates[destination].append(crate)
        message = ''
        for column in crates:
            message += column[-1]
        print(message)

if __name__ == "__main__":
    main('example_instructions_only.txt', example_crates)
    main('input_instructions_only.txt', input_crates)
