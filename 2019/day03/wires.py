#! python3
"""
from: https://adventofcode.com/2019/day/3

--- Day 3: Crossed Wires ---
The gravity assist was successful, and you're well on your way to the Venus refuelling station.
During the rush back on Earth, the fuel management system wasn't completely installed, so that's
next on the priority list.

Opening the front panel reveals a jumble of wires. Specifically, two wires are connected to a
central port and extend outward on a grid. You trace the path each wire takes as it leaves the
central port, one wire per line of text (your puzzle input).

The wires twist and turn, but the two wires occasionally cross paths. To fix the circuit, you need
to find the intersection point closest to the central port. Because the wires are on a grid, use
the Manhattan distance for this measurement. While the wires do technically cross right at the
central port where they both start, this point does not count, nor does a wire count as crossing
with itself.

For example, if the first wire's path is R8,U5,L5,D3, then starting from the central port (o), it
goes right 8, up 5, left 5, and finally down 3:

...........
...........
...........
....+----+.
....|....|.
....|....|.
....|....|.
.........|.
.o-------+.
...........
Then, if the second wire's path is U7,R6,D4,L4, it goes up 7, right 6, down 4, and left 4:

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
These wires cross at two locations (marked X), but the lower-left one is closer to the central
port: its distance is 3 + 3 = 6.

Here are a few more examples:

R75,D30,R83,U83,L12,D49,R71,U7,L72
U62,R66,U55,R34,D71,R55,D58,R83 = distance 159
R98,U47,R26,D63,R33,U87,L62,D20,R33,U53,R51
U98,R91,D20,R16,D67,R40,U7,R15,U6,R7 = distance 135
What is the Manhattan distance from the central port to the closest intersection?

"""

import os

def generate_trail(wire_directions):
    """Given a list of wire directions, generate a set of coordinate pairs for the wire's path"""
    trail = set()
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
            trail.add(current_location)
            distance -= 1
    return trail

def main():
    """Solve the problem!"""
    script_dir = os.path.dirname(__file__)
    file_path = os.path.join(script_dir, './input.txt')
    with open(file_path) as input_file:
        wire1_directions = input_file.readline().split(",")
        wire2_directions = input_file.readline().split(",")
    wire1_path = generate_trail(wire1_directions)
    wire2_path = generate_trail(wire2_directions)
    crosses = wire1_path.intersection(wire2_path)
    min_distance = None
    for cross in crosses:
        distance = abs(cross[0]) + abs(cross[1])
        if(min_distance is None or distance < min_distance):
            min_distance = distance
    print(min_distance)


if __name__ == "__main__":
    main()
