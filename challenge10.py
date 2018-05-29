import binascii
import sys

from Crypto.Cipher import AES

import challenge9


def xor(buf1, buf2):
    if len(buf1) != len(buf2):
        print("fixed_xor - buf1 and buf2 must be of equal length", file = sys.stderr)
    return bytes([a ^ b for a, b, in zip(buf1, buf2)])


def aes_cbc_encrypt(plaintext, key, iv):
    aes = AES.new(key)
    plaintext = challenge9.pkcs7padding(plaintext,
                                        len(plaintext) + (aes.block_size - (len(plaintext) % aes.block_size)))
    prev = iv
    ciphertext = b''
    for block in [plaintext[i:i + aes.block_size] for i in range(0, len(plaintext), aes.block_size)]:
        encrypted = aes.encrypt(xor(block, prev))
        prev = encrypted
        ciphertext += encrypted
    return ciphertext


def aes_cbc_decrypt(ciphertext, key, iv):
    aes = AES.new(key)
    prev = iv
    plaintext = b''
    for block in [ciphertext[i:i + aes.block_size] for i in range(0, len(ciphertext), aes.block_size)]:
        decrypted = xor(aes.decrypt(block), prev)
        plaintext += decrypted
        prev = block
    return challenge9.unpad_pkcs7(plaintext)


if __name__ == '__main__':
    plaintext = b'CBC mode is a block cipher mode that allows us to encrypt irregularly-sized messages, despite the ' \
                b'fact that a block cipher natively only transforms individual blocks. '
    key = b'YELLOW SUBMARINE'
    iv = bytes([0x00] * 16)
    ciphertext = aes_cbc_encrypt(plaintext, key, iv)
    print(binascii.b2a_hex(ciphertext))
    decrypted = aes_cbc_decrypt(ciphertext, key, iv)
    print(decrypted)

    data = b''.join([binascii.a2b_base64(line) for line in open('challenge10_data.txt').readlines()])
    print(aes_cbc_decrypt(data, key, iv))
