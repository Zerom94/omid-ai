#!/usr/bin/env python3
import argparse
from com import greet, add_numbers

def main() -> None:
    parser = argparse.ArgumentParser(description="Simple CLI for the com package.")
    parser.add_argument("-n", "--name", type=str, default="World", help="Name to greet")
    parser.add_argument("-a", "--add", nargs=2, metavar=("X", "Y"), type=float,
                        help="Add two numbers and display the result")
    args = parser.parse_args()

    print(greet(args.name))

    if args.add:
        x, y = args.add
        result = add_numbers(x, y)
        print(f"The sum of {x} and {y} is {result}")

if __name__ == "__main__":
    main()
