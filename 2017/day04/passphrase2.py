"""
from: http://adventofcode.com/2017/day/4

--- Part Two ---
For added security, yet another system policy has been put in place. Now, a valid passphrase must
contain no two words that are anagrams of each other - that is, a passphrase is invalid if any
word's letters can be rearranged to form any other word in the passphrase.
For example:
abcde fghij is a valid passphrase.
abcde xyz ecdab is not valid - the letters from the third word can be rearranged to form the first
word.
a ab abc abd abf abj is a valid passphrase, because all letters need to be used when forming another
word.
iiii oiii ooii oooi oooo is valid.
oiii ioii iioi iiio is not valid - any of these words can be rearranged to form any other word.
Under this new system policy, how many passphrases are valid?

"""

def main():
    """Solve the problem!"""
    valid_count = 0
    with open("input.txt") as input_file:
        for line in input_file:
            valid = True
            used_words = {}
            words = line.split()
            for word in words:
                ordered_word = ''.join(sorted(word))
                if ordered_word in used_words:
                    valid = False
                else:
                    used_words[ordered_word] = 1
            if valid:
                valid_count = valid_count + 1
    print(valid_count)

if __name__ == "__main__":
    main()
