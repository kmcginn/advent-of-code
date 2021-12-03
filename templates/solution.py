#! python3
"""
from: <LINK>

<PUZZLE TEXT>

"""

import os

def main(filename):
    """Solve the problem!"""
    script_dir = os.path.dirname(__file__)
    file_path = os.path.join(script_dir, filename)
    with open(file_path) as input_file:
        pass

if __name__ == "__main__":
    main('example.txt')
    main('input.txt')
