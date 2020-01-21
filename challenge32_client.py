#!/usr/bin/python3

import requests
import binascii

URL = '127.0.0.1'
PORT = 5000

def make_request(mac):
    payload = {'file': 'challenge31_data.txt', 'signature': binascii.hexlify(mac)}
    total_time = 0
    for _ in range(3): 
        response = requests.get(f'http://{URL}:{PORT}', payload)
        if response.status_code == 200:
            print(f'Success. MAC: {binascii.hexlify(mac)}')
            return True, 0
        total_time += response.elapsed.total_seconds()
    return False, total_time

def main():
    mac = bytearray()
    for i in range(64):
        max_time = 0
        for c in range(0, 255):
            success, elapsed = make_request(mac + bytes([c]))
            if success:
                break
            if elapsed > max_time:
                max_time = elapsed
                char = c
        mac.append(char)
        print(max_time, hex(char))
        if success:
            print(binascii.hexlify(mac))
            break


if __name__ == '__main__':
    main()


