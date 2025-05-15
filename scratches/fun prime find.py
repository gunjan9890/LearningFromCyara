#!/bin/python3
import math
import sys
from datetime import datetime


def get_nth_prime(n: int):
    known_primes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29]
    if n <= 10:
        return known_primes[n - 1]
    else:
        possible_prime = known_primes[-1] + 2
        while len(known_primes) < n:
            found_prime = True
            limit = math.ceil(math.sqrt(possible_prime))
            for prime in known_primes[1:]:
                if limit >= prime:
                    if possible_prime % prime == 0:
                        found_prime = False
                        break
                else:
                    break
            if found_prime:
                known_primes.append(possible_prime)
            possible_prime += 2
        return known_primes[n - 1]


t = int(input().strip())
for a0 in range(t):
    n = int(input().strip())
    print(datetime.now())
    print(get_nth_prime(n))
    print(datetime.now())
