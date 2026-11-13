#!/usr/bin/env python3
import sys
from itertools import islice

def fibonacci():
    """Infinite generator of Fibonacci numbers starting from 0, 1, ..."""
    a, b = 0, 1
    while True:
        yield a
        a, b = b, a + b

def main():
    # Expect a single integer argument: number of terms to produce
    if len(sys.argv) != 2:
        sys.stderr.write("Usage: python main.py <n>\n")
        sys.exit(1)
    try:
        n = int(sys.argv[1])
    except ValueError:
        sys.stderr.write("Argument must be an integer.\n")
        sys.exit(1)

    # Lazily take the first n Fibonacci numbers
    fib_numbers = list(islice(fibonacci(), n))
    # Efficiently output using a generator expression and str.join
    sys.stdout.write("\n".join(str(num) for num in fib_numbers))

if __name__ == "__main__":
    main()
