#!/usr/bin/env python3
"""Entry point for the com package demonstration.

This script imports the `greet` function from the `com` package and prints a sample
message. It can be executed directly from the command line.
"""

from com import module


def main():
    """Run a sample demonstration."""
    result = module.greet("World")
    print(result)


if __name__ == "__main__":
    main()
