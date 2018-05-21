def pkcs7padding(block, block_length):
    # Do stuff
    p = block_length - len(block)
    return block + bytes([p]) * p


if __name__ == '__main__':
    print(pkcs7padding(b"YELLOW SUBMARINE", 20))
