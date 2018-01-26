"""
from: http://adventofcode.com/2017/day/5

--- Part Two ---
Now, the jumps are even stranger: after each jump, if the offset was three or more, instead decrease
it by 1. Otherwise, increase it by 1 as before.
Using this rule with the above example, the process now takes 10 steps, and the offset values after
finding the exit are left as 2 3 2 3 -1.
How many steps does it now take to reach the exit?

"""

def main():
    """Solve the problem!"""
    maze = []
    jump_count = 0
    # import the maze
    with open("input.txt") as input_file:
        for line in input_file:
            maze.append(int(line))
    index = 0
    while index < len(maze):
        jump_value = maze[index]
        if jump_value >= 3:
            maze[index] = maze[index] - 1
        else:
            maze[index] = maze[index] + 1
        index = index + jump_value
        jump_count = jump_count + 1
    print(jump_count)

if __name__ == "__main__":
    main()
