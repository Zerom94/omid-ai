def fibonacci(n: int) -> int:
    """Return the n-th Fibonacci number (0-indexed).

    Uses an iterative approach with O(1) extra space.
    Raises ValueError for negative inputs.
    """
    if n < 0:
        raise ValueError("n must be a non-negative integer")
    a, b = 0, 1
    for _ in range(n):
        a, b = b, a + b
    return a
