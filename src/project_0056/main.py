#!/usr/bin/env python3
"""Command‑line interface for the Fibonacci utilities."""

import argparse
from utils import fibonacci, fibonacci_iterative


def main():
    parser = argparse.ArgumentParser(description="Generate Fibonacci numbers.")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("-n", "--max", type=int,
                       help="Maximum value for the Fibonacci sequence (inclusive).")
    group.add_argument("-c", "--count", type=int,
                       help="Number of Fibonacci numbers to generate from the start.")
    args = parser.parse_args()

    if args.max is not None:
        seq = fibonacci(args.max)
        print(f"Fibonacci numbers up to {args.max}:")
    else:
        seq = fibonacci_iterative(args.count)
        print(f"First {args.count} Fibonacci numbers:")
    print(seq)


if __name__ == "__main__":
    main()
