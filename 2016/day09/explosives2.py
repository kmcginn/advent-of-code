"""
from: http://adventofcode.com/2016/day/9

--- Part Two ---

Apparently, the file actually uses version two of the format.

In version two, the only difference is that markers within decompressed data are decompressed.
This, the documentation explains, provides much more substantial compression capabilities, allowing
many-gigabyte files to be stored in only a few kilobytes.

For example:

(3x3)XYZ still becomes XYZXYZXYZ, as the decompressed section contains no markers.
X(8x2)(3x3)ABCY becomes XABCABCABCABCABCABCY, because the decompressed data from the (8x2) marker
is then further decompressed, thus triggering the (3x3) marker twice for a total of six ABC
sequences.
(27x12)(20x12)(13x14)(7x10)(1x12)A decompresses into a string of A repeated 241920 times.
(25x3)(3x3)ABC(2x3)XY(5x2)PQRSTX(18x9)(3x2)TWO(5x7)SEVEN becomes 445 characters long.
Unfortunately, the computer you brought probably doesn't have enough memory to actually decompress
the file; you'll have to come up with another way to get its decompressed length.

What is the decompressed length of the file using this improved format?
"""

import re

def get_decompressed_length(tag, data):
    """Get the decompressed length of the data after the duplication tag"""
    # do something with recursion?
    # base case is there is no tag in the decompressed data, so return length of the data
    # recursive case is find the tag and the data it applies to, and get_decompressed_length on that
    pass

def main():
    """Solve the problem!"""
    data = 'X(8x2)(3x3)ABCY'
    # with open("input.txt") as input_file:
    #     data = input_file.read()
    decompressed = ''
    # TODO: rewrite the vast majority of this to fit part 2
    while len(data) != 0:

        # find the next tag
        matched = re.search(r'([a-zA-Z]*)(\(([0-9]+)x[0-9]+\))', data)

        if matched is not None:
            # add all the normal stuff to decompressed
            decompressed += matched[1]

            # figure out what will be duplicated
            tag = matched[2]
            dup_length, dup_count = [int(x) for x in tag.strip('()').split('x')]
            dup_this = data[len(matched[0]):len(matched[0]) + dup_length]

            # duplicate it, add to decompressed
            for _ in range(0, dup_count):
                decompressed += dup_this

            # remove normal, tag, and duplicated stuff from remaining data
            data = data[(len(matched[0]) + dup_length):]
        else:
            # no tags left, just append what is left
            decompressed += data
            data = ''
    print(len(decompressed))

if __name__ == "__main__":
    main()
