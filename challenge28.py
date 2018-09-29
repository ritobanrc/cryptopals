#!/usr/bin/env python3

from sha1 import sha1
from challenge11 import random_string

key = random_string(16)


def secret_prefix_mac(message):
    return sha1(key + bytes(message, encoding='utf-8'))


def main():
    mac = secret_prefix_mac('United, new beginnings sing: "Defying \
                            truth, love. Truth defy!" Sing beginnings, new unity. ')
    print(mac)
    mac2 = secret_prefix_mac('Alight, winds approach deadly approaching winds alight.')
    print(mac2)


if __name__ == '__main__':
    main()
