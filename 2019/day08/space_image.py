#! python3
"""
from: https://adventofcode.com/2019/day/8

--- Day 8: Space Image Format ---
The Elves' spirits are lifted when they realize you have an opportunity to reboot one of their Mars
rovers, and so they are curious if you would spend a brief sojourn on Mars. You land your ship near
the rover.

When you reach the rover, you discover that it's already in the process of rebooting! It's just
waiting for someone to enter a BIOS password. The Elf responsible for the rover takes a picture of
the password (your puzzle input) and sends it to you via the Digital Sending Network.

Unfortunately, images sent via the Digital Sending Network aren't encoded with any normal encoding;
instead, they're encoded in a special Space Image Format. None of the Elves seem to remember why
this is the case. They send you the instructions to decode it.

Images are sent as a series of digits that each represent the color of a single pixel. The digits
fill each row of the image left-to-right, then move downward to the next row, filling rows
top-to-bottom until every pixel of the image is filled.

Each image actually consists of a series of identically-sized layers that are filled in this way.
So, the first digit corresponds to the top-left pixel of the first layer, the second digit
corresponds to the pixel to the right of that on the same layer, and so on until the last digit,
which corresponds to the bottom-right pixel of the last layer.

For example, given an image 3 pixels wide and 2 pixels tall, the image data 123456789012
corresponds to the following image layers:

Layer 1: 123
         456

Layer 2: 789
         012
The image you received is 25 pixels wide and 6 pixels tall.

To make sure the image wasn't corrupted during transmission, the Elves would like you to find the
layer that contains the fewest 0 digits. On that layer, what is the number of 1 digits multiplied
by the number of 2 digits?

"""

import os

def main():
    """Solve the problem!"""
    script_dir = os.path.dirname(__file__)
    file_path = os.path.join(script_dir, './input.txt')
    width = 25
    height = 6
    with open(file_path) as input_file:
        raw_data = input_file.readline()
    layered_image = list()
    layer_length = width * height
    # separate the raw data into layers
    for i in range(0, len(raw_data), layer_length):
        layer_data = raw_data[i:i+layer_length]
        layered_image.append(layer_data)
    min_zeroes = None
    mult_result = None
    # count the digits in each layer
    for layer in layered_image:
        digit_counts = {'0': 0, '1': 0, '2': 0}
        for digit in layer:
            digit_counts[digit] += 1
        if min_zeroes is None or digit_counts['0'] < min_zeroes:
            min_zeroes = digit_counts['0']
            mult_result = digit_counts['1'] * digit_counts['2']
    print(mult_result)

if __name__ == "__main__":
    main()
