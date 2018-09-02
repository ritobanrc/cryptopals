#!/usr/bin/env python3

import sys

w, n, m, r = 32, 624, 397, 31
a = 0x9908B0DF
(u, d) = (11, 0xFFFFFFFF)
(s, b) = (7, 0x9D2C568016)
(t, c) = (15, 0xEFC6000016)
f = 1812433253
l = 18

class MersenneTwister:
    def __init__(self):
        self.MT = [0] * n
        self.index = n + 1
        self.lower_mask = (1 << r) - 1  # the binary number r 1s
        self.upper_mask = 1 << r
    
    
    def seed_mt(self, seed):
        self.index = n
        self.MT[0] = seed
        for i in range(1, n):
            self.MT[i] = int(d & (f * (self.MT[i - 1] ^ (self.MT[i - 1] >> 30)) + i))
    
    
    def extract_number(self):
        if self.index >= n:
            if self.index > n:
                sys.stderr.write('error: Generator was never seeded')
                return
            self.twist()
        y = self.MT[self.index]
        y = y ^ ((y >> u) & d)
        y = y ^ ((y << s) & b)
        y = y ^ ((y << t) & c)
        y = y ^ (y >> l)
    
        self.index = self.index + 1
        return d & y
    
    
    def twist(self):
        for i in range(0, n):
            x = (self.MT[i] & self.upper_mask) + (self.MT[(i + 1) % n] & self.lower_mask)
            xA = x >> 1
            if x % 2 != 0:
                xA = xA ^ a
            self.MT[i] = self.MT[(i + m) % n] ^ xA
        self.index = 0
    
    
def main():
    rng = MersenneTwister()
    rng.seed_mt(42)
    outfile = open('challenge21_out.txt', 'w+')
    for i in range(1000):
        number = rng.extract_number() % 100
        print(number)
        outfile.write(str(number))
        outfile.write(', ')


if __name__ == '__main__':
    main()
