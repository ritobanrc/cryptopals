#!/usr/bin/env python3

from challenge2 import fixed_xor
from util import *
from challenge18 import aes_ctr_crypt
from challenge11 import random_string
import random
from urllib.parse import quote, unquote


random_key = random_string(16)
random_nonce = random.getrandbits(16)


def build_profile(userdata):
    plaintext = ('comment1=cooking%20MCs;userdata=' + quote(userdata) +
                 ';comment2=%20like%20a%20pound%20of%20bacon')
    plaintext = bytearray(plaintext, encoding='utf-8')
    ciphertext = aes_ctr_crypt(plaintext, random_key, random_nonce)
    return ciphertext


# TODO: implement this using ctr instead of cbc
def authenticate(ciphertext):
    plaintext = aes_ctr_crypt(ciphertext, random_key, random_nonce)
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


def modify_ciphertext_ctr(ciphertext):
    _, plaintext = authenticate(ciphertext)
    print_split_blocks(plaintext)
    # This is the ciphertext xor-red with the plaintext
    # plaintext = ciphertext ^ keystream
    # ciphertext = plaintext ^ keystream
    # comment1=cooking|%20MCs;userdata=|hacker;comment2=|%20like%20a%20po|und%20of%20bacon 
    # print(len(plaintext), len(ciphertext))
    keystream = fixed_xor(ciphertext, plaintext)
    # print(keystream)
    # print(len(keystream))
    new_plaintext = bytearray(plaintext)
    new_plaintext[32:48] = b'a;admin=true;c2='
    new_plaintext = bytes(new_plaintext)
    new_ciphertext = fixed_xor(new_plaintext, keystream)
    return new_ciphertext


def main():
    ciphertext = build_profile('hacker')
    # print(aes_ctr_crypt(ciphertext, random_key, random_nonce))
    ciphertext = modify_ciphertext_ctr(ciphertext)
    success, plaintext = authenticate(ciphertext)
    print(bytes(plaintext))


if __name__ == '__main__':
    main()
