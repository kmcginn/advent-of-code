#! python3
"""
from: https://adventofcode.com/2019/day/3

--- Part Two ---
It turns out that this circuit is very timing-sensitive; you actually need to minimize the signal
delay.

To do this, calculate the number of steps each wire takes to reach each intersection; choose the
intersection where the sum of both wires' steps is lowest. If a wire visits a position on the grid
multiple times, use the steps value from the first time it visits that position when calculating
the total value of a specific intersection.

The number of steps a wire takes is the total number of grid squares the wire has entered to get to
that location, including the intersection being considered. Again consider the example from above:

...........
.+-----+...
.|.....|...
.|..+--X-+.
.|..|..|.|.
.|.-X--+.|.
.|..|....|.
.|.......|.
.o-------+.
...........
In the above example, the intersection closest to the central port is reached after
8+5+5+2 = 20 steps by the first wire and 7+6+4+3 = 20 steps by the second wire for a total of
20+20 = 40 steps.

However, the top-right intersection is better: the first wire takes only 8+5+2 = 15 and the second
wire takes only 7+6+2 = 15, a total of 15+15 = 30 steps.

Here are the best steps for the extra examples from above:

R75,D30,R83,U83,L12,D49,R71,U7,L72
U62,R66,U55,R34,D71,R55,D58,R83 = 610 steps
R98,U47,R26,D63,R33,U87,L62,D20,R33,U53,R51
U98,R91,D20,R16,D67,R40,U7,R15,U6,R7 = 410 steps
What is the fewest combined steps the wires must take to reach an intersection?

"""

import os

def generate_trail(wire_directions):
    """Given a list of directions, generate a set and list of positions for the wire's path"""
    set_trail = set()
    list_trail = list()
    current_location = (0, 0)
    for direction in wire_directions:
        heading = direction[0]
        distance = int(direction[1:])
        while distance > 0:
            if heading == "R":
                current_location = (current_location[0] + 1, current_location[1])
            elif heading == "L":
                current_location = (current_location[0] - 1, current_location[1])
            elif heading == "U":
                current_location = (current_location[0], current_location[1] + 1)
            elif heading == "D":
                current_location = (current_location[0], current_location[1] - 1)
            else:
                raise Exception
            set_trail.add(current_location)
            list_trail.append(current_location)
            distance -= 1
    return (set_trail, list_trail)

def main():
    """Solve the problem!"""
    script_dir = os.path.dirname(__file__)
    file_path = os.path.join(script_dir, './input.txt')
    with open(file_path) as input_file:
        wire1_directions = input_file.readline().split(",")
        wire2_directions = input_file.readline().split(",")
    wire1_points, wire1_path = generate_trail(wire1_directions)
    wire2_points, wire2_path = generate_trail(wire2_directions)
    crosses = wire1_points.intersection(wire2_points)
    min_distance = None
    for cross in crosses:
        wire1_steps = wire1_path.index(cross) + 1
        wire2_steps = wire2_path.index(cross) + 1
        distance = wire1_steps + wire2_steps
        if(min_distance is None or distance < min_distance):
            min_distance = distance
    print(min_distance)


if __name__ == "__main__":
    main()
