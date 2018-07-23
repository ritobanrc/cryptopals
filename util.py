import sys
import os
import binascii
from math import floor


def block_print():
    sys.stdout = open(os.devnull, 'w')


def enable_print():
    sys.stdout = sys.__stdout__


def print_split_blocks_b64(text):
    print(b'|'.join([binascii.b2a_base64(text)[16*i:16*i+16] for i in range(0, floor(len(text)/16))]))


def print_split_blocks_hex(text):
    print(b'|'.join([binascii.b2a_hex(text)[32*i:32*i+32] for i in range(0, floor(len(text)/32))]))


def print_split_blocks(text):
    print(b'|'.join([(text)[16*i:16*i+16] for i in range(0, floor(len(text)/16))]))
