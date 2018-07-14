import binascii

from Crypto.Cipher import AES

import challenge11
import challenge9

from random import randint, seed

from math import floor




def encrypt_oracle(plaintext):
    to_append = binascii.a2b_base64('VGhyZWUgUmluZ3MgZm9yIHRoZSBFbHZlbi1raW5ncyB1bmRlciB0aGUgc2t5LA0KU2V2ZW4gZm9y' +
                                    'IHRoZSBEd2FyZi1sb3JkcyBpbiB0aGVpciBoYWxscyBvZiBzdG9uZSwNCk5pbmUgZm9yIE1vcnRh' +
                                    'bCBNZW4gZG9vbWVkIHRvIGRpZSwNCk9uZSBmb3IgdGhlIERhcmsgTG9yZCBvbiBoaXMgZGFyayB0' +
                                    'aHJvbmUNCkluIHRoZSBMYW5kIG9mIE1vcmRvciB3aGVyZSB0aGUgU2hhZG93cyBsaWUuDQpPbmUg' +
                                    'UmluZyB0byBydWxlIHRoZW0gYWxsLCBPbmUgUmluZyB0byBmaW5kIHRoZW0sDQpPbmUgUmluZyB0' +
                                    'byBicmluZyB0aGVtIGFsbCwgYW5kIGluIHRoZSBkYXJrbmVzcyBiaW5kIHRoZW0sDQpJbiB0aGUg' +
                                    'TGFuZCBvZiBNb3Jkb3Igd2hlcmUgdGhlIFNoYWRvd3MgbGllLg==')
    global random_key
    aes = AES.new(random_key)
    ciphertext = aes.encrypt(challenge9.pkcs7padding(to_prepend + plaintext + to_append))
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


def decrypt_block(oracle, block_size, prevs, offset):
    # we need to find the appended text 1 block at a time. Let's start with the first block.
    known = bytearray(bytes(1) * block_size)
    for i in range(0, block_size):
        short = b'?' * offset[1] + (b'=' * (block_size - i - 1))
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

            if ciphertext[offset[0] + len(prevs):(offset[0] + len(prevs) + block_size)] == \
                    short_encrypted[offset[0] + len(prevs):(offset[0] + len(prevs) + block_size)]:
                known[i] = x
                continue
    return bytes(known)


def guess_offset(oracle):
    ciphertexts = []
    for i in range(0, AES.block_size+1):
        ciphertext = oracle(b'A'*i)
        blocks = [ciphertext[i:i+AES.block_size] for i in range(floor(len(ciphertext)/AES.block_size))]
        ciphertexts.append(blocks)
    offset = 0

    for i in range(0, len(ciphertexts[0])):
        if ciphertexts[0][i] != ciphertexts[1][i]:
            offset += AES.block_size * i
            first_non_eq_block = i
            break
    q = 16
    for i in range(0, len(ciphertexts) - 1):
        if ciphertexts[i][first_non_eq_block] == ciphertexts[i+1][first_non_eq_block]:
            q = i
            break
    offset += (AES.block_size - q)
    return offset, q


def main():
    global random_key
    global to_prepend
    random_key = challenge11.random_string(AES.block_size)
    to_prepend = challenge11.random_string(randint(1, 32))

    guessed_block_size = guess_block_size(encrypt_oracle)
    guessed_offset = guess_offset(encrypt_oracle)
    guessed_ecb = challenge11.guess_ecb(encrypt_oracle(b'?' * guessed_offset[1] + b'YELLOW SUBMARINEYELLOW SUBMARINE'))
    # print('Block size: ', guessed_block_size)
    # print('ECB: ', guessed_ecb)
    # print('Offset: ', guessed_offset)
    prevs = bytearray()
    block_n = 0
    for i in range(24):
        prevs += decrypt_block(encrypt_oracle, guessed_block_size, prevs, guessed_offset)
        block_n += 1
    #print(prevs)
    correct = bytearray(b'Three Rings for the Elven-kings under the sky,\r\nSeven for the Dwarf-lords in their halls'
                        b' of stone,\r\nNine for Mortal Men doomed to die,\r\nOne for the Dark Lord on his dark throne'
                        b'\r\nIn the Land of Mordor where the Shadows lie.\r\nOne Ring to rule them all, One Ring to'
                        b' find them,\r\nOne Ring to bring them all, and in the darkness bind them,\r\nIn the Land of '
                        b'Mordor where the Shadows lie.\x01\x00\x00\x00\x00')
    if prevs != correct:
        print('Error at: ', guessed_offset)


if __name__ == '__main__':
    seed(0)
    for i in range(100):
        main()
