import random

from challenge11 import random_string
from challenge18 import aes_ctr_crypt
from challenge3 import compute_score as compute_monogram_score
from util import *


def aes_ctr_enc_lines(filename):
    ciphertexts = []
    key = random_string(16)
    # Original challenge set this to 0. But that's boring.
    nonce = random.randint(4294967296, 9223372036854775807)
    with open(filename, 'rb') as file:
        for line in file.readlines():
            ciphertexts.append(aes_ctr_crypt(binascii.a2b_base64(line), key, nonce))
    return ciphertexts


def print_plaintexts(plaintexts):
    for plaintext in plaintexts:
        print(plaintext.replace(b'\0', b'-').decode())


def update_plaintext(pt_idx, char_idx, new_char, plaintexts, ciphertexts):
    for i, plaintext in enumerate(plaintexts):
        if char_idx >= len(ciphertexts[i]):
            continue
        plaintext[char_idx] = ord(new_char) ^ ciphertexts[pt_idx][char_idx] ^ ciphertexts[i][char_idx]
        plaintexts[i] = plaintext


def compute_bigram_score(plaintexts, char_idx):
    bigram_frequencies = {
        b'TH': .0271, b'EN': .0113, b'NG': .0089,
        b'HE': .0233, b'AT': .0112, b'AL': .0088,
        b'IN': .0203, b'ED': .0108, b'IT': .0088,
        b'ER': .0178, b'ND': .0107, b'AS': .0087,
        b'AN': .0161, b'TO': .0107, b'IS': .0086,
        b'RE': .0141, b'OR': .0106, b'HA': .0083,
        b'ES': .0132, b'EA': .0100, b'ET': .0076,
        b'ON': .0132, b'TI': .0099, b'SE': .0073,
        b'ST': .0125, b'AR': .0098, b'OU': .0072,
        b'NT': .0117, b'TE': .0098, b'OF': .0071
    }
    score = 0
    for plaintext in plaintexts:
        if char_idx >= len(plaintext):
            continue
        bigram = plaintext[char_idx - 1:char_idx].upper()
        if bytes(bigram) in bigram_frequencies:
            score += bigram_frequencies[bigram]

    return score


def compute_trigram_score(plaintexts, char_idx):
    trigram_frequencies = {
        b'THE': .0181, b'ERE': .0031, b'HES': .0024,
        b'AND': .0073, b'TIO': .0031, b'VER': .0024,
        b'ING': .0072, b'TER': .0030, b'HIS': .0024,
        b'ENT': .0042, b'EST': .0028, b'OFT': .0022,
        b'ION': .0042, b'ERS': .0028, b'ITH': .0021,
        b'HER': .0036, b'ATI': .0026, b'FTH': .0021,
        b'FOR': .0034, b'HAT': .0026, b'STH': .0021,
        b'THA': .0033, b'ATE': .0025, b'OTH': .0021,
        b'NTH': .0033, b'ALL': .0025, b'RES': .0021,
        b'INT': .0032, b'ETH': .0024, b'ONT': .0020,
    }
    score = 0
    for plaintext in plaintexts:
        if char_idx >= len(plaintext):
            continue
        trigram = plaintext[char_idx - 2:char_idx].upper()
        if bytes(trigram) in trigram_frequencies:
            score += trigram_frequencies[trigram]
    return score


def main():
    clear()
    ciphertexts = aes_ctr_enc_lines('challenge19_data.txt')
    plaintexts = [bytearray(b'\0' * len(ciphertext)) for ciphertext in ciphertexts]
    # Plan is to guess a plaintext byte. We can use this to calculate the the keystream byte.
    # Then, we can calculate all the other plaintext bytes using this keystream bytes.
    # Remove any plaintexts that are non ascii printable (not in range 0x20-0x7F)
    # keystream = bytearray([0]*len(max(ciphertexts, key=len)))
    # ciphertexts = sorted(ciphertexts, key=len)[::-1]
    # plaintexts = sorted(plaintexts, key=len)[::-1]
    longest_plaintext_index = [idx for idx, s in enumerate(plaintexts) if len(s) == len(max(plaintexts, key = len))][0]
    for char_idx in range(len(plaintexts[longest_plaintext_index])):
        best_score = float('-inf')
        best_char = 0
        for i in range(0x20, 0x7F):
            update_plaintext(longest_plaintext_index, char_idx, chr(i), plaintexts, ciphertexts)
            monogram_score_input = bytearray()
            for plaintext in plaintexts:
                if char_idx >= len(plaintext):
                    continue
                monogram_score_input.append(plaintext[char_idx])
            score = compute_monogram_score(monogram_score_input) + \
                    20 * compute_bigram_score(plaintexts, char_idx) + \
                    100 * compute_trigram_score(plaintexts, char_idx)
            if score > best_score:
                best_score = score
                best_char = i
            print_plaintexts(plaintexts)
            clear()
        update_plaintext(longest_plaintext_index, char_idx, chr(best_char), plaintexts, ciphertexts)
        print_plaintexts(plaintexts)


if __name__ == '__main__':
    main()
