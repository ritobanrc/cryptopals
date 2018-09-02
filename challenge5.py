#!/usr/bin/env python3
import binascii


def encrypt_repeating_key_xor(plaintext, key):
    return bytes(plaintext[i] ^ key[i % len(key)] for i in range(len(plaintext)))


if __name__ == '__main__':
    string = b'''Burning 'em, if you ain't quick and nimble
I go crazy when I hear a cymbal'''
    print(binascii.hexlify(encrypt_repeating_key_xor(string, b"ICE")).decode())
    print('0b3637272a2b2e63622c2e69692a23693a2a3c6324202d623d63343c2a26226324272765272a282b2f20430a652e2c652a3124333a653e2b2027630c692b20283165286326302e27282f')