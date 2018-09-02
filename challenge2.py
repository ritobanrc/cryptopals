#!/usr/bin/env python3
"""
Fixed XOR
"""

import warnings
import binascii


def fixed_xor(buf1, buf2, ignore_warnings=False):
    if len(buf1) != len(buf2) and not ignore_warnings:
        warnings.warn('fixed_xor - buf1 and buf2 should be of equal length')
    return bytearray([a ^ b for a, b, in zip(buf1, buf2)])


if __name__ == '__main__':
    hexstr1 = '1c0111001f010100061a024b53535009181c'
    hexstr2 = '686974207468652062756c6c277320657965'
    b1 = binascii.a2b_hex(hexstr1)
    b2 = binascii.a2b_hex(hexstr2)
    print(binascii.hexlify(fixed_xor(b1, b2)).decode())
