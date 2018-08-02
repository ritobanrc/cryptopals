from Crypto.Cipher import AES
from struct import pack
from util import *
from challenge2 import fixed_xor
import binascii


def aes_ctr_crypt(text, key, nonce):
    othertext = bytearray()
    counter = 0
    aes = AES.new(key)
    for block in split_blocks(text):
        encrypted = aes.encrypt(pack('<qq', nonce, counter))
        othertext += fixed_xor(encrypted[:len(block)], block)
        counter += 1
    return bytes(othertext)


def main():
    hex_ciphertext = b'L77na/nrFsKvynd6HzOoG7GHTLXsTVu9qvY/2syLXzhPweyyMTJULu/6/kXX0KSvoOLSFQ=='
    plaintext = aes_ctr_crypt(binascii.a2b_base64(hex_ciphertext), b'YELLOW SUBMARINE', 0)
    print(plaintext.decode())


if __name__ == '__main__':
    main()