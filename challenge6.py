import binascii
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
    key_size = key_size_dists.pop(min(key_size_dists))
    # Break ciphertexts into blocks of length keysize
    blocks = [b''] * key_size
    i = 0
    # Instead of breaking it into blocks of key_size, then transposing them,
    # we are directly putting them intot th correct string
    while i < len(ciphertext) - key_size:
        for j in range(key_size):
            blocks[j] += bytes([ciphertext[i + j]])
        i += key_size
    for block in blocks:


if __name__ == '__main__':
    ciphertext = ''
    for line in open('challenge6_data.txt').readlines():
        ciphertext += line.strip()
    print(break_repeating_key_xor(binascii.a2b_base64(ciphertext)))