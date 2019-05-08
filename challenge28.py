#!/usr/bin/env python3

from sha1 import sha1
from challenge11 import random_string

plaintext = (b'United, new beginnings sing: "Defying\n'
             b'truth, love. Truth defy!" Sing beginnings, new\n'
             b'unity. ')

def secret_prefix_mac(message, key):
    return sha1(key + message)


def main():
    mac = secret_prefix_mac(plaintext, random_string(16))
    print(mac)
    mac2 = secret_prefix_mac(b'Alight, winds approach deadly approaching winds alight.', random_string(16))
    print(mac2)


if __name__ == '__main__':
    main()
