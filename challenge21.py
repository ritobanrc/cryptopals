import sys

w, n, m, r = 32, 624, 397, 31
a = 0x9908B0DF
(u, d) = (11, 0xFFFFFFFF)
(s, b) = (7, 0x9D2C568016)
(t, c) = (15, 0xEFC6000016)
f = 1812433253
l = 18

MT = [0] * n
index = n + 1
lower_mask = (1 << r) - 1  # the binary number r 1s
upper_mask = 1 << r


def seed_mt(seed):
    global index
    index = n
    MT[0] = seed
    for i in range(1, n):
        MT[i] = int(d & (f * (MT[i - 1] ^ (MT[i - 1] >> 30)) + i))


def extract_number():
    global index
    if index >= n:
        if index > n:
            sys.stderr.write('error: Generator was never seeded')
            return
        twist()
    y = MT[index]
    y = y ^ ((y >> u) & d)
    y = y ^ ((y << s) & b)
    y = y ^ ((y << t) & c)
    y = y ^ (y >> l)

    index = index + 1
    return d & y


def twist():
    global index
    for i in range(0, n):
        x = (MT[i] & upper_mask) + (MT[(i + 1) % n] & lower_mask)
        xA = x >> 1
        if x % 2 != 0:
            xA = xA ^ a
        MT[i] = MT[(i + m) % n] ^ xA
    index = 0


def main():
    seed_mt(0)
    outfile = open('challenge21_out.txt', 'w+')
    for i in range(1000):
        outfile.write(str(extract_number()))
        outfile.write(', ')


if __name__ == '__main__':
    main()
