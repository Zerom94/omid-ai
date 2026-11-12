from utils import power


def main():
    """Demonstrate the `power` function with a few example calculations."""
    examples = [
        (2, 3),       # 2^3 = 8
        (5, 0),       # 5^0 = 1
        (9, -2),      # 9^-2 = 0.012345...
        (2.5, 4),     # 2.5^4 = 39.0625
    ]
    for base, exp in examples:
        result = power(base, exp)
        print(f"{base} ^ {exp} = {result}")


if __name__ == "__main__":
    main()
