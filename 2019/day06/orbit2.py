#! python3
"""
from: https://adventofcode.com/2019/day/6

--- Part Two ---
Now, you just need to figure out how many orbital transfers you (YOU) need to take to get to Santa
(SAN).

You start at the object YOU are orbiting; your destination is the object SAN is orbiting. An
orbital transfer lets you move from any object to an object orbiting or orbited by that object.

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
K)YOU
I)SAN
Visually, the above map of orbits looks like this:

                          YOU
                         /
        G - H       J - K - L
       /           /
COM - B - C - D - E - F
               \
                I - SAN
In this example, YOU are in orbit around K, and SAN is in orbit around I. To move from K to I, a
minimum of 4 orbital transfers are required:

K to J
J to E
E to D
D to I
Afterward, the map of orbits looks like this:

        G - H       J - K - L
       /           /
COM - B - C - D - E - F
               \
                I - SAN
                 \
                  YOU
What is the minimum number of orbital transfers required to move from the object YOU are orbiting
to the object SAN is orbiting? (Between the objects they are orbiting - not between YOU and SAN.)

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
    file_path = os.path.join(script_dir, './example2.txt')
    edge_dict = dict()
    with open(file_path) as input_file:
        for line in input_file:
            orbit_pair = line.strip().split(")")
            if orbit_pair[0] in edge_dict.keys():
                edge_dict[orbit_pair[0]].append(orbit_pair[1])
            else:
                edge_dict[orbit_pair[0]] = [orbit_pair[1]]
    min_transfers = None
    # perform DFS on each node in the graph to find nodes that have YOU and SAN as children
    for node in edge_dict:
        depth_dict = dict()
        dfs_graph(node, 0, edge_dict, depth_dict)
        if "YOU" in depth_dict.keys() and "SAN" in depth_dict.keys():
            transfers = depth_dict["YOU"] + depth_dict["SAN"] - 2
            if min_transfers is None or transfers < min_transfers:
                min_transfers = transfers
    print(min_transfers)



if __name__ == "__main__":
    main()
