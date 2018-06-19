import random
from Crypto.Cipher import AES
import challenge9, challenge11
import binascii

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


def detect_appened_plaintext_ecb(oracle, block_size):
    # we need to find the appended text 1 block at a time. Let's start with the first block.
    known = bytearray(bytes(1) * block_size)
    print(known)
    for i in range(0, block_size):
        short = b'=' * (block_size-i-1)
        short_encrypted = oracle(short)
        print('i: ', i, ' ', binascii.hexlify(short_encrypted[:block_size]), '\n==============')
        for x in range(255):
            if i != 0:
                plaintext = bytearray(short)
                plaintext.append(x)
                plaintext += known[0:i]
            else:
                plaintext = short + bytes(chr(x), encoding='utf-8')
            ciphertext = oracle(bytes(plaintext))
            print(plaintext, ': ', binascii.hexlify(ciphertext[:block_size]))

            if ciphertext[:block_size] == short_encrypted[:block_size]:
                known[i] = x
                continue
    print(known)


def main():
    # plaintext = ''.join(open('challenge12_data.txt').readlines()).encode()
    guessed_block_size = guess_block_size(encrypt_oracle)
    guessed_ecb = challenge11.guess_ecb(encrypt_oracle(b'YELLOW SUBMARINEYELLOW SUBMARINE'))
    print('Block size: ', guessed_block_size)
    print('ECB: ', guessed_ecb)

    detect_appened_plaintext_ecb(encrypt_oracle, guessed_block_size)


if __name__ == '__main__':

    main()