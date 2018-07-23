from challenge11 import random_string
from Crypto.Cipher import AES
from urllib.parse import quote, unquote
from challenge9 import pkcs7padding
from challenge10 import aes_cbc_encrypt, aes_cbc_decrypt
from challenge15 import strip_pkcs7padding
from util import *
from challenge2 import fixed_xor
from struct import pack

random_key = random_string(AES.key_size[0])
random_iv = random_string(AES.key_size[0])


def build_profile(userdata):
    plaintext = ('comment1=cooking%20MCs;userdata=' + quote(userdata) + ';comment2=%20like%20a%20pound%20of%20bacon')
    plaintext = bytearray(plaintext, encoding='utf-8')
    plaintext = pkcs7padding(plaintext)
    ciphertext = aes_cbc_encrypt(plaintext, random_key, random_iv)
    return ciphertext


def authenticate(ciphertext):
    plaintext = aes_cbc_decrypt(ciphertext, random_key, random_iv)
    plaintext = strip_pkcs7padding(plaintext)
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


def modify_ciphertext(ciphertext):
    # if we modify a certain block, it will be xor-ed with the ciphertext in the block after.
    new_ciphertext = bytearray(ciphertext)
    # this gives us the plaintext "comment1=whatever;userdata=hacker;commment2=whatever"
    block_print() # keep stdout clean
    _, plaintext = authenticate(ciphertext)
    enable_print()
    # b'comment1=cooking|%20MCs;userdata=|hacker;comment2=|%20like%20a%20po|und%20of%20bacon'
    # Unchanged          Unchanged        Scrambled        We Control       Unchanged
    to_xor = fixed_xor(plaintext[48:64], b'a;admin=true;ab=')
    to_xor = pack('16B', *to_xor)
    new_ciphertext[32:48] = fixed_xor(new_ciphertext[32:48], to_xor)
    print_split_blocks_hex(ciphertext)
    print_split_blocks_hex(new_ciphertext)
    # we know that the plaintext
    return bytes(new_ciphertext)


def main():
    ciphertext = build_profile('hacker') # this shouldn't work if I wrote the authenticate function correctly
    ciphertext = modify_ciphertext(ciphertext)
    success, plaintext = authenticate(ciphertext)
    print(bytes(plaintext))


if __name__ == '__main__':
    main()
