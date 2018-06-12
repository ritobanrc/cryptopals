import random

from Crypto.Cipher import AES

import challenge10
import challenge9


def random_string(length):
    return bytes([random.randint(0, 255) for _ in range(length)])


def encrypt_random(plaintext):
    bytes_to_add = random.randint(5, 10)
    plaintext = challenge9.pkcs7padding(random_string(bytes_to_add) + plaintext + random_string(bytes_to_add))
    ecb = random.randint(0, 1)
    if ecb:
        aes = AES.new(random_string(16))
        ciphertext = aes.encrypt(plaintext)
    else:
        ciphertext = challenge10.aes_cbc_encrypt(plaintext, random_string(16), random_string(16))
    return ciphertext, (ecb == 1)


def guess_ecb(ciphertext):
    blocks = set()
    duplicates = 0
    for i in range(0, len(ciphertext) - 16, 16):
        block = ciphertext[i:i + 16]
        if block in blocks:
            duplicates += 1
        blocks.add(block)
    return duplicates > 0


def main():
    # Challenge 11 Data
    # Accio Deathly Hallows by Hank Green
    # 0 is cbc, 1 is ecb
    plaintext = ''.join(open('challenge11_data.txt').readlines()).encode()
    for i in range(1000):
        ciphertext, ecb = encrypt_random(plaintext)
        guess = guess_ecb(ciphertext)
        if guess != ecb:
            print('Failure')
            return
    print('Success')


if __name__ == '__main__':
    main()
