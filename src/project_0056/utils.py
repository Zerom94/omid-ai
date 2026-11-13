"""Utility functions for generating Fibonacci sequences."""


def fibonacci(limit):
    """
    Return a list of Fibonacci numbers up to the given limit (inclusive).

    Parameters
    ----------
    limit : int
        The maximum value of the Fibonacci numbers to generate. Must be non‑negative.

    Returns
    -------
    list[int]
        Fibonacci numbers less than or equal to ``limit``.
    """
    if limit < 0:
        raise ValueError("limit must be non-negative")
    seq = []
    a, b = 0, 1
    while a <= limit:
        seq.append(a)
        a, b = b, a + b
    return seq


def fibonacci_iterative(count):
    """
    Return the first ``count`` Fibonacci numbers.

    Parameters
    ----------
    count : int
        Number of Fibonacci numbers to generate. Must be non‑negative.

    Returns
    -------
    list[int]
        List containing the first ``count`` Fibonacci numbers.
    """
    if count < 0:
        raise ValueError("count must be non-negative")
    seq = []
    a, b = 0, 1
    for _ in range(count):
        seq.append(a)
        a, b = b, a + b
    return seq
