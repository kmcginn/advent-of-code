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

def recursive_rotate(char, count):
    if count == 0:
        return char
    if char == 'z':
        return recursive_rotate('a', count - 1)
    else:
        return recursive_rotate(chr(ord(char) + 1), count - 1)

def rot_n(message, n):
    if n < 0:
        raise Exception
    n = n % 26
    if n == 0:
        return message
    new_message = ''
    for c in message:
        if c == ' ':
            new_message += ' '
        else:
            new_message += recursive_rotate(c, n)
    return new_message

def main():
    f = open('input.txt', 'r')
    r = open('decoded.txt', 'w')
    sectorSum = 0
    for line in f:
        room, metadata = line.rsplit('-', 1)
        match = re.search(r'(\d+)\[(.{5})\]', metadata)
        sector = int(match.group(1))
        checksum = match.group(2)
        if(isRealRoom(room, checksum)):
            decrypted_name = rot_n(room.replace('-', ' ',), sector)
            s = str(decrypted_name) + ' ' + str(sector) + '\n'
            r.write(s)

main()
