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


def main():
    # plaintext = ''.join(open('challenge12_data.txt').readlines()).encode()
    guessed_block_size = guess_block_size(encrypt_oracle)
    guessed_ecb = challenge11.guess_ecb(encrypt_oracle(b'YELLOW SUBMARINEYELLOW SUBMARINE'))
    print('Block size: ', guessed_block_size)
    print('ECB: ', guessed_ecb)


if __name__ == '__main__':
    main()