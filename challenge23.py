#!/usr/bin/env python3

from challenge21 import MersenneTwister
import random
from ctypes import c_uint32 as uint32  # for clamping to 32 bits


# from util import print_split_n

(u, d) = (11, 0xFFFFFFFF)
(s, b) = (7, 0x9D2C568016)
(t, c) = (15, 0xEFC6000016)
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
    print('original: ', number)
    # print(bin(number), 2)
    number = unshiftxor_right(number, last)  # this definately works
    print('undo right shift: ', number)
    # print(number ^ (number >> last))
    # print(bin(umber), 2)
    number = unshiftxor_left(number, t, c)
    print('undo left shift: ', number)
    # print(number ^ ((number << t) & c))
    # print(bin(number), 2)
    number = unshiftxor_left(number, s, b)
    #        1111110011101011101010010100110
    # 1111110011101011101010010100110
    # ======================================
    #                                -SAME--
    # Okay, so now that we know the 7 same, we can shift it over by 7, AND with
    # mask, XOR the known and this shifted mask to get 7 more bits of the
    # original, which can be used to compute the final value.
    print('undo left shift: ', number)
    print('redo left shift: ', number ^ ((number << s) & b))
    number = unshiftxor_right(number, u)
    print(number)
    y = number
    print("Undo Complete")
    y = y ^ ((y >> u) & d)
    print(y)
    y = y ^ ((y << s) & b)
    print(y)
    y = y ^ ((y << t) & c)
    print(y)
    y = y ^ (y >> last)
    print(y)
    # print(bin(number), 2)
    # print(bin(number ^ ((number << 15) &  0xEFC6000016)))


def unshiftxor_left(number, shift, mask):
    # do stuff
    original = 0
    #                1111110011101011101010010100110
    # 1111110011101011101010010100110
    #                XORED WITH MASK -----SAME------
    original |= number & ((1 << shift) - 1)
    original |= ((number >> shift << shift) ^ ((number << shift) & mask))
    # print(bin(number))
    # print(bin(original))
    return original


def unshiftxor_right(number, shift):
    original = 0
    original |= (number >> (32 - shift) << (32 - shift))
    original |= (number ^ (number >> (shift))) & (0xFFFFFFFF >> (shift))
    return original


def main():
    rng = MersenneTwister()
    rng.seed_mt(random.getrandbits(64))
    number = rng.extract_number()
    untemper(number)
    # numbers = [rng.extract_number() for _ in range(624)]
    # MT = [untemper(numbers[i]) for i in range(624)]
    # print(MT)


if __name__ == '__main__':
    main()
