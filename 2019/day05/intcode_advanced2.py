#! python3
"""
from: https://adventofcode.com/2019/day/5

--- Part Two ---
The air conditioner comes online! Its cold air feels good for a while, but then the TEST alarms
start to go off. Since the air conditioner can't vent its heat anywhere but back into the
spacecraft, it's actually making the air inside the ship warmer.

Instead, you'll need to use the TEST to extend the thermal radiators. Fortunately, the diagnostic
program (your puzzle input) is already equipped for this. Unfortunately, your Intcode computer is
not.

Your computer is only missing a few opcodes:

Opcode 5 is jump-if-true: if the first parameter is non-zero, it sets the instruction pointer to
the value from the second parameter. Otherwise, it does nothing.
Opcode 6 is jump-if-false: if the first parameter is zero, it sets the instruction pointer to the
value from the second parameter. Otherwise, it does nothing.
Opcode 7 is less than: if the first parameter is less than the second parameter, it stores 1 in the
position given by the third parameter. Otherwise, it stores 0.
Opcode 8 is equals: if the first parameter is equal to the second parameter, it stores 1 in the
position given by the third parameter. Otherwise, it stores 0.
Like all instructions, these instructions need to support parameter modes as described above.

Normally, after an instruction is finished, the instruction pointer increases by the number of
values in that instruction. However, if the instruction modifies the instruction pointer, that
value is used and the instruction pointer is not automatically increased.

For example, here are several programs that take one input, compare it to the value 8, and then
produce one output:

3,9,8,9,10,9,4,9,99,-1,8 - Using position mode, consider whether the input is equal to 8;
output 1 (if it is) or 0 (if it is not).
3,9,7,9,10,9,4,9,99,-1,8 - Using position mode, consider whether the input is less than 8;
output 1 (if it is) or 0 (if it is not).
3,3,1108,-1,8,3,4,3,99 - Using immediate mode, consider whether the input is equal to 8;
output 1 (if it is) or 0 (if it is not).
3,3,1107,-1,8,3,4,3,99 - Using immediate mode, consider whether the input is less than 8;
output 1 (if it is) or 0 (if it is not).
Here are some jump tests that take an input, then output 0 if the input was zero or 1 if the input
was non-zero:

3,12,6,12,15,1,13,14,13,4,13,99,-1,0,1,9 (using position mode)
3,3,1105,-1,9,1101,0,0,12,4,12,99,1 (using immediate mode)
Here's a larger example:

3,21,1008,21,8,20,1005,20,22,107,8,21,20,1006,20,31,
1106,0,36,98,0,0,1002,21,125,20,4,20,1105,1,46,104,
999,1105,1,46,1101,1000,1,20,4,20,1105,1,46,98,99
The above example program uses an input instruction to ask for a single number. The program will
then output 999 if the input value is below 8, output 1000 if the input value is equal to 8, or
output 1001 if the input value is greater than 8.

This time, when the TEST diagnostic program runs its input instruction to get the ID of the system
to test, provide it 5, the ID for the ship's thermal radiator controller. This diagnostic test
suite only outputs one number, the diagnostic code.

What is the diagnostic code for system ID 5?

"""
import os

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

