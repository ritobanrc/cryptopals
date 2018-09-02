#!/usr/bin/env python3
import binascii

import challenge3


def import_file(file):
    data = []
    with open(file, 'r') as f:
        for line in f:
            data.append(binascii.unhexlify(line.strip()))
    return data


def detect_single_byte_xor(lines):
    results = {}
    for line in lines:
        decrypted = challenge3.single_byte_xor(line)
        results[decrypted[0]] = decrypted[1]
        # print(decrypted)
    best = max(results)
    return best, results[best]


if __name__ == '__main__':
    print(detect_single_byte_xor(import_file('challenge4_data.txt')))
