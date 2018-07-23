import challenge15


def pkcs7padding(block, block_length = 0):
    if block_length == 0:
        block_length = len(block) + (16 - (len(block) % 16))
    p = block_length - len(block)
    return block + bytes([p]) * p


def unpad_pkcs7(padded):
    '''
    obsolete. Use challenge15.strip_pkcs7padding
    :param padded:
    :return:
    '''
    # count = padded[-1]
    # return padded[:-count]
    return challenge15.strip_pkcs7padding(padded)


if __name__ == '__main__':
    print(pkcs7padding(b"YELLOW SUBMARINE", 20))
