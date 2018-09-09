#!/usr/bin/env python3

from challenge21 import MersenneTwister
import random


# from util import print_split_n

(u, d) = (11, 0xFFFFFFFF)
(s, b) = (7, 0x9D2C5680)
(t, c) = (15, 0xEFC60000)
f = 1812433253
last = 18  # This was originally l, but syntastic got triggered


def untemper(number):
    # do stuff here
    # the last thing we do is xor y with the 14 leftmost bits of y
    # therefore, the 18 leftmost bits of number were unchanged
    # Now, we know the 18 leftmost bits,
    #   and y was xor-red with the 14 leftmost bits,
    # we can xor the 14 rightmost bits with the
    #   14 leftmost bits to get the entire thing
    # print('original: ', number)
    number ^= (number >> last)
    number ^= (number << t) & c
    number ^= (number << 7) & 0x1680
    number ^= (number << 7) & 0xC4000
    number ^= (number << 7) & 0xD200000
    number ^= (number << 7) & 0x90000000
    number ^= (number >> 11) & 0xFFC00000
    number ^= (number >> 11) & 0x3FF800
    number ^= (number >> 11) & 0x7FF
    # y = number
    # print("Undo Complete")
    # y = y ^ ((y >> u) & d)
    # print(y)
    # y = y ^ ((y << s) & b)
    # print(y)
    # y = y ^ ((y << t) & c)
    # print(y)
    # y = y ^ (y >> last)
    # print(y)
    return number


def main():
    rng = MersenneTwister()
    seed = random.getrandbits(32)
    rng.seed_mt(seed)
    numbers = [rng.extract_number() for _ in range(624)]
    MT = [untemper(numbers[i]) for i in range(624)]
    spliced = MersenneTwister()
    spliced.seed_mt(seed)
    spliced.MT = MT

    for _ in range(624*2):
        expected = rng.extract_number()
        predicted = spliced.extract_number()
        assert expected == predicted
        print(expected, predicted)


if __name__ == '__main__':
    main()
