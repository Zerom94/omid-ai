#!/usr/bin/env python3
\"\"\"Command‑line interface for Fibonacci calculations.

Usage:
    python main.py <n>
    Prints the first n Fibonacci numbers.
\"\"\"

import sys
from fibonacci import fibonacci_sequence, fibonacci_number

def main():
    if len(sys.argv) != 2:
        print("Usage: python main.py <non‑negative integer>")
        sys.exit(1)
    try:
        n = int(sys.argv[1])
        if n < 0:
            raise ValueError
    except ValueError:
        print("Please provide a non‑negative integer.")
        sys.exit(1)

    seq = fibonacci_sequence(n)
    print(f"First {n} Fibonacci numbers: {seq}")
    if n > 0:
        print(f"The {n-1}-th Fibonacci number is {fibonacci_number(n-1)}")

if __name__ == "__main__":
    main()
