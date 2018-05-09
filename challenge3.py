import binascii
from collections import Counter
import csv


def load_frequencies(filename):
    reader = csv.reader(open(filename))
    frequencies = {}
    for row in reader:
        frequencies[row[0].lower()] = float(row[1])/100
    return frequencies


def single_byte_xor(hexstr):
    frequencies = load_frequencies('frequencies.csv')
    ciphertext = binascii.unhexlify(hexstr)
    results = {}
    for i in range(0, 128):
        c = chr(i)
        plaintext = bytearray([a ^ b for a, b in zip(ciphertext, [i]*len(ciphertext))])
        if not all(char.isprintable() for char in plaintext.decode()):
            continue
        error = check_error(plaintext.lower(), frequencies)
        if error < 0.8:
            results[error] = plaintext
        #print(c, ": error: ", error, ' plaintext: ', plaintext)
    return results


def check_error(plaintext, frequencies):
    counter = Counter(plaintext)
    total_error = 0
    if sum(chr(char).isalpha() for char in plaintext)/len(plaintext) < .7: # if less than 70% are letters
        total_error += 1
    if sum(chr(char).isspace() for char in plaintext)/len(plaintext) > 0.05:
        total_error -= 0.5
    for char, count in counter.most_common():
        if chr(char) not in frequencies:
            continue
        total_error += abs(float(count)/len(plaintext)-frequencies[chr(char)])
    return total_error


if __name__ == '__main__':
    results = single_byte_xor('1b37373331363f78151b7f2b783431333d78397828372d363c78373e783a393b3736')
    print(results.pop(min(results)).decode())
