"""
Convert hex to base64
"""

import base64
import binascii


def hex_to_base64(hexstr):
    txt = binascii.a2b_hex(hexstr)
    return base64.b64encode(txt)


if __name__ == '__main__':
    hexstr = '49276d206b696c6c696e6720796f757220627261696e206c696b65206120706f69736f6e6f7573206d757368726f6f6d'
    print(hex_to_base64(hexstr).decode())
