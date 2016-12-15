def handleTurn(heading, turn):
    if heading == 'N':
        if turn == 'L':
            return 'W'
        else:
            return 'E'
    elif heading == 'S':
        if turn == 'L':
            return 'E'
        else:
            return 'W'
    elif heading == 'E':
        if turn == 'L':
            return 'N'
        else:
            return 'S'
    elif heading == 'W':
        if turn == 'L':
            return 'S'
        else:
            return 'N'
    else:
        raise Exception

def updateLocation(heading, x, y, turn, distance):
    # update heading
    newHeading = handleTurn(heading, turn)
    # modify counter
    newX = x
    newY = y
    if newHeading == 'N':
        newX = x + distance
    elif newHeading == 'S':
        newX = x - distance
    elif newHeading == 'E':
        newY = y + distance
    elif newHeading == 'W':
        newY = y - distance
    else:
        raise Exception

    return (newHeading, newX, newY)

def checkIntersection(a, b, c, d):
    # a->b is vertical
    if a[0] == b[0]:
        # c->d is also vertical
        if c[0] == d[0]:
            return False
        else:
            if a[1] > b[1]:
                bigY1 = a[1]
                smallY1 = b[1]
            else:
                bigY1 = b[1]
                smallY1 = a[1]
            
                #return c[1] < a[1] and c[1] > b[1]
            #else:
                #return c[1] < b[1] and c[1] > a[1]
    # a->b is horizontal
    else:
        # c->d is also horizontal
        if c[1] == d[1]:
            return False
        else:
            if a[0] > b[0]:
                return c[0] < a[0] and c[0] > b[0]
            else:
                return c[0] < b[0] and c[0]


def processData():
    rawData = 'L5, R1, R3, L4, R3, R1, L3, L2, R3, L5, L1, L2, R5, L1, R5, R1, L4, R1, R3, L4, L1, R2, R5, R3, R1, R1, L1, R1, L1, L2, L1, R2, L5, L188, L4, R1, R4, L3, R47, R1, L1, R77, R5, L2, R1, L2, R4, L5, L1, R3, R187, L4, L3, L3, R2, L3, L5, L4, L4, R1, R5, L4, L3, L3, L3, L2, L5, R1, L2, R5, L3, L4, R4, L5, R3, R4, L2, L1, L4, R1, L3, R1, R3, L2, R1, R4, R5, L3, R5, R3, L3, R4, L2, L5, L1, L1, R3, R1, L4, R3, R3, L2, R5, R4, R1, R3, L4, R3, R3, L2, L4, L5, R1, L4, L5, R4, L2, L1, L3, L3, L5, R3, L4, L3, R5, R4, R2, L4, R2, R3, L3, R4, L1, L3, R2, R1, R5, L4, L5, L5, R4, L5, L2, L4, R4, R4, R1, L3, L2, L4, R3'

    return rawData.split(', ')

def main():
    #instructions = processData()
    instructions = ['R8', 'R4', 'R4', 'R8']
    heading = 'N'
    x = 0
    y = 0
    locations = [(x, y)]
    for i in instructions:
        turn = i[0]
        distance = int(i[1:])
        result = updateLocation(heading, x, y, turn, distance)
        heading = result[0]
        x = result[1]
        y = result[2]
        locations.append((x, y))
    
    totalDistance = abs(x) + abs(y)
    print(locations)
    print(totalDistance)

main()
