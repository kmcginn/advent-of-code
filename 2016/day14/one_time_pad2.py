""" Solution to Day 14

from: http://adventofcode.com/2016/day/14

--- Part Two ---

Of course, in order to make this process even more secure, you've also implemented key stretching.

Key stretching forces attackers to spend more time generating hashes. Unfortunately, it forces
everyone else to spend more time, too.

To implement key stretching, whenever you generate a hash, before you use it, you first find the
MD5 hash of that hash, then the MD5 hash of that hash, and so on, a total of 2016 additional
hashings. Always use lowercase hexadecimal representations of hashes.

For example, to find the stretched hash for index 0 and salt abc:

Find the MD5 hash of abc0: 577571be4de9dcce85a041ba0410f29f.
Then, find the MD5 hash of that hash: eec80a0c92dc8a0777c619d9bb51e910.
Then, find the MD5 hash of that hash: 16062ce768787384c81fe17a7a60c7e3.
...repeat many times...
Then, find the MD5 hash of that hash: a107ff634856bb300138cac6568c0f24.
So, the stretched hash for index 0 in this situation is a107ff.... In the end, you find the original
hash (one use of MD5), then find the hash-of-the-previous-hash 2016 times, for a total of 2017 uses
of MD5.

The rest of the process remains the same, but now the keys are entirely different. Again for salt
abc:

The first triple (222, at index 5) has no matching 22222 in the next thousand hashes.
The second triple (eee, at index 10) hash a matching eeeee at index 89, and so it is the first key.
Eventually, index 22551 produces the 64th key (triple fff with matching fffff at index 22859.
Given the actual salt in your puzzle input and using 2016 extra MD5 calls of key stretching, what
index now produces your 64th one-time pad key?
"""

import hashlib
import re

class StretchedHasher(object):
    """Class for generating a stretched hash, with internal caching for speed!"""
    def __init__(self):
        self.cache = dict()

    def generate_hash(self, salt):
        """Return the result of hashing the salt with MD5 2017 times"""

        # check for cache hit
        if salt in self.cache.keys():
            return self.cache[salt]

        if len(self.cache.keys()) >= 1000:
            # clean up the salt with the lowest index in the cache to optimize space
            del self.cache[sorted(self.cache.keys(), key=lambda salt: int(re.findall(r'[0-9]+', salt)[0]))[0]]

        stretched_hash = hashlib.md5(str.encode(salt)).hexdigest()
        for i in range(0, 2016):
            stretched_hash = hashlib.md5(str.encode(stretched_hash)).hexdigest()

        # add computed hash to the cache
        self.cache[salt] = stretched_hash

        return stretched_hash

def generates_key(salt, index, hasher):
    """Returns true if the stretched hash of salt and the index contains one character three times
    in a row, and one of the next 1000 stretched hashes with the same salt and an increasing index
    contains the same character five times in a row"""
    starting_hash = hasher.generate_hash(salt + str(index))
    match = re.search(r'([a-z0-9])\1\1', starting_hash)
    if match is None:
        return (False, hasher)
    repeat_target = match[1] + match[1] + match[1] + match[1] + match[1]
    for i in range(index + 1, index + 1001):
        new_hash = hasher.generate_hash(salt + str(i))
        if repeat_target in new_hash:
            return (True, hasher)
    return (False, hasher)


def main():
    """Execution of solution"""
    salt = 'abc'
    index = 0
    key_count = 0
    hasher = StretchedHasher()
    while key_count < 64:
        # print("Checking index " + str(index))
        result = generates_key(salt, index, hasher)
        hasher = result[1]
        if result[0]:
            key_count += 1
        index += 1
    print(index - 1)

if __name__ == "__main__":
    main()
