def pkcs7padding(block, block_length = 0):
    if block_length == 0:
        block_length = len(block) + (16 - (len(block) % 16))
    p = block_length - len(block)
    return block + bytes([p]) * p


def unpad_pkcs7(padded):
    count = padded[-1]
    return padded[:-count]


if __name__ == '__main__':
    print(pkcs7padding(b"YELLOW SUBMARINE", 20))
