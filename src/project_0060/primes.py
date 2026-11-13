"""
Utility functions for prime number calculations.
"""


def is_prime(n: int) -> bool:
    """Return True if n is a prime number, else False."""
    if n < 2:
        return False
    if n == 2:
        return True
    if n % 2 == 0:
        return False
    limit = int(n ** 0.5) + 1
    for i in range(3, limit, 2):
        if n % i == 0:
            return False
    return True


def generate_primes(limit: int):
    """Yield prime numbers up to (and including) limit."""
    for num in range(2, limit + 1):
        if is_prime(num):
            yield num


def first_n_primes(count: int):
    """Yield the first `count` prime numbers."""
    found = 0
    num = 2
    while found < count:
        if is_prime(num):
            yield num
            found += 1
        num += 1
