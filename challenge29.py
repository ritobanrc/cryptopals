#!/usr/bin/python3
import struct
import random
import binascii
from challenge28 import secret_prefix_mac
from sha1 import sha1

def generate_padding(message):
    original_byte_len = len(message)
    original_bit_len = original_byte_len * 8
    message += b'\x80'
    message += b'\x00' * ((56 - (original_byte_len + 1) % 64) % 64)
    message += struct.pack(b'>Q', original_bit_len)
    return message

data = b'comment1=cooking%20MCs;userdata=foo;comment2=%20like%20a%20pound%20of%20bacon'
with open('/usr/share/dict/words') as f:
    prefix = bytes(random.choice(f.readlines()), encoding='utf8')

def get_mac():
    mac = secret_prefix_mac(data, prefix)
    return mac

def forge_mac(original_message, mac, append):
    h0, h1, h2, h3, h4 = struct.unpack('>IIIII', mac)
    for prefix_length in range(1, 20):
        print(f'------------ PREFIX LENGTH: {prefix_length} --------------')
        to_pad = b'a' * prefix_length  + original_message
        padded = generate_padding(to_pad)
        new_mac = sha1(append, 8*(len(padded) + len(append)), h0, h1, h2, h3, h4)
        new_plaintext = padded[prefix_length:] + append
        if authenticate(new_plaintext, new_mac):
            return new_plaintext, new_mac
    return b'', b''

def authenticate(plaintext, mac, output = True):
    from urllib.parse import quote, unquote
    if secret_prefix_mac(plaintext, prefix) != mac:
        if output: print('MAC Error')
        return False
    info_dict = {}
    for pair in plaintext.split(b';'):
        k, v = pair.split(b'=')
        info_dict[bytes(unquote(k.decode(errors='ignore')), encoding='utf-8')] = \
                 bytes(unquote(v.decode(errors='ignore')), encoding='utf-8')
    if b'admin' in info_dict and info_dict[b'admin'] == b'true':
        if output: print('Logged in as admin. ')
        return True
    else:
        if output: print('Logged in as regular user')
        return False

def main():
    mac = get_mac()
    print('Original MAC: ', binascii.hexlify(mac))
    authenticate(data, mac)
    new_plaintext, new_mac = forge_mac(data, mac, b';admin=true')
    authenticate(new_plaintext, new_mac)


if __name__ == '__main__':
    main()
