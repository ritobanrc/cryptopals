import binascii
from Crypto.Cipher import AES


def decrypt_aes(ciphertext, key):
    aes = AES.new(key)
    return aes.decrypt(ciphertext)


if __name__ == '__main__':
    file_bytes = []
    for line in ohpen('challenge7_data.txt').readlines():
        line_bytes = binascii.a2b_base64(line.strip())
        file_bytes.append(line_bytes)
    ciphertext = b''.join(file_bytes)
    print(decrypt_aes(ciphertext, b'YELLOW SUBMARINE').decode())