#!/usr/bin/env python3
import binascii
import os
import sys
from math import ceil


def block_print():
    sys.stdout = open(os.devnull, 'w')


def enable_print():
    sys.stdout = sys.__stdout__


def print_split_blocks_b64(text):
    print(b'|'.join([binascii.b2a_base64(text)[16*i:16*i+16] for i in range(0, ceil(len(text)/16))]))


def print_split_blocks_hex(text):
    print(b'|'.join([binascii.b2a_hex(text)[32*i:32*i+32] for i in range(0, ceil(len(text)/16))]).decode())


def print_split_blocks(text):
    print(b'|'.join([text[16*i:16*i+16] for i in range(0, ceil(len(text)/16))]))


def get_index(block_n, char_id):
    return block_n * 16 + char_id


def split_blocks(text):
    return [text[i:i+16] for i in range(0, len(text), 16)]


def clear():
    os.system('cls' if os.name == 'nt' else 'clear')
