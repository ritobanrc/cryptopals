#!/usr/bin/env python3
import binascii

from Crypto.Cipher import AES

from challenge11 import random_string
from challenge9 import pkcs7padding, unpad_pkcs7


def create_obj(str):
    kv_pairs = str.split(b'&')
    obj = {}
    for pair_str in kv_pairs:
        k, v = pair_str.split(b'=')
        obj[bytes(k)] = v
    return obj


def profile_for(username):
    username = username.replace('&', '')
    username = username.replace('=', '')
    str = 'email=' + username + '&uid=10&role=user'
    random_key = random_string(16)
    aes = AES.new(random_key)
    return aes.encrypt(pkcs7padding(bytes(str, encoding = 'utf-8'))), random_key


# email=&ui d = 1 0 &
#   1234567891011121314
def decrypt_profile(encrypted_profile, key):
    aes = AES.new(key)
    return create_obj(unpad_pkcs7(aes.decrypt(bytes(encrypted_profile))))


def main():
    ciphertext, random_key = profile_for('ab')
    print('Ciphertext: ', len(ciphertext))
    print('Random Key: ', binascii.b2a_hex(random_key))
    # insert attack here
    ciphertext = bytearray(ciphertext)
    aes = AES.new(random_key)
    ciphertext[16:32] = aes.encrypt(pkcs7padding(b'role=admin'))
    print('Plaintext: ', decrypt_profile(ciphertext, random_key))


if __name__ == '__main__':
    main()
