"""
Fixed XOR
"""

import sys
import binascii


def fixed_xor(buf1, buf2):
    if len(buf1) != len(buf2):
        print("fixed_xor - buf1 and buf2 must be of equal length", file=sys.stderr)
    return bytearray([a ^ b for a, b, in zip(buf1, buf2)])


if __name__ == '__main__':
    hexstr1 = '1c0111001f010100061a024b53535009181c'
    hexstr2 = '686974207468652062756c6c277320657965'
    b1 = binascii.a2b_hex(hexstr1)
    b2 = binascii.a2b_hex(hexstr2)
    print(binascii.hexlify(fixed_xor(b1, b2)).decode())