def run_intcode(memory, input_val):
    """Run an Intcode program from memory and return the result"""
    instr_ptr = 0
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
            # position mode
            if param_modes[0] == 0:
                num1 = memory[memory[instr_ptr + 1]]
            # immediate mode
            elif param_modes[0] == 1:
                num1 = memory[instr_ptr + 1]
            else:
                raise Exception

            # process num2
            # position mode
            if param_modes[1] == 0:
                num2 = memory[memory[instr_ptr + 2]]
            # immediate mode
            elif param_modes[1] == 1:
                num2 = memory[instr_ptr + 2]
            else:
                raise Exception

            # process store
            # position mode
            if param_modes[2] == 0:
                store = memory[instr_ptr + 3]
            # immediate mode
            elif param_modes[2] == 1:
                # this parameter cannot be in immediate mode
                raise Exception
            else:
                raise Exception
            memory[store] = num1 + num2
            instr_ptr = instr_ptr + 4

        # MULTIPLY - num1, num2, store
        elif opcode == 2:
            # process num1
            # position mode
            if param_modes[0] == 0:
                num1 = memory[memory[instr_ptr + 1]]
            # immediate mode
            elif param_modes[0] == 1:
                num1 = memory[instr_ptr + 1]
            else:
                raise Exception

            # process num2
            # position mode
            if param_modes[1] == 0:
                num2 = memory[memory[instr_ptr + 2]]
            # immediate mode
            elif param_modes[1] == 1:
                num2 = memory[instr_ptr + 2]
            else:
                raise Exception

            # process store
            # position mode
            if param_modes[2] == 0:
                store = memory[instr_ptr + 3]
            # immediate mode
            elif param_modes[2] == 1:
                # this parameter cannot be in immediate mode
                raise Exception
            else:
                raise Exception
            memory[store] = num1 * num2
            instr_ptr = instr_ptr + 4

        # INPUT - position
        elif opcode == 3:
            # position mode
            if param_modes[0] == 0:
                position = memory[instr_ptr + 1]
            # immediate mode
            elif param_modes[0] == 1:
                # parameter cannot be in immediate mode
                raise Exception
            else:
                raise Exception
            memory[position] = input_val
            instr_ptr = instr_ptr + 2

        # OUTPUT - position
        elif opcode == 4:
            # position mode
            if param_modes[0] == 0:
                print(memory[memory[instr_ptr + 1]])
            # immediate mode
            elif param_modes[0] == 1:
                print(memory[instr_ptr + 1])
            else:
                raise Exception
            instr_ptr = instr_ptr + 2

        # JUMP-IF-TRUE - test, new_ptr
        elif opcode == 5:
            # process test
            # position mode
            if param_modes[0] == 0:
                test = memory[memory[instr_ptr + 1]]
            # immediate mode
            elif param_modes[0] == 1:
                test = memory[instr_ptr + 1]
            else:
                raise Exception

            # process new_ptr
            # position mode
            if param_modes[1] == 0:
                new_ptr = memory[memory[instr_ptr + 2]]
            # immediate mode
            elif param_modes[1] == 1:
                new_ptr = memory[instr_ptr + 2]
            else:
                raise Exception

            if test != 0:
                instr_ptr = new_ptr
            else:
                instr_ptr = instr_ptr + 3

        # JUMP-IF-FALSE - test, new_ptr
        elif opcode == 6:
            # process test
            # position mode
            if param_modes[0] == 0:
                test = memory[memory[instr_ptr + 1]]
            # immediate mode
            elif param_modes[0] == 1:
                test = memory[instr_ptr + 1]
            else:
                raise Exception

            # process new_ptr
            # position mode
            if param_modes[1] == 0:
                new_ptr = memory[memory[instr_ptr + 2]]
            # immediate mode
            elif param_modes[1] == 1:
                new_ptr = memory[instr_ptr + 2]
            else:
                raise Exception

            if test == 0:
                instr_ptr = new_ptr
            else:
                instr_ptr = instr_ptr + 3

        # LESS THAN - num1, num2, store
        elif opcode == 7:
            # process num1
            # position mode
            if param_modes[0] == 0:
                num1 = memory[memory[instr_ptr + 1]]
            # immediate mode
            elif param_modes[0] == 1:
                num1 = memory[instr_ptr + 1]
            else:
                raise Exception

            # process num2
            # position mode
            if param_modes[1] == 0:
                num2 = memory[memory[instr_ptr + 2]]
            # immediate mode
            elif param_modes[1] == 1:
                num2 = memory[instr_ptr + 2]
            else:
                raise Exception

            # process store
            # position mode
            if param_modes[2] == 0:
                store = memory[instr_ptr + 3]
            # immediate mode
            elif param_modes[2] == 1:
                # this parameter cannot be in immediate mode
                raise Exception
            else:
                raise Exception

            if num1 < num2:
                memory[store] = 1
            else:
                memory[store] = 0
            instr_ptr = instr_ptr + 4

        # EQUALS - num1, num2, store
        elif opcode == 8:
            # process num1
            # position mode
            if param_modes[0] == 0:
                num1 = memory[memory[instr_ptr + 1]]
            # immediate mode
            elif param_modes[0] == 1:
                num1 = memory[instr_ptr + 1]
            else:
                raise Exception

            # process num2
            # position mode
            if param_modes[1] == 0:
                num2 = memory[memory[instr_ptr + 2]]
            # immediate mode
            elif param_modes[1] == 1:
                num2 = memory[instr_ptr + 2]
            else:
                raise Exception

            # process store
            # position mode
            if param_modes[2] == 0:
                store = memory[instr_ptr + 3]
            # immediate mode
            elif param_modes[2] == 1:
                # this parameter cannot be in immediate mode
                raise Exception
            else:
                raise Exception

            if num1 == num2:
                memory[store] = 1
            else:
                memory[store] = 0
            instr_ptr = instr_ptr + 4

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

    run_intcode(init_memory, 5)

if __name__ == "__main__":
    main()
