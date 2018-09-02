#!/usr/bin/env python3
import binascii
import random
from Crypto.Cipher import AES
from challenge11 import random_string
from challenge10 import aes_cbc_encrypt, aes_cbc_decrypt
from util import *
from challenge15 import strip_pkcs7padding

possible_b64_plaintexts = [
    'MDAwMDAwTm93IHRoYXQgdGhlIHBhcnR5IGlzIGp1bXBpbmc=',
    'MDAwMDAxV2l0aCB0aGUgYmFzcyBraWNrZWQgaW4gYW5kIHRoZSBWZWdhJ3MgYXJlIHB1bXBpbic=',
    'MDAwMDAyUXVpY2sgdG8gdGhlIHBvaW50LCB0byB0aGUgcG9pbnQsIG5vIGZha2luZw==',
    'MDAwMDAzQ29va2luZyBNQydzIGxpa2UgYSBwb3VuZCBvZiBiYWNvbg==',
    'MDAwMDA0QnVybmluZyAnZW0sIGlmIHlvdSBhaW4ndCBxdWljayBhbmQgbmltYmxl',
    'MDAwMDA1SSBnbyBjcmF6eSB3aGVuIEkgaGVhciBhIGN5bWJhbA==',
    'MDAwMDA2QW5kIGEgaGlnaCBoYXQgd2l0aCBhIHNvdXBlZCB1cCB0ZW1wbw==',
    'MDAwMDA3SSdtIG9uIGEgcm9sbCwgaXQncyB0aW1lIHRvIGdvIHNvbG8=',
    'MDAwMDA4b2xsaW4nIGluIG15IGZpdmUgcG9pbnQgb2g=',
    'MDAwMDA5aXRoIG15IHJhZy10b3AgZG93biBzbyBteSBoYWlyIGNhbiBibG93]']

random_key = random_string(AES.key_size[0])


def encrypt_cbc_random():
    plaintext = binascii.a2b_base64(random.choice(possible_b64_plaintexts))
    iv = random_string(AES.block_size)
    return aes_cbc_encrypt(plaintext, random_key, iv), iv


def check_cbc_padding_random(ciphertext, iv):
    ciphertext = bytes(ciphertext)
    iv = bytes(iv)
    try:
        plaintext = aes_cbc_decrypt(ciphertext, random_key, iv)
        return True
    except ValueError:
        return False


def cbc_padding_oracle(c1, c2):
    assert (len(c1) == len(c2) == AES.block_size)
    p2 = bytearray([0] * AES.block_size)
    chosen_c1 = bytearray(random_string(AES.block_size))
    # note that padding is the amount of padding this iteration is attempting to achieve. -padding is the byte being set
    for padding in range(1, AES.block_size + 1):
        for c in range(256):
            chosen_c1[-padding] = c
            if check_cbc_padding_random(c2, chosen_c1):
                break
        p2[-padding] = chosen_c1[-padding] ^ padding ^ c1[-padding]
        for i in range(1, padding + 1):
            chosen_c1[-i] = chosen_c1[-i] ^ padding ^ (padding + 1)

    return p2


def main():
    ciphertext, iv = encrypt_cbc_random()
    plaintext = bytearray([0]*len(ciphertext))
    plaintext[get_index(0, 0):get_index(1, 0)] = cbc_padding_oracle(iv, ciphertext[get_index(0, 0):get_index(1, 0)])
    for i in range(1, len(ciphertext)//AES.block_size):
        plaintext[get_index(i, 0):get_index(i+1, 0)] = cbc_padding_oracle(
            ciphertext[get_index(i-1, 0):get_index(i, 0)],
            ciphertext[get_index(i, 0):get_index(i+1, 0)]
        )
    print(strip_pkcs7padding(plaintext).decode())


if __name__ == '__main__':
    for i in range(20):
        main()
