#! python3
"""
from: https://adventofcode.com/2019/day/12

--- Part Two ---
All this drifting around in space makes you wonder about the nature of the universe. Does history
really repeat itself? You're curious whether the moons will ever return to a previous state.

Determine the number of steps that must occur before all of the moons' positions and velocities
exactly match a previous point in time.

For example, the first example above takes 2772 steps before they exactly match a previous point in
time; it eventually returns to the initial state:

After 0 steps:
pos=<x= -1, y=  0, z=  2>, vel=<x=  0, y=  0, z=  0>
pos=<x=  2, y=-10, z= -7>, vel=<x=  0, y=  0, z=  0>
pos=<x=  4, y= -8, z=  8>, vel=<x=  0, y=  0, z=  0>
pos=<x=  3, y=  5, z= -1>, vel=<x=  0, y=  0, z=  0>

After 2770 steps:
pos=<x=  2, y= -1, z=  1>, vel=<x= -3, y=  2, z=  2>
pos=<x=  3, y= -7, z= -4>, vel=<x=  2, y= -5, z= -6>
pos=<x=  1, y= -7, z=  5>, vel=<x=  0, y= -3, z=  6>
pos=<x=  2, y=  2, z=  0>, vel=<x=  1, y=  6, z= -2>

After 2771 steps:
pos=<x= -1, y=  0, z=  2>, vel=<x= -3, y=  1, z=  1>
pos=<x=  2, y=-10, z= -7>, vel=<x= -1, y= -3, z= -3>
pos=<x=  4, y= -8, z=  8>, vel=<x=  3, y= -1, z=  3>
pos=<x=  3, y=  5, z= -1>, vel=<x=  1, y=  3, z= -1>

After 2772 steps:
pos=<x= -1, y=  0, z=  2>, vel=<x=  0, y=  0, z=  0>
pos=<x=  2, y=-10, z= -7>, vel=<x=  0, y=  0, z=  0>
pos=<x=  4, y= -8, z=  8>, vel=<x=  0, y=  0, z=  0>
pos=<x=  3, y=  5, z= -1>, vel=<x=  0, y=  0, z=  0>
Of course, the universe might last for a very long time before repeating. Here's a copy of the
second example from above:

<x=-8, y=-10, z=0>
<x=5, y=5, z=10>
<x=2, y=-7, z=3>
<x=9, y=-8, z=-3>
This set of initial positions takes 4686774924 steps before it repeats a previous state! Clearly,
you might need to find a more efficient way to simulate the universe.

How many steps does it take to reach the first state that exactly matches a previous state?
"""

import os
from functools import reduce

def main():
    """Solve the problem!"""
    script_dir = os.path.dirname(__file__)
    file_path = os.path.join(script_dir, './example2.txt')
    moons_pos = list()
    with open(file_path) as input_file:
        for line in input_file:
            moons_pos.append(parse_coords(line))
    moons_vel = [[0, 0, 0] for x in range(0, len(moons_pos))]
    previous_states = { str(moons_pos) + str(moons_vel) }
    steps_taken = 0
    show_steps = False
    while True:
        step_simulation(moons_pos, moons_vel)
        steps_taken += 1
        if show_steps:
            print("After", steps_taken, " steps")
            for j in range(0, len(moons_pos)):
                print("Position:", moons_pos[j], "Velocity:", moons_vel[j])
        state_str = str(moons_pos) + str(moons_vel)
        if state_str in previous_states:
            break
        previous_states.add(state_str)
    print(steps_taken)

def parse_coords(coord_str):
    """Parse a line like <x=1, y=2, z=-3> into [1, 2, -3]"""
    coords = coord_str.strip('<>\n').split(',')
    return [int(coords[x].split('=')[1]) for x in range(0, 3)]

def step_simulation(moons_pos, moons_vel):
    """Apply one step to the simulation bodies"""
    # TODO: MAKE THIS MORE EFFICIENT - matrices?
    # apply gravity to velocity
    for i in range(0, len(moons_pos)):
        for j in range(i+1, len(moons_pos)):
            for coord in range(0, 3):
                if moons_pos[i][coord] == moons_pos[j][coord]:
                    continue
                if moons_pos[i][coord] > moons_pos[j][coord]:
                    moons_vel[i][coord] -= 1
                    moons_vel[j][coord] += 1
                else:
                    moons_vel[i][coord] += 1
                    moons_vel[j][coord] -= 1
    # apply velocity to position
    for i in range(0, len(moons_pos)):
        for coord in range(0, 3):
            moons_pos[i][coord] += moons_vel[i][coord]

if __name__ == "__main__":
    main()
