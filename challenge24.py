#!/usr/bin/env python3

from challenge21 import MersenneTwister
import random
import struct
from challenge2 import fixed_xor

prefix = b'Of course it is happening inside your head, Harry, but why on earth \
should that mean it is not real?'


def crypt_mtr(text, seed):
    mt = MersenneTwister()
    mt.seed_mt(seed)
    keystream = b''.join([struct.pack('I', mt.extract_number())
                          for _ in range(len(text))])
    return fixed_xor(text, keystream, True)


def mtr_oracle(text):
    seed = random.getrandbits(16)
    ciphertext = crypt_mtr(prefix + text, seed)
    return ciphertext


def main():
    plaintext = b'Life before Death. \
                  Strength before Weakness. \
                  Journey before Destination'
    ciphertext = mtr_oracle(plaintext)
    print(ciphertext)
    prefix_length = len(ciphertext) - len(plaintext)
    for i in range(2**16):
        possible = crypt_mtr(ciphertext, i)
        if possible[prefix_length:] == plaintext:
            print(possible.decode())
            return


if __name__ == '__main__':
    main()
