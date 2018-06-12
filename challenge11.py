import random
import binascii
from Crypto.Cipher import AES
import challenge10
import challenge9


def generate_random_key():
    return bytes([random.randint(0, 255) for _ in range(0,16)])


def encrypt_random(plaintext):
    key = generate_random_key()
    c = random.randint(5,10)
    plaintext = bytes([random.randint(0, 255) for _ in range(0, c)]) + plaintext \
                + bytes([random.randint(0,255) for _ in range(0, c)])
    ecb = random.randint(0, 1)
    if ecb == 1:
        print('ecb', end='')
        aes = AES.new(key)
        plaintext = challenge9.pkcs7padding(plaintext)
        return aes.encrypt(plaintext), ecb
    else:
        print('cbc', end='')
        return challenge10.aes_cbc_encrypt(plaintext, key, bytes([random.randint(0, 255) for _ in range(16)])), ecb


def detect_ecb_aes(line):
    strings = set()
    duplicates = 0
    block_size = 1
    for i in range(len(line) - block_size):
        s = line[i:i+block_size]
        if strings.__contains__(s):
            duplicates += 1
        else:
            strings.add(s)
    return duplicates


if __name__ == '__main__':
    for i in range(100):
        ciphertext, ecb = encrypt_random(b' Now, have the function choose to encrypt under ECB 1/2 the time, and under '
                                         b'CBC the other half (just use random IVs each time for CBC). Use rand(2) to '
                                         b'decide which to use.Detect the block cipher mode the function is using each '
                                         b'time. You should end up with a piece of code that, pointed at a block box '
                                         b'that might be encrypting ECB or CBC, tells you which one is happening.')
        if detect_ecb_aes(ciphertext) > 0:
            print(binascii.b2a_hex(ciphertext), 'ecb')
        else:
            print(binascii.b2a_hex(ciphertext), 'cbc')
