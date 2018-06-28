import binascii

from Crypto.Cipher import AES

import challenge11
import challenge9

from random import randint

random_key = challenge11.random_string(AES.block_size)
to_prepend = challenge11.random_string(randint(1, 32))


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

            if ciphertext[offset + len(prevs):(offset + len(prevs) + block_size)] == \
                    short_encrypted[offset + len(prevs):(offset + len(prevs) + block_size)]:
                known[i] = x
                continue
    return bytes(known)


def guess_offset(oracle):
    empty_input = oracle(b'')
    one_char = oracle(b'A')
    offset_block_start = [i for i in range(len(empty_input)) if empty_input[i] == one_char[i]]
    # if they were equal for less than a contiguous block, ignore. it's a conincidence.
    # find the last index whose is separated by 1 from the previous (i.e. 13, 14, [15], 94)
    # this+1 is the rounded down length of the prepended text. => l_min
    print(offset_block_start)
    for i in range(0, AES.block_size+1):
        ciphertext = binascii.b2a_hex(oracle(b'A'*i))
        print([ciphertext[i:i + 32] for i in range(0, len(ciphertext), 32)])
    return 16


def main():
    # plaintext = ''.join(open('challenge12_data.txt').readlines()).encode()
    guessed_block_size = guess_block_size(encrypt_oracle)
    guessed_ecb = challenge11.guess_ecb(encrypt_oracle(b'YELLOW SUBMARINEYELLOW SUBMARINE'))
    guessed_offset = guess_offset(encrypt_oracle)
    print('Block size: ', guessed_block_size)
    print('ECB: ', guessed_ecb)
    print('Offset: ', guessed_offset)
    prevs = bytearray()
    block_n = 0
    for i in range(24):
        prevs += decrypt_block(encrypt_oracle, guessed_block_size, prevs, guessed_offset)
        block_n += 1
    print(prevs)


if __name__ == '__main__':
    main()
