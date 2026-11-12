def fibonacci_sequence(n):
    \"\"\"Return a list of the first n Fibonacci numbers.

    Parameters
    ----------
    n : int
        Number of terms to generate. Must be non‑negative.

    Returns
    -------
    list[int]
        List containing the Fibonacci sequence up to n terms.
    \"\"\"
    if n < 0:
        raise ValueError("n must be a non‑negative integer")
    seq = []
    a, b = 0, 1
    for _ in range(n):
        seq.append(a)
        a, b = b, a + b
    return seq


def fibonacci_number(k):
    \"\"\"Return the k‑th Fibonacci number (0‑based).\"\"\"
    if k < 0:
        raise ValueError("k must be a non‑negative integer")
    a, b = 0, 1
    for _ in range(k):
        a, b = b, a + b
    return a
