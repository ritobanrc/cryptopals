from struct import pack


def strip_pkcs7padding(plaintext):
    try:
        plaintext = bytearray(plaintext, encoding='utf-8')
    except TypeError:
        plaintext = bytearray(plaintext)
    pad_length = plaintext[-1]
    padding = pack('=B', pad_length)*pad_length
    if plaintext[-pad_length:] != padding:
        raise ValueError
    return plaintext[:-pad_length]


if __name__ == '__main__':
    print(strip_pkcs7padding('ICE ICE BABY\x04\x04\x04\x04'))
    try:
        strip_pkcs7padding('ICE ICE BABY\x01\x02\x03\x04')
    except ValueError:
        print('Success')
