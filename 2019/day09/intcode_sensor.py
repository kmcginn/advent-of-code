#! python3
"""
from: https://adventofcode.com/2019/day/9

--- Day 9: Sensor Boost ---
You've just said goodbye to the rebooted rover and left Mars when you receive a faint distress
signal coming from the asteroid belt. It must be the Ceres monitoring station!

In order to lock on to the signal, you'll need to boost your sensors. The Elves send up the latest
BOOST program - Basic Operation Of System Test.

While BOOST (your puzzle input) is capable of boosting your sensors, for tenuous safety reasons, it
refuses to do so until the computer it runs on passes some checks to demonstrate it is a complete
Intcode computer.

Your existing Intcode computer is missing one key feature: it needs support for parameters in
relative mode.

Parameters in mode 2, relative mode, behave very similarly to parameters in position mode: the
parameter is interpreted as a position. Like position mode, parameters in relative mode can be read
from or written to.

The important difference is that relative mode parameters don't count from address 0. Instead, they
count from a value called the relative base. The relative base starts at 0.

The address a relative mode parameter refers to is itself plus the current relative base. When the
relative base is 0, relative mode parameters and position mode parameters with the same value refer
to the same address.

For example, given a relative base of 50, a relative mode parameter of -7 refers to memory address
50 + -7 = 43.

The relative base is modified with the relative base offset instruction:

Opcode 9 adjusts the relative base by the value of its only parameter. The relative base increases
(or decreases, if the value is negative) by the value of the parameter.
For example, if the relative base is 2000, then after the instruction 109,19, the relative base
would be 2019. If the next instruction were 204,-34, then the value at address 1985 would be output.

Your Intcode computer will also need a few other capabilities:

The computer's available memory should be much larger than the initial program. Memory beyond the
initial program starts with the value 0 and can be read or written like any other memory. (It is
invalid to try to access memory at a negative address, though.)
The computer should have support for large numbers. Some instructions near the beginning of the
BOOST program will verify this capability.
Here are some example programs that use these features:

109,1,204,-1,1001,100,1,100,1008,100,16,101,1006,101,0,99 takes no input and produces a copy of
itself as output.
1102,34915192,34915192,7,4,7,99,0 should output a 16-digit number.
104,1125899906842624,99 should output the large number in the middle.
The BOOST program will ask for a single input; run it in test mode by providing it the value 1. It
will perform a series of checks on each opcode, output any opcodes (and the associated parameter
modes) that seem to be functioning incorrectly, and finally output a BOOST keycode.

Once your Intcode computer is fully functional, the BOOST program should report no malfunctioning
opcodes when run in test mode; it should only output a single value, the BOOST keycode. What BOOST
keycode does it produce?

"""

import os
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
    """Run an Intcode program from memory"""
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
            return

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
            print(output)

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
    # in order to support a memory larger than the program,
    # copy program to a defaultdict with default value of 0
    memory = defaultdict(lambda: 0)
    for i in range(0, len(init_memory)):
        memory[i] = init_memory[i]
    input_list = [1]
    run_intcode(memory, input_list)

if __name__ == "__main__":
    main()
