from hashlib import sha1
from challenge2 import fixed_xor

# These are hardcoded values for sha1
block_size = 64
output_size = 20

def hmac_sha1(key, message):
    if len(key) > block_size:
        key = sha1(key).digest()
    if len(key) < block_size:
        key += (block_size - len(key))*b'\x00'
    o_key_pad = fixed_xor(key, b'\x5c'*block_size)
    i_key_pad = fixed_xor(key, b'\x36'*block_size)

    return sha1(o_key_pad + sha1(i_key_pad + message).digest()).digest()

def main():
    import binascii
    assert binascii.hexlify(hmac_sha1(b'', b'')) == b'fbdb1d1b18aa6c08324b7d64b71fb76370690e1d'
    assert (binascii.hexlify(hmac_sha1(b'key', b'The quick brown fox jumps over the lazy dog'))
            == b'de7c9b85b8b78aa6bc8a7a36f70a90701c9db4d9')

if __name__ == '__main__':
    main()
