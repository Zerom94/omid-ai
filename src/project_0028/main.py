"""Entry point for the simple example project.

The script imports utility functions from :pymod:`utils` and demonstrates
their usage.  Running the module will print a greeting and the result of an
addition.
"""

from utils import greet, add


def main() -> None:
    # Demonstrate the greeting function
    name = "World"
    print(greet(name))

    # Demonstrate the add function
    a, b = 3.5, 4.2
    result = add(a, b)
    print(f"{a} + {b} = {result}")


if __name__ == "__main__":
    main()
