def isValidTriangle(sides):
    if len(sides) != 3:
        raise Exception
    sides.sort()
    if (sides[0] + sides[1]) > sides[2]:
        return True
    else:
        return False

def main():
    f = open('input.txt', 'r')
    count = 0
    for line in f:
        sides = line.split()
        convertedSides = [int(s) for s in sides]
        print(convertedSides)
        if isValidTriangle(convertedSides):
            count = count + 1
    print(count)

if __name__ == "__main__":
    main()
