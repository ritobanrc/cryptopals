#!/usr/bin/env python3
import binascii

from Crypto.Cipher import AES

import challenge11
import challenge9

random_key = challenge11.random_string(AES.block_size)


def encrypt_oracle(plaintext):
    to_append = binascii.a2b_base64('Um9sbGluJyBpbiBteSA1LjAKV2l0aCBteSByYWctdG9wIGRvd24gc28gbXkg'\
                                    'aGFpciBjYW4gYmxvdwpUaGUgZ2lybGllcyBvbiBzdGFuZGJ5IHdhdmluZyBq'\
                                    'dXN0IHRvIHNheSBoaQpEaWQgeW91IHN0b3A/IE5vLCBJIGp1c3QgZHJvdmUg'\
                                    'YnkK')
    global random_key
    aes = AES.new(random_key)
    ciphertext = aes.encrypt(challenge9.pkcs7padding(plaintext + to_append))
    return ciphertext


def guess_block_size(oracle):
    last_block_size = 0
    this_block_size = 0
    length = 1
    while last_block_size == 0 or this_block_size == last_block_size:
        last_block_size = this_block_size
        this_block_size = len(oracle(b'A' * length))
        length += 1
    return this_block_size - last_block_size


def decrypt_block(oracle, block_size, prevs):
    # we need to find the appended text 1 block at a time. Let's start with the first block.
    known = bytearray(bytes(1) * block_size)
    for i in range(0, block_size):
        short = (b'=' * (block_size - i - 1))
        short_encrypted = oracle(bytes(short))
        # print('i: ', i, ' ', binascii.hexlify(short_encrypted[:(len(prevs)+block_size)]), '\n', short)
        for x in range(255):
            plaintext = bytearray()
            plaintext += short
            plaintext += prevs
            plaintext += known[0:i]
            plaintext.append(x)
            ciphertext = oracle(bytes(plaintext))
            # print(plaintext, ': ', binascii.hexlify(ciphertext[:(len(prevs)+block_size)]))

            if ciphertext[len(prevs):(len(prevs) + block_size)] == short_encrypted[len(prevs):(len(prevs) + block_size)]:
                known[i] = x
                continue
    return bytes(known)


def main():
    # plaintext = ''.join(open('challenge12_data.txt').readlines()).encode()
    guessed_block_size = guess_block_size(encrypt_oracle)
    guessed_ecb = challenge11.guess_ecb(encrypt_oracle(b'YELLOW SUBMARINEYELLOW SUBMARINE'))
    print('Block size: ', guessed_block_size)
    print('ECB: ', guessed_ecb)
    prevs = bytearray()
    block_n = 0
    for i in range(9):
        prevs += decrypt_block(encrypt_oracle, guessed_block_size, prevs)
        block_n += 1
    print(prevs.decode())


if __name__ == '__main__':
    main()
