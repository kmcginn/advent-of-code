#! python3
"""
from: https://adventofcode.com/2019/day/6

--- Day 6: Universal Orbit Map ---
You've landed at the Universal Orbit Map facility on Mercury. Because navigation in space often
involves transferring between orbits, the orbit maps here are useful for finding efficient routes
between, for example, you and Santa. You download a map of the local orbits (your puzzle input).

Except for the universal Center of Mass (COM), every object in space is in orbit around exactly one
other object. An orbit looks roughly like this:

                  \
                   \
                    |
                    |
AAA--> o            o <--BBB
                    |
                    |
                   /
                  /
In this diagram, the object BBB is in orbit around AAA. The path that BBB takes around AAA
(drawn with lines) is only partly shown. In the map data, this orbital relationship is written
AAA)BBB, which means "BBB is in orbit around AAA".

Before you use your map data to plot a course, you need to make sure it wasn't corrupted during the
download. To verify maps, the Universal Orbit Map facility uses orbit count checksums - the total
number of direct orbits (like the one shown above) and indirect orbits.

Whenever A orbits B and B orbits C, then A indirectly orbits C. This chain can be any number of
objects long: if A orbits B, B orbits C, and C orbits D, then A indirectly orbits D.

For example, suppose you have the following map:

COM)B
B)C
C)D
D)E
E)F
B)G
G)H
D)I
E)J
J)K
K)L
Visually, the above map of orbits looks like this:

        G - H       J - K - L
       /           /
COM - B - C - D - E - F
               \
                I
In this visual representation, when two objects are connected by a line, the one on the right
directly orbits the one on the left.

Here, we can count the total number of orbits as follows:

D directly orbits C and indirectly orbits B and COM, a total of 3 orbits.
L directly orbits K and indirectly orbits J, E, D, C, B, and COM, a total of 7 orbits.
COM orbits nothing.
The total number of direct and indirect orbits in this example is 42.

What is the total number of direct and indirect orbits in your map data?

"""

import os

def dfs_graph(curr_node, depth, graph, depth_dict):
    """Perform Depth First Search from the current node, recording depths of all nodes"""
    # record depth of current node
    depth_dict[curr_node] = depth

    # base case: we hit a leaf node
    if curr_node not in graph.keys():
        return

    children = graph[curr_node]
    for child in children:
        dfs_graph(child, depth + 1, graph, depth_dict)
    return

def main():
    """Solve the problem!"""
    script_dir = os.path.dirname(__file__)
    file_path = os.path.join(script_dir, './input.txt')
    edge_dict = dict()
    with open(file_path) as input_file:
        for line in input_file:
            orbit_pair = line.strip().split(")")
            if orbit_pair[0] in edge_dict.keys():
                edge_dict[orbit_pair[0]].append(orbit_pair[1])
            else:
                edge_dict[orbit_pair[0]] = [orbit_pair[1]]
    depth_dict = dict()
    dfs_graph("COM", 0, edge_dict, depth_dict)
    total_orbits = 0
    for depth in depth_dict.values():
        total_orbits += depth
    print(total_orbits)


if __name__ == "__main__":
    main()
