#!/usr/bin/env python3
import challenge19
import challenge3


def main():
    ciphertexts = challenge19.aes_ctr_enc_lines('challenge20_data.txt')

    key_size = len(min(ciphertexts, key = len))
    ciphertexts = [ciphertext[:key_size] for ciphertext in ciphertexts]
    ciphertext = b''.join(ciphertexts)
    blocks = [b''] * key_size

    i = 0
    # Instead of breaking it into blocks of key_size, then transposing them,
    # we are directly putting them into the correct string
    while i < len(ciphertext) - key_size:
        for j in range(key_size):
            blocks[j] += bytes([ciphertext[i + j]])
        i += key_size
    plaintext = []
    key_size_score = 0
    for block in blocks:
        # each block contains characters that are spaced out by key_size.
        # now, we rebuild the original string
        plainblock = challenge3.single_byte_xor(block)
        plaintext.append(plainblock[1])
        key_size_score += plainblock[0]

    new_plaintext = b''.join([bytearray([j[i] for j in plaintext]) for i in range(len(plaintext[0]))])
    print(new_plaintext.decode().replace(' / ', '\n'))


if __name__ == '__main__':
    main()
