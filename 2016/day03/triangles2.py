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
    listA = []
    listB = []
    listC = []
    for line in f:
        row = line.split()
        convertedRow = [int(s) for s in row]
        listA.append(convertedRow[0])
        listB.append(convertedRow[1])
        listC.append(convertedRow[2])
    listA.extend(listB)
    listA.extend(listC)
    for i in range(0, len(listA)-2, 3):
        l = [listA[i], listA[i+1], listA[i+2]]
        if isValidTriangle(l):
            count = count + 1

    print(count)

if __name__ == "__main__":
    main()
