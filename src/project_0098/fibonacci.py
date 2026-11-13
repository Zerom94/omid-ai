def fibonacci(n):
    """Return the nth Fibonacci number using iteration.
    n must be a non‑negative integer.
    """
    if n < 0:
        raise ValueError('n must be a non‑negative integer')
    a, b = 0, 1
    for _ in range(n):
        a, b = b, a + b
    return a


def fibonacci_sequence(limit):
    """Generate Fibonacci numbers up to *limit*.
    If *limit* is an integer >= 0 it is interpreted as the number of elements to produce.
    If *limit* is a non‑integer number it is interpreted as the maximum value (inclusive).
    """
    seq = []
    a, b = 0, 1
    while True:
        if isinstance(limit, int) and limit >= 0:
            if len(seq) >= limit:
                break
        else:
            if a > limit:
                break
        seq.append(a)
        a, b = b, a + b
    return seq
