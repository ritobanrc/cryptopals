import random  # just being used to simulate a real application
import time

import challenge21


def get_random_number():
    time.sleep(random.randint(40, 100))
    seed = int(time.time())
    print(seed)
    challenge21.seed_mt(seed)
    time.sleep(random.randint(40, 100))
    return challenge21.extract_number()


def crack_rng_seed(random_number):
    for i in range(int(time.time() - 140), int(time.time() - 40)):
        challenge21.seed_mt(i)
        if challenge21.extract_number() == random_number:
            seed = i
            break
    return seed


def main():
    for i in range(10):
        print(crack_rng_seed(get_random_number()))


if __name__ == '__main__':
    main()
