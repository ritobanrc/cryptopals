#!/usr/bin/python3
import random
import binascii
import struct
from md4 import MD4

def secret_prefix_mac(message, key):
    md4 = MD4(key + message)
    return md4.digest()

data = b'comment1=cooking%20MCs;userdata=foo;comment2=%20like%20a%20pound%20of%20bacon'
with open('/usr/share/dict/words') as f:
    prefix = bytes(random.choice(f.readlines()), encoding='utf8')

def get_mac():
    mac = secret_prefix_mac(data, prefix)
    return mac


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

def get_md4_padding(message):
    length = struct.pack('<Q', len(message) * 8)
    message += b'\x80'
    message += bytes((56 - len(message) % 64) % 64)
    message += length
    return message

def forge_sha1_mac(original_message, mac, append):
    A, B, C, D = struct.unpack('<IIII', mac)
    for prefix_length in range(1, 20):
        print(f'PREFIX LENGTH: {prefix_length}')
        to_pad = b'a' * prefix_length  + original_message
        padded = get_md4_padding(to_pad)

        md4 = MD4(append, len(padded) + len(append), A, B, C, D)
        new_mac = md4.digest()

        new_plaintext = padded[prefix_length:] + append
        if authenticate(new_plaintext, new_mac):
            return new_plaintext, new_mac
    return b'', b''


def main():
    mac = get_mac()
    print('Original MAC: ', binascii.hexlify(mac))
    authenticate(data, mac)
    new_plaintext, new_mac = forge_sha1_mac(data, mac, b';admin=true')
    authenticate(new_plaintext, new_mac)

if __name__ == '__main__':
    main()
