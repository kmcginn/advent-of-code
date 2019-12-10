#! python3
"""
from: https://adventofcode.com/2019/day/8

--- Part Two ---
Now you're ready to decode the image. The image is rendered by stacking the layers and aligning the
pixels with the same positions in each layer. The digits indicate the color of the corresponding
pixel: 0 is black, 1 is white, and 2 is transparent.

The layers are rendered with the first layer in front and the last layer in back. So, if a given
position has a transparent pixel in the first and second layers, a black pixel in the third layer,
and a white pixel in the fourth layer, the final image would have a black pixel at that position.

For example, given an image 2 pixels wide and 2 pixels tall, the image data 0222112222120000
corresponds to the following image layers:

Layer 1: 02
         22

Layer 2: 11
         22

Layer 3: 22
         12

Layer 4: 00
         00
Then, the full image can be found by determining the top visible pixel in each position:

The top-left pixel is black because the top layer is 0.
The top-right pixel is white because the top layer is 2 (transparent), but the second layer is 1.
The bottom-left pixel is white because the top two layers are 2, but the third layer is 1.
The bottom-right pixel is black because the only visible pixel in that position is 0 (from layer 4).
So, the final image looks like this:

01
10
What message is produced after decoding your image?

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
    flat_image = flatten_image(layered_image)
    render_image(flat_image, width, height)

def flatten_image(layered_image):
    """Flattens an array of layered images (string) into an array of ints"""
    layer_length = len(layered_image[0])
    # initialize empty flattened image
    flattened_image = [-1 for x in range(0, layer_length)]
    for pixel in range(0, layer_length):
        for layer in layered_image:
            # pixel has not been set
            if flattened_image[pixel] == -1:
                flattened_image[pixel] = int(layer[pixel])
            # overwite transparent pixels only
            elif flattened_image[pixel] == 2:
                flattened_image[pixel] = int(layer[pixel])
    return flattened_image

def render_image(image_data, width, height):
    """Displays an image given an array of pixels and the dimensions"""
    display_line = ''
    for pixel in image_data:
        if pixel == 0:
            display_line += " "
        elif pixel == 1:
            display_line += "*"
        else:
            raise Exception
        if len(display_line) == width:
            print(display_line)
            display_line = ''

if __name__ == "__main__":
    main()
