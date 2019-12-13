#! python3
"""
from: https://adventofcode.com/2019/day/7

--- Part Two ---
It's no good - in this configuration, the amplifiers can't generate a large enough output signal to
produce the thrust you'll need. The Elves quickly talk you through rewiring the amplifiers into a
feedback loop:

      O-------O  O-------O  O-------O  O-------O  O-------O
0 -+->| Amp A |->| Amp B |->| Amp C |->| Amp D |->| Amp E |-.
   |  O-------O  O-------O  O-------O  O-------O  O-------O |
   |                                                        |
   '--------------------------------------------------------+
                                                            |
                                                            v
                                                     (to thrusters)
Most of the amplifiers are connected as they were before; amplifier A's output is connected to
amplifier B's input, and so on. However, the output from amplifier E is now connected into
amplifier A's input. This creates the feedback loop: the signal will be sent through the amplifiers
many times.

In feedback loop mode, the amplifiers need totally different phase settings: integers from 5 to 9,
again each used exactly once. These settings will cause the Amplifier Controller Software to
repeatedly take input and produce output many times before halting. Provide each amplifier its
phase setting at its first input instruction; all further input/output instructions are for signals.

Don't restart the Amplifier Controller Software on any amplifier during this process. Each one
should continue receiving and sending signals until it halts.

All signals sent or received in this process will be between pairs of amplifiers except the very
first signal and the very last signal. To start the process, a 0 signal is sent to amplifier A's
input exactly once.

Eventually, the software on the amplifiers will halt after they have processed the final loop. When
this happens, the last output signal from amplifier E is sent to the thrusters. Your job is to find
the largest output signal that can be sent to the thrusters using the new phase settings and
feedback loop arrangement.

Here are some example programs:

Max thruster signal 139629729 (from phase setting sequence 9,8,7,6,5):

3,26,1001,26,-4,26,3,27,1002,27,2,27,1,27,26,
27,4,27,1001,28,-1,28,1005,28,6,99,0,0,5
Max thruster signal 18216 (from phase setting sequence 9,7,8,5,6):

3,52,1001,52,-5,52,3,53,1,52,56,54,1007,54,5,55,1005,55,26,1001,54,
-5,54,1105,1,12,1,53,54,53,1008,54,0,55,1001,55,1,55,2,53,55,53,4,
53,1001,56,-1,56,1005,56,6,99,0,0,0,0,10
Try every combination of the new phase settings on the amplifier feedback loop. What is the highest
signal that can be sent to the thrusters?

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

def run_intcode(memory, input_list, instr_ptr=0, input_ptr=0, previous_output=None):
    """Run an Intcode program from memory"""
    output = previous_output
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
            # position mode
            if param_modes[0] == 0:
                output = memory[memory[instr_ptr + 1]]
            # immediate mode
            elif param_modes[0] == 1:
                output = memory[instr_ptr + 1]
            else:
                raise Exception
            instr_ptr = instr_ptr + 2
            return (output, instr_ptr, input_ptr)

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

class Amplifier:
    """Holds the state of an amplifier"""
    def __init__(self, memory, phase):
        self.memory = memory
        self.input_list = [phase]
        self.instr_ptr = 0
        self.input_ptr = 0
        self.output = None

def main():
    """Solve the problem!"""
    script_dir = os.path.dirname(__file__)
    file_path = os.path.join(script_dir, './input.txt')
    with open(file_path) as input_file:
        init_memory = list(map(int, input_file.read().split(',')))

    all_phase_combos = generate_phase_list([5, 6, 7, 8, 9])
    max_output = None

    for phase_list in all_phase_combos:
        # initialize all amplifiers with phase
        amplifier_states = [Amplifier(init_memory.copy(), phase_list[x]) for x in range(0, 5)]
        # initialize first amp with input of 0
        amplifier_states[0].input_list.append(0)

        final_output = None
        # loop through all the amplifiers continuously until they all halt
        amp_i = 0
        while True:
            curr_amp = amplifier_states[amp_i]
            output_val, new_instr_ptr, new_input_ptr = run_intcode(curr_amp.memory, curr_amp.input_list, curr_amp.instr_ptr, curr_amp.input_ptr, curr_amp.output)

            # store state for current amplifier
            curr_amp.instr_ptr = new_instr_ptr
            curr_amp.input_ptr = new_input_ptr
            curr_amp.output = output_val

            # end looping if last amplifier has halted
            if amp_i == 4 and new_input_ptr == -1:
                final_output = output_val
                break

            # increment to next amplifier
            if amp_i == 4:
                amp_i = 0
            else:
                amp_i += 1

            # send output from current amp to next amp
            amplifier_states[amp_i].input_list.append(output_val)

        if max_output is None or final_output > max_output:
            max_output = final_output
    print(max_output)

if __name__ == "__main__":
    main()
