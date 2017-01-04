'''
--- Day 7: Internet Protocol Version 7 ---

--- Part Two ---

You would also like to know which IPs support SSL (super-secret listening).

An IP supports SSL if it has an Area-Broadcast Accessor, or ABA, anywhere in the supernet sequences
(outside any square bracketed sections), and a corresponding Byte Allocation Block, or BAB,
anywhere in the hypernet sequences. An ABA is any three-character sequence which consists of the
same character twice with a different character between them, such as xyx or aba. A corresponding
BAB is the same characters but in reversed positions: yxy and bab, respectively.

For example:

aba[bab]xyz supports SSL (aba outside square brackets with corresponding bab within square
brackets).
xyx[xyx]xyx does not support SSL (xyx, but no corresponding yxy).
aaa[kek]eke supports SSL (eke in supernet with corresponding kek in hypernet; the aaa sequence is
not related, because the interior character must be different).
zazbz[bzb]cdb supports SSL (zaz has no corresponding aza, but zbz has a corresponding bzb, even
though zaz and zbz overlap).
How many IPs in your puzzle input support SSL?
'''

import re


def is_abba(abba_str):
    """Returns true if 4 character string consists of a pair of two different characters followed
    by the reverse of that pair"""
    if len(abba_str) != 4:
        raise Exception
    return abba_str[0] == abba_str[3] and abba_str[1] == abba_str[2] and abba_str[0] != abba_str[1]


def contains_abba(sequence):
    """Returns true if sequence contains at least one ABBA"""
    # TODO: figure out a more Python-esque way to do this
    for i in range(len(sequence) - 3):
        if is_abba(sequence[i:i + 4]):
            return True
    return False


def supports_tls(ip_string):
    """Returns true if ip supports TLS"""
    hypers = re.findall(r'\[([a-z]+)\]', ip_string)
    for h in hypers:
        if contains_abba(h):
            return False
        # remove the hypertexts from the IP for easier splitting later
        ip_string = ip_string.replace(h, '')
    normals = ip_string.split('[]')
    for n in normals:
        if contains_abba(n):
            return True
    return False

def supports_ssl(ip_string):
    """Returns true if ip supports SSL"""
    pass

def main():
    """Execution of solution"""
    count = 0
    with open("input.txt") as input_file:
        for line in input_file:
            if supports_tls(line):
                count = count + 1
    print(count)

if __name__ == "__main__":
    main()
