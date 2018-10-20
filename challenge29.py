#!/usr/bin/env python3
import struct
from challenge26 import build_profile, authenticate


def pad(message):
    pad = b'\x80' + b'\x00' * ((56 - ((len(message) * 8) + 1) % 64) % 64) + struct.pack(b'>Q', len(message) * 8)
    print(pad)


def main():
    ciphertext = build_profile('hackerman')
    authenticate(ciphertext)


if __name__ == '__main__':
    main()
