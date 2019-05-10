#!/usr/bin/python3
import os
import random
import binascii
import time
from flask import request, abort
from flask_api import FlaskAPI, status
from my_hmac import hmac_sha1

APP = FlaskAPI(__name__)

with open('/usr/share/dict/words') as f:
    key = bytes(random.choice(f.readlines()), encoding='utf8')[:-1]

print(key)

@APP.route('/')
def index():
    filename = request.args.get('file', '')
    submitted_mac = request.args.get('signature', '')
    print(filename, os.path.exists(filename))
    if filename == '' or submitted_mac == '':
        return ''
    if not os.path.exists(filename):
        return ''
    with open(filename, 'rb') as f:
        data = f.read()
    actual_mac = hmac_sha1(key, data)
    submitted_mac = binascii.unhexlify(submitted_mac)
    if insecure_compare(actual_mac, submitted_mac):
        return f'<h1>{filename}</h1> {str(data)}', 200
    abort(500)

def insecure_compare(buf1, buf2):
    for b1, b2 in zip(buf1, buf2):
        if not b1 == b2:
            return False
        time.sleep(0.050)
    return True

if __name__ == '__main__':
    APP.debug = True
    APP.run()

