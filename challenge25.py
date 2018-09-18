#!/usr/bin/env python3

import binascii
import challenge7
from challenge11 import random_string
from challenge18 import aes_ctr_crypt
import random

key = random_string(16)
nonce = random.getrandbits(63)


def edit(ciphertext, offset, newtext):
    plaintext = bytearray(aes_ctr_crypt(ciphertext, key, nonce))
    plaintext[offset:offset + len(newtext)] = newtext
    return aes_ctr_crypt(plaintext, key, nonce)


def oracle():
    file_bytes = []
    for line in open('challenge25_data.txt').readlines():
        line_bytes = binascii.a2b_base64(line.strip())
        file_bytes.append(line_bytes)
    ciphertext = b''.join(file_bytes)
    plaintext = challenge7.decrypt_aes(ciphertext, b'YELLOW SUBMARINE')
    ciphertext = aes_ctr_crypt(plaintext, key, nonce)
    return ciphertext


def main():
    ciphertext = oracle()
    print(edit(ciphertext, 0, ciphertext).decode())


if __name__ == '__main__':
    main()
