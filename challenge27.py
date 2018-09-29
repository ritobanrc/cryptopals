#!/usr/bin/env python3

from challenge11 import random_string
from urllib.parse import quote, unquote
from challenge9 import pkcs7padding
from challenge10 import aes_cbc_encrypt, aes_cbc_decrypt
from challenge15 import strip_pkcs7padding
from challenge2 import fixed_xor
from util import *


random_key = random_string(16)


def build_profile(userdata):
    plaintext = ('comment1=Life%20before%20Death;userdata=' + quote(userdata) +
                 ';comment2=Strength%20before%20Weakness\nJourney%20Before%20Destination')
    plaintext = bytearray(plaintext, encoding='utf-8')
    plaintext = pkcs7padding(plaintext)
    ciphertext = aes_cbc_encrypt(plaintext, random_key, random_key)
    return ciphertext


def authenticate(ciphertext):
    plaintext = aes_cbc_decrypt(ciphertext, random_key, random_key)
    plaintext = strip_pkcs7padding(plaintext)
    if any(c > 127 for c in plaintext):
        return False, plaintext
    info_dict = {}
    for pair in plaintext.split(b';'):
        k, v = pair.split(b'=')
        info_dict[bytes(unquote(k.decode(errors='ignore')), encoding='utf-8')] = \
                 bytes(unquote(v.decode(errors='ignore')), encoding='utf-8')
    if b'admin' in info_dict and info_dict[b'admin'] == b'true':
        print('Logged in as admin. ')
        return True, plaintext
    else:
        print('Logged in as regular user')
        return False, plaintext


def main():
    enc_profile = build_profile('Szeth')
    # print_split_blocks_hex(profile)
    new_ciphertext = bytes(enc_profile[0:16] + bytearray([0]*16) + enc_profile[0:16] +
                           enc_profile[48:])
    # print_split_blocks_hex(new_ciphertext)
    success, new_plaintext = authenticate(new_ciphertext)
    # print_split_blocks(new_plaintext)
    key = bytes(fixed_xor(new_plaintext[0:16], new_plaintext[32:48]))
    # print(key)
    profile = strip_pkcs7padding(aes_cbc_decrypt(enc_profile, key, key)) + \
                                 b';admin=true'
    new_enc_profile = aes_cbc_encrypt(pkcs7padding(profile), key, key)
    success, plaintext = authenticate(new_enc_profile)
    print(plaintext.decode())


if __name__ == '__main__':
    main()
