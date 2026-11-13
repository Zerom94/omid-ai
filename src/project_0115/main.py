#!/usr/bin/env python3
import sys
from itertools import islice

def fib_generator():
    a, b = 0, 1
    while True:
        yield a
        a, b = b, a + b

def nth_fib(n: int) -> int:
    """Return the n‑th Fibonacci number (0‑indexed)."""
    return next(islice(fib_generator(), n, None))

def main():
    if len(sys.argv) != 2 or not sys.argv[1].isdigit():
        sys.stderr.write("Usage: python main.py N\n")
        sys.exit(1)
    n = int(sys.argv[1])
    # Lazily generate the first n+1 Fibonacci numbers and collect them via a list comprehension
    seq = [str(num) for num in islice(fib_generator(), n + 1)]
    sys.stdout.write("\n".join(seq) + "\n")

if __name__ == "__main__":
    main()
