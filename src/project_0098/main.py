#!/usr/bin/env python3
import argparse
from fibonacci import fibonacci, fibonacci_sequence

def parse_args():
    parser = argparse.ArgumentParser(description='Fibonacci utilities')
    subparsers = parser.add_subparsers(dest='command', required=True)

    nth_parser = subparsers.add_parser('nth', help='Compute the nth Fibonacci number')
    nth_parser.add_argument('n', type=int, help='Zero‑based index of the Fibonacci number')

    seq_parser = subparsers.add_parser('seq', help='Generate a Fibonacci sequence')
    seq_parser.add_argument('limit', type=float, help='Number of elements (int) or max value (float)')
    return parser.parse_args()

def main():
    args = parse_args()
    if args.command == 'nth':
        try:
            print(fibonacci(args.n))
        except ValueError as e:
            print(f'Error: {e}')
    elif args.command == 'seq':
        # If limit is an integer value (e.g., "10" or "10.0"), treat it as a count.
        limit = int(args.limit) if args.limit.is_integer() else args.limit
        seq = fibonacci_sequence(limit)
        print(seq)

if __name__ == '__main__':
    main()
