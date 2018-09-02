#!/usr/bin/env python3

import random  # just being used to simulate a real application
import time
from challenge21 import MersenneTwister

seed = 0  # for testing purposes

def get_random_number():
    global seed 
    time.sleep(random.randint(40, 100))
    seed = int(time.time())
    rng = MersenneTwister()
    rng.seed_mt(seed)
    time.sleep(random.randint(40, 100))
    return rng.extract_number()


def crack_rng_seed(random_number):
    for i in range(int(time.time() - 140), int(time.time() - 40)):
        rng = MersenneTwister()
        rng.seed_mt(i)
        if rng.extract_number() == random_number:
            seed = i
            break
    return seed


def main():
    for i in range(10):
        assert crack_rng_seed(get_random_number()) == seed  # we expect no errors here
    print("Success!")


if __name__ == '__main__':
    main()
