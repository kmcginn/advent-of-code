#! python3
"""
from: https://adventofcode.com/2019/day/7

--- Day 7: Amplification Circuit ---
Based on the navigational maps, you're going to need to send more power to your ship's thrusters to
reach Santa in time. To do this, you'll need to configure a series of amplifiers already installed
on the ship.

There are five amplifiers connected in series; each one receives an input signal and produces an
output signal. They are connected such that the first amplifier's output leads to the second
amplifier's input, the second amplifier's output leads to the third amplifier's input, and so on.
The first amplifier's input value is 0, and the last amplifier's output leads to your ship's
thrusters.

    O-------O  O-------O  O-------O  O-------O  O-------O
0 ->| Amp A |->| Amp B |->| Amp C |->| Amp D |->| Amp E |-> (to thrusters)
    O-------O  O-------O  O-------O  O-------O  O-------O
The Elves have sent you some Amplifier Controller Software (your puzzle input), a program that
should run on your existing Intcode computer. Each amplifier will need to run a copy of the program.

When a copy of the program starts running on an amplifier, it will first use an input instruction
to ask the amplifier for its current phase setting (an integer from 0 to 4). Each phase setting is
used exactly once, but the Elves can't remember which amplifier needs which phase setting.

The program will then call another input instruction to get the amplifier's input signal, compute
the correct output signal, and supply it back to the amplifier with an output instruction. (If the
amplifier has not yet received an input signal, it waits until one arrives.)

Your job is to find the largest output signal that can be sent to the thrusters by trying every
possible combination of phase settings on the amplifiers. Make sure that memory is not shared or
reused between copies of the program.

For example, suppose you want to try the phase setting sequence 3,1,2,4,0, which would mean setting
amplifier A to phase setting 3, amplifier B to setting 1, C to 2, D to 4, and E to 0. Then, you
could determine the output signal that gets sent from amplifier E to the thrusters with the
following steps:

Start the copy of the amplifier controller software that will run on amplifier A. At its first input
instruction, provide it the amplifier's phase setting, 3. At its second input instruction, provide
it the input signal, 0. After some calculations, it will use an output instruction to indicate the
amplifier's output signal.
Start the software for amplifier B. Provide it the phase setting (1) and then whatever output
signal was produced from amplifier A. It will then produce a new output signal destined for
amplifier C.
Start the software for amplifier C, provide the phase setting (2) and the value from amplifier B,
then collect its output signal.
Run amplifier D's software, provide the phase setting (4) and input value, and collect its output
signal.
Run amplifier E's software, provide the phase setting (0) and input value, and collect its output
signal.
The final output signal from amplifier E would be sent to the thrusters. However, this phase
setting sequence may not have been the best one; another sequence might have sent a higher signal
to the thrusters.

Here are some example programs:

Max thruster signal 43210 (from phase setting sequence 4,3,2,1,0):

3,15,3,16,1002,16,10,16,1,16,15,15,4,15,99,0,0
Max thruster signal 54321 (from phase setting sequence 0,1,2,3,4):

3,23,3,24,1002,24,10,24,1002,23,-1,23,
101,5,23,23,1,24,23,23,4,23,99,0,0
Max thruster signal 65210 (from phase setting sequence 1,0,4,3,2):

3,31,3,32,1002,32,10,32,1001,31,-2,31,1007,31,0,33,
1002,33,7,33,1,33,31,31,1,32,31,31,4,31,99,0,0,0
Try every combination of phase settings on the amplifiers. What is the highest signal that can be
sent to the thrusters?

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

def run_intcode(memory, input_list):
    """Run an Intcode program from memory and return the result"""
    instr_ptr = 0
    input_ptr = 0
    output = None
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
            return output

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
            memory[position] = input_list[input_ptr]
            input_ptr = input_ptr + 1
            instr_ptr = instr_ptr + 2

        # OUTPUT - position
        elif opcode == 4:
            if output is not None:
                raise Exception
            # position mode
            if param_modes[0] == 0:
                output = memory[memory[instr_ptr + 1]]
            # immediate mode
            elif param_modes[0] == 1:
                output = memory[instr_ptr + 1]
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

def generate_phase_list(phase_list):
    """Generate all possible unique lists of given phases"""
    # base case: only one setting left
    if len(phase_list) == 1:
        return [phase_list]

    all_phase_lists = list()

    for phase in phase_list:
        new_list = phase_list.copy()
        new_list.remove(phase)
        sublists = generate_phase_list(new_list)
        for sub in sublists:
            sub.append(phase)
            all_phase_lists.append(sub)
    return all_phase_lists

def main():
    """Solve the problem!"""
    script_dir = os.path.dirname(__file__)
    file_path = os.path.join(script_dir, './input.txt')
    with open(file_path) as input_file:
        init_memory = list(map(int, input_file.read().split(',')))

    all_phase_combos = generate_phase_list([0, 1, 2, 3, 4])
    max_output = None
    for phase_list in all_phase_combos:
        phase_input = 0
        for phase in phase_list:
            memory = init_memory.copy()
            phase_input = run_intcode(memory, [phase, phase_input])
        if max_output is None or phase_input > max_output:
            max_output = phase_input
    print(max_output)

if __name__ == "__main__":
    main()
