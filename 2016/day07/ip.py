'''
--- Day 7: Internet Protocol Version 7 ---

While snooping around the local network of EBHQ, you compile a list of IP addresses (they're IPv7,
of course; IPv6 is much too limited). You'd like to figure out which IPs support TLS
(transport-layer snooping).

An IP supports TLS if it has an Autonomous Bridge Bypass Annotation, or ABBA. An ABBA is any
four-character sequence which consists of a pair of two different characters followed by the
reverse of that pair, such as xyyx or abba. However, the IP also must not have an ABBA within any
hypernet sequences, which are contained by square brackets.

For example:

abba[mnop]qrst supports TLS (abba outside square brackets).
abcd[bddb]xyyx does not support TLS (bddb is within square brackets, even though xyyx is outside
square brackets).
aaaa[qwer]tyui does not support TLS (aaaa is invalid; the interior characters must be different).
ioxxoj[asdfgh]zxcvbn supports TLS (oxxo is outside square brackets, even though it's within a
larger string).
How many IPs in your puzzle input support TLS?
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
        if is_abba(sequence[i:i+4]):
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
