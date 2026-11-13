def fibonacci(n):
    """Return the nth Fibonacci number (0-indexed)."""
    if n < 0:
        raise ValueError("n must be non-negative")
    a, b = 0, 1
    for _ in range(n):
        a, b = b, a + b
    return a

def fibonacci_sequence(limit):
    """Generate Fibonacci numbers up to *limit* (inclusive)."""
    a, b = 0, 1
    while a <= limit:
        yield a
        a, b = b, a + b
