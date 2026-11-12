import argparse
import sys
from . import math_utils

def _parse_args(argv):
    parser = argparse.ArgumentParser(
        prog="com",
        description="Command line utilities for common math operations."
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    fact_parser = subparsers.add_parser("factorial", help="Compute factorial of a non‑negative integer.")
    fact_parser.add_argument("n", type=int, help="Non‑negative integer.")

    fib_parser = subparsers.add_parser("fibonacci", help="Compute nth Fibonacci number (0-indexed).")
    fib_parser.add_argument("n", type=int, help="Non‑negative integer index.")

    prime_parser = subparsers.add_parser("isprime", help="Test if a number is prime.")
    prime_parser.add_argument("n", type=int, help="Integer to test.")

    return parser.parse_args(argv)

def main(argv=None):
    args = _parse_args(argv or sys.argv[1:])
    if args.command == "factorial":
        try:
            result = math_utils.factorial(args.n)
            print(result)
        except ValueError as e:
            print(f"Error: {e}", file=sys.stderr)
            sys.exit(1)
    elif args.command == "fibonacci":
        try:
            result = math_utils.fibonacci(args.n)
            print(result)
        except ValueError as e:
            print(f"Error: {e}", file=sys.stderr)
            sys.exit(1)
    elif args.command == "isprime":
        result = math_utils.is_prime(args.n)
        print(f"{args.n} is {'a' if result else 'not a'} prime number.")
    else:
        # This branch should never be reached because argparse enforces choices
        sys.stderr.write("Unknown command\n")
        sys.exit(2)

if __name__ == "__main__":
    main()
