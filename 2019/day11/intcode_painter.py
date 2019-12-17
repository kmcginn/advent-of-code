#! python3
"""
from: https://adventofcode.com/2019/day/11

--- Day 11: Space Police ---
On the way to Jupiter, you're pulled over by the Space Police.

"Attention, unmarked spacecraft! You are in violation of Space Law! All spacecraft must have a
clearly visible registration identifier! You have 24 hours to comply or be sent to Space Jail!"

Not wanting to be sent to Space Jail, you radio back to the Elves on Earth for help. Although it
takes almost three hours for their reply signal to reach you, they send instructions for how to
power up the emergency hull painting robot and even provide a small Intcode program (your puzzle
input) that will cause it to paint your ship appropriately.

There's just one problem: you don't have an emergency hull painting robot.

You'll need to build a new emergency hull painting robot. The robot needs to be able to move around
on the grid of square panels on the side of your ship, detect the color of its current panel, and
paint its current panel black or white. (All of the panels are currently black.)

The Intcode program will serve as the brain of the robot. The program uses input instructions to
access the robot's camera: provide 0 if the robot is over a black panel or 1 if the robot is over a
white panel. Then, the program will output two values:

First, it will output a value indicating the color to paint the panel the robot is over: 0 means to
paint the panel black, and 1 means to paint the panel white.
Second, it will output a value indicating the direction the robot should turn: 0 means it should
turn left 90 degrees, and 1 means it should turn right 90 degrees.
After the robot turns, it should always move forward exactly one panel. The robot starts facing up.

The robot will continue running for a while like this and halt when it is finished drawing. Do not
restart the Intcode computer inside the robot during this process.

For example, suppose the robot is about to start running. Drawing black panels as ., white panels
as #, and the robot pointing the direction it is facing (< ^ > v), the initial state and region
near the robot looks like this:

.....
.....
..^..
.....
.....
The panel under the robot (not visible here because a ^ is shown instead) is also black, and so any
input instructions at this point should be provided 0. Suppose the robot eventually outputs 1 (paint
white) and then 0 (turn left). After taking these actions and moving forward one panel, the region
now looks like this:

.....
.....
.<#..
.....
.....
Input instructions should still be provided 0. Next, the robot might output 0 (paint black) and
then 0 (turn left):

.....
.....
..#..
.v...
.....
After more outputs (1,0, 1,0):

.....
.....
..^..
.##..
.....
The robot is now back where it started, but because it is now on a white panel, input instructions
should be provided 1. After several more outputs (0,1, 1,0, 1,0), the area looks like this:

.....
..<#.
...#.
.##..
.....
Before you deploy the robot, you should probably have an estimate of the area it will cover:
specifically, you need to know the number of panels it paints at least once, regardless of color.
In the example above, the robot painted 6 panels at least once. (It painted its starting panel
twice, but that panel is still only counted once; it also never painted the panel it ended on.)

Build a new emergency hull painting robot and run the Intcode program on it. How many panels does
it paint at least once?

"""

import os
from enum import Enum, auto
from collections import defaultdict

