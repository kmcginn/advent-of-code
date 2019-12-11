#! python3
"""
from: https://adventofcode.com/2019/day/10

--- Part Two ---
Once you give them the coordinates, the Elves quickly deploy an Instant Monitoring Station to the
location and discover the worst: there are simply too many asteroids.

The only solution is complete vaporization by giant laser.

Fortunately, in addition to an asteroid scanner, the new monitoring station also comes equipped with
a giant rotating laser perfect for vaporizing asteroids. The laser starts by pointing up and always
rotates clockwise, vaporizing any asteroid it hits.

If multiple asteroids are exactly in line with the station, the laser only has enough power to
vaporize one of them before continuing its rotation. In other words, the same asteroids that can be
detected can be vaporized, but if vaporizing one asteroid makes another one detectable, the
newly-detected asteroid won't be vaporized until the laser has returned to the same position by
rotating a full 360 degrees.

For example, consider the following map, where the asteroid with the new monitoring station
(and laser) is marked X:

.#....#####...#..
##...##.#####..##
##...#...#.#####.
..#.....X...###..
..#.#.....#....##
The first nine asteroids to get vaporized, in order, would be:

.#....###24...#..
##...##.13#67..9#
##...#...5.8####.
..#.....X...###..
..#.#.....#....##
Note that some asteroids (the ones behind the asteroids marked 1, 5, and 7) won't have a chance to
be vaporized until the next full rotation. The laser continues rotating; the next nine to be
vaporized are:

.#....###.....#..
##...##...#.....#
##...#......1234.
..#.....X...5##..
..#.9.....8....76
The next nine to be vaporized are then:

.8....###.....#..
56...9#...#.....#
34...7...........
..2.....X....##..
..1..............
Finally, the laser completes its first full rotation (1 through 3), a second rotation (4 through 8),
and vaporizes the last asteroid (9) partway through its third rotation:

......234.....6..
......1...5.....7
.................
........X....89..
.................
In the large example above (the one with the best monitoring station location at 11,13):

The 1st asteroid to be vaporized is at 11,12.
The 2nd asteroid to be vaporized is at 12,1.
The 3rd asteroid to be vaporized is at 12,2.
The 10th asteroid to be vaporized is at 12,8.
The 20th asteroid to be vaporized is at 16,0.
The 50th asteroid to be vaporized is at 16,9.
The 100th asteroid to be vaporized is at 10,16.
The 199th asteroid to be vaporized is at 9,6.
The 200th asteroid to be vaporized is at 8,2.
The 201st asteroid to be vaporized is at 10,9.
The 299th and final asteroid to be vaporized is at 11,1.
The Elves are placing bets on which will be the 200th asteroid to be vaporized. Win the bet by
determining which asteroid that will be; what do you get if you multiply its X coordinate by 100
and then add its Y coordinate? (For example, 8,2 becomes 802.)

"""

import os
import math

def main():
    """Solve the problem!"""
    script_dir = os.path.dirname(__file__)
    file_path = os.path.join(script_dir, './input.txt')
    # generate list of asteroid coordinates from input
    asteroid_coords = list()
    with open(file_path) as input_file:
        row = 0
        for line in input_file:
            col = 0
            for char in line:
                if char == '#':
                    asteroid_coords.append((col, row))
                col += 1
            row += 1
    max_asteroids_seen = None
    station_point = None
    station_asteroids_by_angle = dict()
    for point in asteroid_coords:
        unique_asteroid_angles = set()
        asteroids_by_angle = dict()
        for target in asteroid_coords:
            # skip comparing a point to itself
            if point == target:
                continue
            # calculate the angle (radians) between the evaluated point and the target asteroid
            delta_y = target[1] - point[1]
            delta_x = target[0] - point[0]
            angle = math.atan2(delta_y, delta_x)
            # only store unique angles for determining best station location
            # (since the first asteroid "blocks" others in that line)
            unique_asteroid_angles.add(angle)

            # store all coords by angle (degrees) for laser elimination
            # adjust angle so 0 is pointing "up" on the map
            deg_angle = math.degrees(angle) + 90
            # convert negative angles to positive equivalent
            if deg_angle < 0:
                deg_angle += 360
            if deg_angle in asteroids_by_angle.keys():
                asteroids_by_angle[deg_angle].append(target)
            else:
                asteroids_by_angle[deg_angle] = [target]
        # determine if current point is optimal station
        if max_asteroids_seen is None or len(unique_asteroid_angles) > max_asteroids_seen:
            max_asteroids_seen = len(unique_asteroid_angles)
            station_point = point
            station_asteroids_by_angle = asteroids_by_angle

    # prep for asteroid vaporization from the selected station point
    asteroids_vaporized = 0
    # sort station_asteroids_by_angle by increasing distance from the station
    for angle in station_asteroids_by_angle:
        station_asteroids_by_angle[angle].sort(key=lambda point: math.dist(station_point, point))
    # get a list of the angles in increasing order
    ordered_angles = list(station_asteroids_by_angle.keys())
    ordered_angles.sort()
    # vaporize asteroids!
    asteroids_remaining = True
    while asteroids_remaining:
        asteroids_remaining = False
        for angle in ordered_angles:
            # all asteroids at this angle have been destroyed
            if len(station_asteroids_by_angle[angle]) == 0:
                continue
            asteroids_remaining = True
            vaporized = station_asteroids_by_angle[angle].pop(0)
            asteroids_vaporized += 1
            if asteroids_vaporized == 200:
                print("200th asteroid destroyed is:", vaporized)
    print("Total asteroids vaporized:", asteroids_vaporized)


if __name__ == "__main__":
    main()
