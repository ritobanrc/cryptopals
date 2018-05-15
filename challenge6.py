import binascii
from math import inf

import challenge3


def hamming_dist(b1, b2):
    return sum([bin((a ^ b)).count('1') for a,b in zip(b1, b2)])


def break_repeating_key_xor(ciphertext):
    key_size_dists = {}
    # Guess Keysize
    for key_size in range(2, 41):
        # technically, we should look at the entire ciphertext.
        # however, for the sake of efficiency, we are only looking at the first 4 blocks
        block1 = ciphertext[0:key_size]
        block2 = ciphertext[key_size:key_size*2]
        block3 = ciphertext[key_size * 2:key_size * 3]
        block4 = ciphertext[key_size * 3:key_size * 4]
        total_dist = hamming_dist(block1, block2) + hamming_dist(block2, block3) + hamming_dist(block3, block4)
        total_dist /= (key_size * 3) # we normalize the distance by dividing by the key_size and average the distances
        key_size_dists[total_dist] = key_size
    # print(key_size_dists)
    key_sizes_to_test = [key_size_dists.pop(min(key_size_dists)) for _ in range(5)]
    # print(key_sizes_to_test)
    key_sizes_to_test = [29]
    best_key_size = -1
    best_score = -inf
    best_plaintext = bytearray()
    for key_size in key_sizes_to_test:
        # Break ciphertext into keysize blocks of length n
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
        # new_plaintext = bytearray([i for sub in list(itertools.zip_longest(*plaintext)) for i in sub])

        # print('\nKey Size: ', key_size, ' Key Size Score: ', key_size_score)
        if key_size_score > best_score:
            best_key_size = key_size
            best_score = key_size_score
            best_plaintext = new_plaintext
    return best_key_size, best_score, best_plaintext


if __name__ == '__main__':
    ciphertext = ''
    for line in open('challenge6_data.txt').readlines():
        ciphertext += line.strip()
    print(break_repeating_key_xor(binascii.a2b_base64(ciphertext))[2].decode())
