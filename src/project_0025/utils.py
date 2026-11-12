def factorial(n):
    """Return the factorial of a non‑negative integer n."""
    if n < 0:
        raise ValueError("n must be non‑negative")
    result = 1
    for i in range(2, n+1):
        result *= i
    return result
