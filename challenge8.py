#!/usr/bin/env python3
import binascii
from Crypto.Cipher import AES


def detect_ecb_aes(line):
    strings = set()
    duplicates = 0
    for i in range(len(line) - 16):
        s = line[i:i+16]
        if strings.__contains__(s):
            duplicates += 1
        else:
            strings.add(s)
    return duplicates


if __name__ == '__main__':
    for line in open('challenge8_data.txt').readlines():
        dupicates = detect_ecb_aes(binascii.a2b_hex(line.strip()))
        if dupicates > 0:
            print(line)