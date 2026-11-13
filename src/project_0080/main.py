#!/usr/bin/env python3
"""Entry point for the com project."""

import argparse
from com.core import greet

def main() -> None:
    parser = argparse.ArgumentParser(description="Demo com package CLI")
    parser.add_argument(
        "-n", "--name", type=str, default="World", help="Name to greet"
    )
    args = parser.parse_args()
    print(greet(args.name))

if __name__ == "__main__":
    main()