def list_digits(number):
    """Takes up to a 6 digit int and returns a list of each digit in order"""
    factor = 100000
    digits = list()
    while factor > 1:
        digits.append(number // factor)
        number = number % factor
        factor //= 10
    digits.append(number)
    return digits

def get_param_value(mode, memory, ptr, relative_base):
    """Returns the value of the parameter at memory[ptr] based on the mode"""
    # position mode
    if mode == 0:
        return memory[memory[ptr]]
    # immediate mode
    elif mode == 1:
        return memory[ptr]
    # relative mode
    elif mode == 2:
        return memory[memory[ptr] + relative_base]
    else:
        raise Exception

def get_write_param_value(mode, memory, ptr, relative_base):
    """Returns the value of the paramter at memory[ptr] based on the mode, for a writing paramter"""
    # position mode
    if mode == 0:
        return memory[ptr]
    # immediate mode
    elif mode == 1:
        # immediate mode is not supported
        raise Exception
    elif mode == 2:
        return memory[ptr] + relative_base
    else:
        raise Exception

def run_intcode(memory, input_list, instr_ptr=0, input_ptr=0, previous_output=None):
    """Run an Intcode program from memory. Returns output, instr_ptr, input_ptr"""
    output = previous_output
    relative_base = 0
    while instr_ptr < len(memory):
        instruction = memory[instr_ptr]
        digits = list_digits(instruction)

        # extract opcode
        opcode_pair = digits[len(digits)-2:]
        opcode = opcode_pair[0]*10 + opcode_pair[1]

        # extract parameter modes
        param_modes = digits[:len(digits)-2]
        param_modes.reverse()

        # HALT
        if opcode == 99:
            return (output, -1, -1)

        # ADD - num1, num2, store
        if opcode == 1:
            # process num1
            num1 = get_param_value(param_modes[0], memory, instr_ptr + 1, relative_base)

            # process num2
            num2 = get_param_value(param_modes[1], memory, instr_ptr + 2, relative_base)

            # process store
            store = get_write_param_value(param_modes[2], memory, instr_ptr + 3, relative_base)

            memory[store] = num1 + num2
            instr_ptr = instr_ptr + 4

        # MULTIPLY - num1, num2, store
        elif opcode == 2:
            # process num1
            num1 = get_param_value(param_modes[0], memory, instr_ptr + 1, relative_base)

            # process num2
            num2 = get_param_value(param_modes[1], memory, instr_ptr + 2, relative_base)

            # process store
            store = get_write_param_value(param_modes[2], memory, instr_ptr + 3, relative_base)

            memory[store] = num1 * num2
            instr_ptr = instr_ptr + 4

        # INPUT - position
        elif opcode == 3:
            position = get_write_param_value(param_modes[0], memory, instr_ptr + 1, relative_base)

            memory[position] = input_list[input_ptr]
            input_ptr = input_ptr + 1
            instr_ptr = instr_ptr + 2

        # OUTPUT - position
        elif opcode == 4:
            output = get_param_value(param_modes[0], memory, instr_ptr + 1, relative_base)

            instr_ptr = instr_ptr + 2
            return (output, instr_ptr, input_ptr)

        # JUMP-IF-TRUE - test, new_ptr
        elif opcode == 5:
            # process test
            test = get_param_value(param_modes[0], memory, instr_ptr + 1, relative_base)

            # process new_ptr
            new_ptr = get_param_value(param_modes[1], memory, instr_ptr + 2, relative_base)

            if test != 0:
                instr_ptr = new_ptr
            else:
                instr_ptr = instr_ptr + 3

        # JUMP-IF-FALSE - test, new_ptr
        elif opcode == 6:
            # process test
            test = get_param_value(param_modes[0], memory, instr_ptr + 1, relative_base)

            # process new_ptr
            new_ptr = get_param_value(param_modes[1], memory, instr_ptr + 2, relative_base)

            if test == 0:
                instr_ptr = new_ptr
            else:
                instr_ptr = instr_ptr + 3

        # LESS THAN - num1, num2, store
        elif opcode == 7:
            # process num1
            num1 = get_param_value(param_modes[0], memory, instr_ptr + 1, relative_base)

            # process num2
            num2 = get_param_value(param_modes[1], memory, instr_ptr + 2, relative_base)

            # process store
            store = get_write_param_value(param_modes[2], memory, instr_ptr + 3, relative_base)

            if num1 < num2:
                memory[store] = 1
            else:
                memory[store] = 0
            instr_ptr = instr_ptr + 4

        # EQUALS - num1, num2, store
        elif opcode == 8:
            # process num1
            num1 = get_param_value(param_modes[0], memory, instr_ptr + 1, relative_base)

            # process num2
            num2 = get_param_value(param_modes[1], memory, instr_ptr + 2, relative_base)

            # process store
            store = get_write_param_value(param_modes[2], memory, instr_ptr + 3, relative_base)

            if num1 == num2:
                memory[store] = 1
            else:
                memory[store] = 0
            instr_ptr = instr_ptr + 4

        # RELATIVE BASE OFFSET - offset
        elif opcode == 9:
            offset = get_param_value(param_modes[0], memory, instr_ptr + 1, relative_base)

            relative_base += offset
            instr_ptr = instr_ptr + 2

        # unknown opcode
        else:
            raise Exception
    raise Exception

def main():
    """Solve the problem!"""
    script_dir = os.path.dirname(__file__)
    file_path = os.path.join(script_dir, './input.txt')
    with open(file_path) as input_file:
        init_memory = list(map(int, input_file.read().split(',')))
    # copy program to memory where any unassigned index is 0
    memory = defaultdict(lambda: 0)
    for i in range(0, len(init_memory)):
        memory[i] = init_memory[i]
    # all unpainted hull locations are black
    hull_locations = defaultdict(lambda: 0)
    input_list = list()
    instr_ptr = 0
    input_ptr = 0
    current_location = (0, 0)
    current_direction = Direction.UP
    while True:
        # add the paint color of the current panel to the input list
        input_list.append(hull_locations[current_location])
        # paint the current panel
        paint_color, instr_ptr, input_ptr = run_intcode(memory, input_list, instr_ptr, input_ptr)
        if instr_ptr == -1:
            break
        hull_locations[current_location] = paint_color
        # figure out where to go next
        turn, instr_ptr, input_ptr = run_intcode(memory, input_list, instr_ptr, input_ptr)
        if instr_ptr == -1:
            break
        current_location, current_direction = process_turn(turn, current_location, current_direction)
    # determine number of panels painted at least once
    print(len(hull_locations.keys()))

class Direction(Enum):
    """Enum to define the cardinal directions"""
    UP = auto()
    DOWN = auto()
    LEFT = auto()
    RIGHT = auto()

def process_turn(turn, current_location, current_direction):
    """Given a turn and a current location and direction, return the new location and direction"""
    if current_direction == Direction.UP:
        if turn == 0:
            return ((current_location[0] - 1, current_location[1]), Direction.LEFT)
        elif turn == 1:
            return ((current_location[0] + 1, current_location[1]), Direction.RIGHT)
    elif current_direction == Direction.DOWN:
        if turn == 0:
            return ((current_location[0] + 1, current_location[1]), Direction.RIGHT)
        elif turn == 1:
            return ((current_location[0] - 1, current_location[1]), Direction.LEFT)
    elif current_direction == Direction.LEFT:
        if turn == 0:
            return ((current_location[0], current_location[1] - 1), Direction.DOWN)
        elif turn == 1:
            return ((current_location[0], current_location[1] + 1), Direction.UP)
    elif current_direction == Direction.RIGHT:
        if turn == 0:
            return ((current_location[0], current_location[1] + 1), Direction.UP)
        elif turn == 1:
            return ((current_location[0], current_location[1] - 1), Direction.DOWN)
    raise Exception

if __name__ == "__main__":
    main()
