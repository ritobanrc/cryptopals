"""
The MIT License (MIT)

Copyright (c) 2013-2015 AJ Alt

Permission is hereby granted, free of charge, to any person obtaining a copy of
this software and associated documentation files (the "Software"), to deal in
the Software without restriction, including without limitation the rights to
use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of
the Software, and to permit persons to whom the Software is furnished to do so,
subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS
FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR
COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER
IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN
CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
"""
#!/usr/bin/env python

from __future__ import print_function, unicode_literals
import struct

try:
    range = xrange
except NameError:
    pass

def _left_rotate(n, b):
    return ((n << b) | (n >> (32 - b))) & 0xffffffff
    
def sha1(message, ml_pad = 0,
         h0 = 0x67452301,
         h1 = 0xEFCDAB89,
         h2 = 0x98BADCFE,
         h3 = 0x10325476,
         h4 = 0xC3D2E1F0):
    """SHA-1 Hashing Function

    A custom SHA-1 hashing function implemented entirely in Python.

    Arguments:
        message: The input message string to hash.

    Returns:
        A SHA-1 digest of the input message.
    """
    # Initialize variables:
    
    # Pre-processing:
    original_byte_len = len(message)
    original_bit_len = original_byte_len * 8
    # append the bit '1' to the message
    message += b'\x80'
    
    # append 0 <= k < 512 bits '0', so that the resulting message length (in bits)
    #    is congruent to 448 (mod 512)
    message += b'\x00' * ((56 - (original_byte_len + 1) % 64) % 64)

    
    # append length of message (before pre-processing), in bits, as 64-bit big-endian integer
    if ml_pad == 0:
        ml_pad = original_bit_len
    message += struct.pack(b'>Q', ml_pad)
    # print('\n-------MESSAGE------\n', len(message), message, '\n-------MESSAGE------\n')
    # Process the message in successive 512-bit chunks:
    # break message into 512-bit chunks
    for i in range(0, len(message), 64):
        w = [0] * 80
        # break chunk into sixteen 32-bit big-endian words w[i]
        for j in range(16):
            # print(message[i + j*4:i+j*4 + 4])
            w[j] = struct.unpack(b'>I', message[i + j*4:i + j*4 + 4])[0]
        # Extend the sixteen 32-bit words into eighty 32-bit words:
        for j in range(16, 80):
            w[j] = _left_rotate(w[j-3] ^ w[j-8] ^ w[j-14] ^ w[j-16], 1)
    
        # Initialize hash value for this chunk:
        a = h0
        b = h1
        c = h2
        d = h3
        e = h4
    
        for i in range(80):
            if 0 <= i <= 19:
                # Use alternative 1 for f from FIPS PB 180-1 to avoid ~
                f = d ^ (b & (c ^ d))
                k = 0x5A827999
            elif 20 <= i <= 39:
                f = b ^ c ^ d
                k = 0x6ED9EBA1
            elif 40 <= i <= 59:
                f = (b & c) | (b & d) | (c & d) 
                k = 0x8F1BBCDC
            elif 60 <= i <= 79:
                f = b ^ c ^ d
                k = 0xCA62C1D6
    
            a, b, c, d, e = ((_left_rotate(a, 5) + f + e + k + w[i]) & 0xffffffff, 
                            a, _left_rotate(b, 30), c, d)
    
        # Add this chunk's hash to result so far:
        h0 = (h0 + a) & 0xffffffff
        h1 = (h1 + b) & 0xffffffff 
        h2 = (h2 + c) & 0xffffffff
        h3 = (h3 + d) & 0xffffffff
        h4 = (h4 + e) & 0xffffffff
   

    # print(hex(h0),
          # hex(h1),
          # hex(h2),
          # hex(h3),
          # hex(h4))
    # Produce the final hash value (big-endian):
    return struct.pack('>IIIII', h0, h1, h2, h3, h4)
    
if __name__ == '__main__':
    # Imports required for command line parsing. No need for these elsewhere
    import argparse
    import sys 
    import os

    # Parse the incoming arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('input', nargs='?',
             help='input file or message to hash')
    args = parser.parse_args()

    data = None

    if args.input is None:
        # No argument given, assume message comes from standard input
        try:
            # sys.stdin is opened in text mode, which can change line endings,
            # leading to incorrect results. Detach fixes this issue, but it's
            # new in Python 3.1
            data = sys.stdin.detach().read()
        except AttributeError:
            # Linux ans OSX both use \n line endings, so only windows is a
            # problem.
            if sys.platform == "win32": 
                import msvcrt
                msvcrt.setmode(sys.stdin.fileno(), os.O_BINARY) 
            data = sys.stdin.read().encode()
    elif os.path.isfile(args.input):
        # An argument is given and it's a valid file. Read it
        with open(args.input, 'rb') as f:
            data = f.read()
    else:
        data = args.input
    
    # Show the final digest
    import binascii
    print('sha1-digest:', binascii.hexlify(sha1(bytes(data, encoding='utf8'))).decode())
