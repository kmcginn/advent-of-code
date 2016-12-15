from collections import defaultdict
from operator import itemgetter
import re

def isRealRoom(name, checksum):
    if len(checksum) != 5:
        raise Exception
    totals = defaultdict(int)
    for c in name:
        if c != '-':
            totals[c] += 1
    pairs = zip(totals.keys(), totals.values())
    alphaPairs = sorted(pairs, key=itemgetter(0))
    freqPairs = sorted(alphaPairs, key=itemgetter(1), reverse=True)
    genCheckSum = ''
    for a, b in freqPairs:
        genCheckSum += a
    return genCheckSum[:5] == checksum

def main():
    f = open('input.txt', 'r')
    sectorSum = 0
    for line in f:
        room, metadata = line.rsplit('-', 1)
        match = re.search(r'(\d+)\[(.{5})\]', metadata)
        sector = int(match.group(1))
        checksum = match.group(2)
        if(isRealRoom(room, checksum)):
            sectorSum += sector
    print(sectorSum)

if __name__ == "__main__":
    main()
